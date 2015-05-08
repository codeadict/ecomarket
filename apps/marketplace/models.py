import copy
from decimal import Decimal
from discounts.models import FreeShipping
import datetime
import pytz

from django.conf import settings
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.core.validators import MaxLengthValidator
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import models
from django.db.models import permalink, Max, Q
from django.db.models.signals import post_save
from django.template.defaultfilters import slugify
from django.contrib.contenttypes.models import ContentType

from django.utils.translation import ugettext_lazy as _

from django_extensions.db.fields import AutoSlugField
from django_extensions.db.fields.json import JSONField

from actstream import action

from money import Money
from money.contrib.django.models.fields import MoneyField

from main.utils import generate_identifier
from marketplace.managers import StallManager, ProductManager, CategoryManager
from purchase import settings as purchase_settings
from marketplace.fields import \
    ProductImageField, ProductImageThumbsField, NullableMoneyField

from image_crop.fields import ImageWithPreviewField, calculate_auto_crop

from marketplace.wrong import SOME_WIERD_DATA_THAT_SHOULDNT_BE_HERE

from categories.models import CategoryBase


# Product Attributes
# =================
class Category(CategoryBase):
    """
    Contains hierarchial product categories
    """

    seo_title = models.CharField(max_length=511, blank=True, null=True,
                                 verbose_name="SEO title")
    description = models.CharField(max_length=511, blank=True, null=True,
                                   verbose_name="On-page description")
    navigation_name = models.CharField(max_length=100)
    image_src = models.CharField(max_length=255, blank=True, null=True)
    objects = CategoryManager()

    def get_non_empty_children(self):
        """FIXME: temporary hack for search"""
        for cat in self.get_children():
            # line removed, so now this method is basically a proxy
            yield cat

    def is_traversable_in_search_selector(self):
        """FIXME: ugly hack for search, long term solution is use faceting"""
        return self.id not in SOME_WIERD_DATA_THAT_SHOULDNT_BE_HERE

    def get_top_level_parent(self):
        category = self
        while(category.parent is not None):
            category = category.parent
        return category

    def _get_slugs(self):
        slugs = [self.slug]
        category = self
        while category.parent is not None:
            category = category.parent
            slugs.insert(0, category.slug)
        return slugs

    def get_slug_path(self):
        # Example: "/category1-name/category2-name/"
        return "/".join(self._get_slugs() + [""])

    def get_absolute_url(self):
        slugs = self._get_slugs()
        url_name = "category_discover"
        return reverse(url_name, args=slugs)

    def get_search_url(self):
        slugs = self._get_slugs()
        return reverse('product_search', args=slugs)

    def get_discover_url(self):
        slugs = self._get_slugs()
        return reverse('category_discover', args=slugs)

    @staticmethod
    def sort_by_popularity(categories):
        # FIXME why does the below create a load of duplicates?
        #return categories.order_by("products__number_of_sales")
        # TODO Do not use inefficient sort.
        return sorted(categories, key=(
            lambda cat: cat.products.order_by("number_of_sales")[0]))

    def update_image(self, product=None):
        """
        Use the image of the most popular recently sold product as the category
        image.

        :params product: Optionally force it to use this product as the image
        """
        if product is not None:
            if product.stock == 0:
                product = None
        if product is None:
            products = (self.products.live()
                            .exclude(stock=0)
                            .order_by('-number_of_recent_sales')[:1])
            if len(products):
                product = products[0]
        if product is None:
            self.image_src = '/static/images/blank.png'
            return False
        if self.image_src == product.image.thumbnail.url:
            return False
        self.image_src = product.image.thumbnail.url
        return True

    class Meta:
        verbose_name_plural = 'categories'
        ordering = ("name", )


class ProductAttributeBase(models.Model):
    title = models.CharField(_('title'), unique=True, max_length=200)
    slug = AutoSlugField(populate_from='title', editable=True)
    description = models.TextField(blank=True, default='', null=False)
    seo_title = models.CharField(max_length=511, blank=True, null=True,
                                 verbose_name="SEO title")

    class Meta:
        abstract = True

    def __unicode__(self, *args, **kwargs):
        return self.title


class Cause(ProductAttributeBase):
    pass


class Certificate(ProductAttributeBase):
    url = models.URLField()
    cause = models.ForeignKey(
        Cause,
        related_name="certificates")
    image = ImageWithPreviewField(
        upload_to='product/certificates/',
        max_length=255,
        null=True,
        preview_size=(300, 200))


class Color(ProductAttributeBase):
    pass


class Ingredient(ProductAttributeBase):
    pass


class Material(ProductAttributeBase):
    pass


class Keyword(ProductAttributeBase):
    pass


class Occasion(ProductAttributeBase):
    pass


class Recipient(ProductAttributeBase):
    pass


class StallCategory(CategoryBase):
    """
    Contains hierarchial stall categories
    """

    class Meta:
        verbose_name_plural = 'stall categories'


REASON_FOR_SUSPENSION = (
    (1, 'Seller is not responding to Emails'),
    (2, 'Seller is not updating Stock'),
    (3, 'Seller is not dispatching Orders'),
    (4, 'Seller can not be reached at contact details specified'),
)

# For each tier we give Stall owners a certain number of maximum days within which they
# must do a stock check, or their stall is suspended.
RENEWAL_TIER_LIMITS = {
    1: 7,
    2: 14,
    3: 30,
    4: 90,
    5: 180,
    6: 360,
    7: 1800,
}

class Stall(models.Model):
    """
    Represents a stall owner's stall.

    NOTE
    # In the purchasing sprint you will need to collect the
    # bank details for the seller as well so that we can collect
    # commission.

    """
    user = models.OneToOneField(User, related_name='stall')
    title = models.CharField(
        _('Stall name'), max_length=60, default='', unique=True)
    slug = AutoSlugField(populate_from='title', unique=True)
    description_short = models.CharField(
        _('short stall description'), max_length=90,
        blank=True, default='', null=False)
    description_full = models.TextField(
        _('full stall description'), blank=True, default='', null=False,
        validators=[MaxLengthValidator(215)])

    # unique numeric identifier between 10000000 and 99999999
    identifier = models.IntegerField(
        max_length=8, default=0)

    paypal_email = models.EmailField(
        max_length=255, blank=True, default='', null=False)
    phone_landline = models.CharField(
        max_length=16, blank=True, null=True,
        verbose_name=_("Home/Office phone"))
    phone_mobile = models.CharField(
        max_length=16, null=True,
        verbose_name=_("Mobile phone"))
    twitter_username = models.CharField(
        max_length=255, blank=True, default='', null=False)

    message_after_purchasing = models.TextField(
        _('message after purchasing'), blank=True, default='', null=False)
    refunds_policy = models.TextField(
        _('refund policy'), blank=True, default='', null=False)
    returns_policy = models.TextField(
        _('returns policy'), blank=True, default='', null=False)

    holiday_mode = models.BooleanField(
        _('holidy mode'), blank=True, default=False, null=False)
    holiday_message = models.TextField(
        _('message to customers'), blank=True, default='', null=False)

    is_chat_enabled = models.BooleanField(
        _('chat enabled'), blank=True, default=False, null=False)
    chat_stall_uri = models.URLField(
        _('URI of the chat widget'), blank=True, default=False, null=False)
    chat_operator_uri = models.URLField(
        _('URI of the chat operator'), blank=True, default=False, null=False)

    category = models.ForeignKey(
        StallCategory, verbose_name="main category",
        related_name="stalls", null=True, blank=True)

    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)

    email_opt_in = models.BooleanField(default=True)

    # We compulsorily ask Sellers to do a Stock Check
    # Check Card #183 - https://trello.com/c/YVF5y7EI/183
    renewal_tier = models.PositiveSmallIntegerField(default=3)
    is_suspended = models.BooleanField(default=False, verbose_name='Suspended?')
    reason_for_suspension = models.PositiveSmallIntegerField(choices=REASON_FOR_SUSPENSION,
        blank=True, null=True, verbose_name='Suspension Reason')
    last_stock_checked_at = models.DateTimeField(default=datetime.datetime.now)

    total_gmv_till_yesterday = models.DecimalField(max_digits=10, decimal_places=2, default=0.0, verbose_name='Total GMV')
    total_orders_till_yesterday = models.PositiveSmallIntegerField(default=0, verbose_name='Total Orders')

    total_suspensions_till_yesterday = models.PositiveSmallIntegerField(default=0, verbose_name='Suspensions till date')
    is_active = models.BooleanField(default=False, verbose_name='Active?')

    total_products_till_yesterday = models.PositiveSmallIntegerField(default=0, verbose_name='Total Products')
    total_live_products_till_yesterday = models.PositiveSmallIntegerField(default=0, verbose_name='Live Products')
    total_messages_received_till_yesterday = models.PositiveSmallIntegerField(default=0, verbose_name='Messages Received')
    days_to_next_stockcheck_till_yesterday = models.PositiveSmallIntegerField(default=0, verbose_name='Stock Check in')

    number_of_calls = models.PositiveSmallIntegerField(default=0, verbose_name='Number of Calls')

    is_closed = models.BooleanField(default=False, verbose_name='Closed?',
        help_text='Closed stalls are preserved only as archive. All of their products are un-published.')
    is_in_video_beta = models.BooleanField(default=False, help_text='In Video Beta?')
    objects = StallManager()

    def __unicode__(self):
        return u"{0}:{1}".format(self.user.username, self.title)

    @staticmethod
    @permalink
    def _get_absolute_url(slug):
        """Wrapper function"""
        return ('my_stall', (), {'slug': slug})

    def get_absolute_url(self):
        return Stall._get_absolute_url(self.slug)

    @property
    def admin_url(self):
        url = reverse('admin:%s_%s_change' %(self._meta.app_label,  self._meta.module_name),  args=[self.id])
        return url

    def get_welcome_video(self):
        welcome_videos = self.videos.filter(
            is_welcome=True, is_published=True).order_by('-created')[:1]
        if len(welcome_videos) == 1:
            return welcome_videos[0]

    def has_welcome_video(self):
        return self.get_welcome_video() is not None

    def get_latest_video(self):
        latest = self.videos.filter(
            is_welcome=True,
            is_published=True).order_by('-created')
        if latest.count():
            return latest[:1][0]

    def save(self, *args, **kwargs):
        """ Overriden the save to slugify the name on save. """
        self.slug = slugify(self.title)
        if self.identifier == 0:
            self.identifier = generate_identifier(Stall)
        super(Stall, self).save(*args, **kwargs)

    @property
    def total_gmv(self):
        """Total Gross Merchandise Value of sales
        See also: UserProfile.total_gmv
        """
        orders = self.orders
        paid_orders = orders.filter(Q(is_joomla_order=True) | ~Q(payment=None))
        return Money(0, purchase_settings.DEFAULT_CURRENCY) + sum(
            [obj.total() for obj in paid_orders])

    @property
    def completeness(self):
        """ Returns a completeness score for the stall profile. """
        score = 0.0
        if self.products.count() > 0:
            score += 0.25
        #TODO: add more checks here as and when they become available.
        return int(score * 100)

    # TODO
    @property
    def shipping_record(self):
        return 85

    @property
    def num_reviews(self):
        return 0

    @property
    def avg_review(self):
        return 0

    @property
    def times_suspended(self):
        return self.stockcheck.filter(suspended=True).count()

    @property
    def days_to_next_stockcheck(self):
        now = datetime.datetime.now(tz=pytz.utc)

        # NOTE: For some strange reason sometimes the field get fetched from the
        # database timezone unaware. To fix this we add the tzinfo everytime.
        last_stock_checked_at = self.last_stock_checked_at.replace(tzinfo=pytz.utc)

        if self.renewal_tier:
            days = RENEWAL_TIER_LIMITS[self.renewal_tier] - (now - last_stock_checked_at).days
        else:
            days = 30 - (now - last_stock_checked_at).days
        return days

    @property
    def stockcheck_days_limit(self):
        return RENEWAL_TIER_LIMITS[self.renewal_tier]

    def delete(self):
        now = datetime.datetime.now(tz=pytz.utc)
        self.products.all().update(status=Product.PUBLISHED_CLOSED, updated=now)
        self.is_closed = True
        self.save()
        self.user.is_active = False
        self.user.save()

    @property
    def has_stock_checked_ever(self):
        # This was the datetime of deployment of stock check feature on Live server
        dt = datetime.datetime(2013, 10, 22, 16, 49, 42, tzinfo=pytz.utc)
        # All existing stalls had this default datetime for last stock check
        # If last stock check date is later than default, then stall had a stock check
        if self.created < dt.date() and self.last_stock_checked_at > dt:
            return True
        # If new stall, then check they have done stock on a later day after stall creation
        if self.created > dt.date() and self.last_stock_checked_at.date() > self.created:
            return True
        return False


class StallOldStylePhoneNumber(models.Model):

    stall = models.OneToOneField(Stall, related_name="phone_old")
    phone_number = models.CharField(max_length=20)

    def __unicode__(self):
        return unicode(self.phone_number)


class StallVideo(models.Model):
    """
    Associates a Video URL with a Stall
    """
    stall = models.ForeignKey(Stall, related_name="videos")
    title = models.CharField(_('Video Title'), max_length=60)
    url = models.CharField(_('Video URL'), max_length=255)
    is_welcome = models.BooleanField(_('Welcome Video?'))
    is_published = models.BooleanField(_('Is Published?'))
    created = models.DateTimeField(
        _('Creation Date'),
        auto_now_add=True, editable=False)

    def __unicode__(self):
        return u"{0}: {1}".format(self.stall.title, self.title)


class Price(models.Model):
    """
    TODO:how would we ensure only one type of currency per product is stored?
    """
    product = models.ForeignKey('Product', related_name='prices')
    amount = MoneyField(
        _(u'price'), max_digits=6, decimal_places=2,
        null=False,
        default_currency=purchase_settings.DEFAULT_CURRENCY)


class Product(models.Model):
    """ Represents a product within a stall. """
    PUBLISHED_DRAFT = 'd'
    PUBLISHED_LIVE = 'l'
    PUBLISHED_UNPUBLISHED = 'u'
    PUBLISHED_DELETED = 'x'
    PUBLISHED_SUSPENDED = 's'
    PUBLISHED_CLOSED = 'c'

    PUBLISHED_STATUS = (
        (PUBLISHED_DRAFT, 'Draft'),
        (PUBLISHED_LIVE, 'Live'),
        (PUBLISHED_UNPUBLISHED, 'Unpublished'),
        (PUBLISHED_DELETED, 'Deleted'),
        (PUBLISHED_SUSPENDED, 'Suspended'),
        (PUBLISHED_CLOSED, 'Stall Closed'),
    )

    FLAGS = (
        (0, 'faulty shipping profile'),
    )

    cached_vars = ['status']

    def __init__(self, *args, **kwargs):
        super(Product, self).__init__(*args, **kwargs)
        self.var_cache = {}
        for var in self.cached_vars:
            self.var_cache[var] = copy.copy(getattr(self, var))

        self.shipping_discounts = {}
        self.free_shippings = {}
        self.shipping_prices = {}

    stall = models.ForeignKey('Stall', related_name='products')
    title = models.CharField(max_length=200, unique=True)
    description = models.TextField()
    slug = AutoSlugField(populate_from='title')

    causes = models.ManyToManyField(
        Cause, blank=True, null=True, related_name='products')
    certificates = models.ManyToManyField(
        Certificate, blank=True, null=True, related_name='products')
    colors = models.ManyToManyField(
        Color, verbose_name=_('main colors'),
        blank=False, null=False, related_name='products')
    ingredients = models.ManyToManyField(
        Ingredient, blank=True, null=True, related_name='products')
    materials = models.ManyToManyField(
        Material, blank=True, null=True,
        related_name='products', verbose_name="Eco Materials")
    keywords = models.ManyToManyField(
        Keyword, blank=True, null=True, related_name='products')
    occasions = models.ManyToManyField(
        Occasion, blank=True, null=True, related_name='products')
    recipients = models.ManyToManyField(
        Recipient, blank=False, null=False, related_name='products')

    # None means unlimited, 0 means no stock.
    stock = models.IntegerField(
        blank=True, default=None, null=True)

    shipping_profile = models.ForeignKey(
        'ShippingProfile',
        related_name='products')

    primary_category = models.ForeignKey(
        Category, verbose_name="main category",
        related_name="products", null=True, blank=True)
    secondary_category = models.ForeignKey(
        Category, verbose_name="secondary category",
        related_name="secondary_products", null=True, blank=True)

    status = models.CharField(
        max_length=1, choices=PUBLISHED_STATUS, default=PUBLISHED_DRAFT)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    publication_date = models.DateTimeField(null=True, blank=True)

    # For ordering. Must be updated when a sale is made
    number_of_sales = models.IntegerField(default=0)

    # This is updated using a cron job
    number_of_recent_sales = models.SmallIntegerField(default=0)

    flag = models.PositiveIntegerField(
        blank=True,
        null=True,
        choices=FLAGS,
    )

    objects = ProductManager()

    def __unicode__(self):
        return u"{0}:{1}".format(
            self.stall.title,
            self.title)

    @property
    def ships_from_country(self):
        if self.shipping_profile:
            if self.shipping_profile.shipping_country:
                return self.shipping_profile.shipping_country.code
        return 'UK'

    @property
    def categories(self):
        return [c.name for c in self.category_objs()]

    def category_objs(self):
        cat = self.primary_category
        cats = []
        while cat:
            cats.append(cat)
            cat = cat.parent
        return reversed(cats)

    @property
    def category_tree(self):
        return ' > '.join([c.name for c in self.category_objs()])

    @staticmethod
    def _path(stall_identifier, slug):
        return '/products/%s/%s/' % (
            stall_identifier, slug)

    @property
    def path(self):
        """Wrapper function"""
        return Product._path(self.stall.identifier, self.slug)

    @permalink
    def get_absolute_url(self):
        return ('product_page', (),
                {'product_name': self.slug,
                 'stall_identifier': self.stall.identifier})

    @property
    def price(self):
        return self.get_price_instance()

    def has_free_shipping(self, country):
        if not country in self.free_shippings:
            self.calculate_prices(country)

        return self.free_shippings[country]

    def get_shipping_discounts(self, country):
        if not country in self.shipping_discounts:
            self.calculate_prices(country)

        return self.shipping_discounts[country]

    def get_shipping_prices(self, country):
        """
        Calculates the shipping price for a given country.

        @param country: country the product will be shipped to
        @return: tuple containing prices for single product shipping and shipping with another product
        """
        if not country in self.shipping_prices:
            self.calculate_prices(country)

        return self.shipping_prices[country]

    def calculate_prices(self, country):
        """
        Calculate shipping price, shipping discount and set a flag if the product qualifies for
        free shipping

        @param country:
        @return: None
        """
        rule_price = None
        rule_price_extra = None

        for current_rule in self.shipping_profile.shipping_rules.all():
            if country in current_rule.countries.all():
                rule_price = current_rule.rule_price
                rule_price_extra = current_rule.rule_price_extra
                break

        # no country found, use rest of the world
        if not rule_price or not rule_price_extra:
            rule_price = self.shipping_profile.others_price
            rule_price_extra = self.shipping_profile.others_price_extra

        self.shipping_prices[country] = rule_price, rule_price_extra

        #
        # check for free shipping
        #

        # set default values
        self.shipping_discounts[country] = (
            Money(amount="0", currency=purchase_settings.DEFAULT_CURRENCY),
            Money(amount="0", currency=purchase_settings.DEFAULT_CURRENCY)
        )
        self.free_shippings[country] = False

        free_shippings = FreeShipping.objects.filter(shipping_to=country)
        if rule_price and rule_price_extra:
            if rule_price.amount == 0:
                self.free_shippings[country] = True
            elif free_shippings:
                free_shipping = free_shippings[0]
                discount_amount = self.price.amount * free_shipping.percent_discount

                if rule_price < discount_amount:
                    self.shipping_discounts[country] = rule_price, rule_price_extra
                    self.free_shippings[country] = True

    def get_price_budget(self, country):
        """
        Calculate the price budget for Google AdWords.
        At the moment it is 20% of the product's price including shipping.

        :param country: Country instance
        :return:
        """
        shipping_price, shipping_price_extra = self.get_shipping_prices(country)
        price_budget = (self.price.amount + shipping_price) * Decimal(0.2)

        return price_budget

    def get_price_instance(self):
        """
        TODO: This would need thought for multi-currency environment.
        """
        for price in self.prices.all():
            return price
        # Making sure templates never error out because of no price instances
        # During product creation, all products will have prices.
        return Price(
            product=self, amount=Money(
                amount="0", currency=purchase_settings.DEFAULT_CURRENCY))

    @property
    def posted_in_days(self):
        return 2

    @property
    def delivery_days(self):
        return 6

    @property
    def best_love_lists(self):
        return self.love_lists.order_by('-promoted')

    @property
    def num_hearts(self):
        return self.love_lists.count()

    @property
    def images(self):
        return self.product_images.all()

    @property
    def image(self):
        return self.primary_image

    def mixpanel_record(self):
        record = {
            'Publish Status': self.get_status_display(),
            'Title': self.title,
            'Description': self.description,
            'Main Category': self.primary_category.seo_title,
            'Product Causes': [x.title for x in self.causes.all()],
            'Photos': int(self.product_images.count()),
            'Main Colours': [x.title for x in self.colors.all()],
            'Keywords': [x.title for x in self.keywords.all()],
            'Ingredients': [x.title for x in self.ingredients.all()],
            'Eco Materials': [x.title for x in self.materials.all()],
            'Occasions': [x.title for x in self.occasions.all()],
            'Recipients': [x.title for x in self.recipients.all()],
            'Price': repr(self.price.amount),
            'Unlimited Stock': self.stock == 0,
            'Product Ships From': self.ships_from_country
        }
        if self.stock is not None:
            record['Number In Stock'] = repr(int(self.stock))
        if self.secondary_category:
            record['Secondary Category'] = self.secondary_category.seo_title
        return record
        #'Ships Worldwide': self.ships_worldwide()

    @property
    def primary_image(self):
        """
        Returns the primary image to show everywhere.

        TODO: Can add a boolean to ProductImage to store which image
        to use as primary.
        """
        try:
            images = self.images.order_by('-created')[:1]
            if len(images):
                return images[0]
        except IndexError:
            pass

        # Hack to make sure we serve a dummy image if none exist.
        return ProductImage(product=self, name='dummy')

    def get_shipping_rule_for_country(self, country):
        return self.shipping_profile.shipping_rules.filter(country=country)

    def is_out_of_stock(self):
        return self.stock == 0

    @property
    def certificates_by_cause(self):
        """
        Map of cause IDs and their certificates
        """
        output = {}
        for cert in self.certificates.all():
            cause_id = cert.cause_id
            if cause_id not in output:
                output[cause_id] = []
            output[cause_id].append(cert)
        return output

    def in_stock(self):
        if self.stock > 0 or self.stock is None:
            return True
        return False


def product_listed_handler(sender, instance, created, **kwargs):
    from actstream.models import Action

    if (created and instance.status == Product.PUBLISHED_LIVE) \
            or (not created
                and instance.var_cache['status'] != Product.PUBLISHED_LIVE
                and instance.status == Product.PUBLISHED_LIVE):
        """
        We do not repeat the same product going Published twice.
        So if a old product just goes from Unpublished to Published,
        then we simply delete old action, if any.
        """
        query = Action.objects.filter(
            actor_content_type=ContentType.objects.get_for_model(instance.stall.user),
            actor_object_id=instance.stall.user.id,
            verb='listed a new product on',
            target_content_type=ContentType.objects.get_for_model(instance.stall),
            target_object_id=instance.stall.id,
            action_object_content_type=ContentType.objects.get_for_model(instance),
            action_object_object_id=instance.id
        )
        occured_before = bool(query.count())
        if occured_before:
            query.delete()
        action.send(
            instance.stall.user,
            verb='listed a new product on',
            action_object=instance, target=instance.stall)
    elif (not created
        and instance.var_cache['status'] == Product.PUBLISHED_LIVE
        and instance.status != Product.PUBLISHED_LIVE):
        query = Action.objects.filter(
            actor_content_type=ContentType.objects.get_for_model(instance.stall.user),
            actor_object_id=instance.stall.user.id,
            verb='listed a new product on',
            target_content_type=ContentType.objects.get_for_model(instance.stall),
            target_object_id=instance.stall.id,
            action_object_content_type=ContentType.objects.get_for_model(instance),
            action_object_object_id=instance.id
        )
        occured_before = bool(query.count())
        if occured_before:
            query.delete()

post_save.connect(product_listed_handler, sender=Product, dispatch_uid="marketplace_models_product_listed_handler")


class ProductImage(models.Model):
    product = models.ForeignKey('Product', related_name='product_images')
    name = models.CharField(
        max_length=255, blank=True, default='', null=False)
    filename = models.CharField(
        max_length=255, blank=True, default='', null=False)
    image = ProductImageField(
        max_length=255,
        upload_to='product/',
        preview_size=(400, 533),
        blank=False,
        null=False)
    thumbnail = ProductImageThumbsField(
        max_length=255,
        upload_to='product/',
        sizes=(50, 70, 80, 95, 100, 105, 170, 228, 400),
        aspect_ratio=1,
        blank=True,
        null=True)
    slug = AutoSlugField(populate_from='name', allow_duplicates=True)
    data = JSONField(blank=True, default='', null=False)
    #is_primary = models.BooleanField(default=False)

    active = models.BooleanField(default=True)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)

    class Meta:
        ordering = ('created', )

    @property
    def valid_sizes(self):
        return [s[0] for s in self.thumbnail.field.sizes]

    def image_or_default(self, size=None):

        try:
            self.image and self.image.size
        except:
            # doesnt exist or not on fs
            return settings.STATIC_URL \
                + "images/product/%s/default.png" % size

        try:
            filesize = self.thumbnail.size
        except (OSError, ValueError):
            filesize = 0

        try:
            if not filesize:
                self.crop_thumbnail()

            if size is not None and int(size) in self.valid_sizes:
                return getattr(
                    self.thumbnail,
                    'url_%sx%s' % (size, size))
            return self.thumbnail.url
        except:
            # always return something, and never fail!
            pass
        return settings.STATIC_URL + "images/product/%s/default.png" % size

    @property
    def url(self):
        try:
            return self.image.url
        except ValueError:
            return settings.STATIC_URL + "images/product/default/default.png"

    @property
    def url_preview(self):
        return self.image.url_preview

    @property
    def url_50(self):
        return self.image_or_default(size='50')

    @property
    def url_70(self):
        return self.image_or_default(size='70')

    @property
    def url_80(self):
        return self.image_or_default(size='80')

    @property
    def url_95(self):
        return self.image_or_default(size='95')

    @property
    def url_100(self):
        return self.image_or_default(size='100')

    @property
    def url_105(self):
        return self.image_or_default(size='105')

    @property
    def url_170(self):
        return self.image_or_default(size='170')

    @property
    def url_228(self):
        return self.image_or_default(size='228')

    @property
    def url_400(self):
        return self.image_or_default(size='400')

    def crop_thumbnail(self):
        # TODO: fix .data to use PIL ordering for crop coords
        # update the thumbnails using the given co-ordinates
        if self.data.get('image_crop'):
            xl, xr, yt, yb = self.data.get('image_crop')
        else:
            xl, yt, xr, yb = calculate_auto_crop(self.image, 228)

        self.image.file.open()
        self.image.file.seek(0)
        cropped = self.image.read()

        upfile = SimpleUploadedFile(self.filename, cropped)

        self.thumbnail.save(self.filename, upfile, True, [xl, yt, xr, yb])


class ShippingProfile(models.Model):
    """
    A collection of shipping rules that a stallholder can assign
    to a product for sale
    """
    stall = models.ForeignKey('Stall', related_name='shipping_profile')
    title = models.CharField(max_length=200)
    slug = AutoSlugField(populate_from='title')

    shipping_country = models.ForeignKey(
        'Country', related_name='shipping_profile')

    shipping_postcode = models.CharField(
        max_length=20,
        null=True, blank=True)

    others_price = NullableMoneyField(
        max_digits=6, decimal_places=2,
        null=True, blank=True,
        default_currency=purchase_settings.DEFAULT_CURRENCY)

    others_price_extra = NullableMoneyField(
        max_digits=6, decimal_places=2,
        null=True, blank=True,
        default_currency=purchase_settings.DEFAULT_CURRENCY)

    others_delivery_time = models.IntegerField(
        _(u"Delivery takes between"),
        null=True, blank=True)
    others_delivery_time_max = models.IntegerField(
        null=True, blank=True)

    class Meta:
        unique_together = ('stall', 'title',)

    def __unicode__(self, *args, **kwargs):
        return self.title

    @property
    def rules(self):
        return ShippingRule.objects.filter(profile=self)

    def ships_to_country(self, country):
        if self.ships_worldwide():
            return True
        return len(Country.objects.filter(shipping_rules__profile=self,
                                          code=country.code)[:1]) > 0

    def ships_worldwide(self):
        return self.others_price is not None

    def to_json(self):
        result = {
            "shipping_country": self.shipping_country.to_json(),
            "rules": [r.to_json() for r in self.shipping_rules.all()]
        }
        if self.ships_worldwide():
            others_price_extra = None
            if self.others_price_extra:
                others_price_extra = self.others_price_extra.amount
            result.update({
                "ships_worldwide": True,
                "others_price": self.others_price.amount,
                "others_price_extra": others_price_extra,
            })
        else:
            result.update({
                "ships_worldwide": False,
            })
        default_country = self.get_default_country()
        if default_country:
            result["default_country_code"] = default_country.code
        else:
            result["default_country_code"] = None
        return result

    def get_default_country(self):
        countries = Country.objects.filter(
            shipping_rules__profile=self)
        if len(countries) == 0:
            return None
        for country in countries:
            if country.code == "GB":
                return country
        return countries[0]


class ShippingRule(models.Model):
    """
    A Shipping rule that a stallholder can assign to a shipping profile
    """
    profile = models.ForeignKey(
        'ShippingProfile',
        related_name='shipping_rules')

    countries = models.ManyToManyField(
        'Country',
        related_name='shipping_rules')

    rule_price = MoneyField(
        max_digits=6, decimal_places=2,
        null=False,
        default_currency=purchase_settings.DEFAULT_CURRENCY)

    rule_price_extra = MoneyField(
        max_digits=6, decimal_places=2,
        null=False,
        default_currency=purchase_settings.DEFAULT_CURRENCY)

    despatch_time = models.IntegerField(_(u"Dispatch takes"))
    delivery_time = models.IntegerField(_(u"Delivery takes between"))
    delivery_time_max = models.IntegerField()

    def to_json(self):
        return {
            "rule_price": float(self.rule_price.amount),
            "rule_price_extra": float(self.rule_price_extra.amount),
            "dispatch_time": self.despatch_time,
            "delivery_time": self.delivery_time,
            "delivery_time_max": self.delivery_time_max,
            "countries": [c.to_json() for c in self.countries.all()],
        }


class Country(models.Model):
    """
    A country that can be shipped to or from
    """
    code = models.CharField(
        max_length=10,
        unique=True)
    title = models.CharField(
        max_length=200,
        unique=True)

    def __unicode__(self, *args, **kwargs):
        return self.title

    def to_json(self):
        return {
            "id": self.id,
            "code": self.code,
            "title": self.title,
        }


class SuggestedCertificate(ProductAttributeBase):
    product = models.ForeignKey(
        Product,
        related_name='suggested_certificates')
    url = models.URLField()

    def __unicode__(self, *args, **kwargs):
        return self.title


class CurrencyExchangeRate(models.Model):
    """
    We run a cron to get currency exchange rates every hour.
    Using Open Exchange Rates as the data provider.
    The default base is USD in the free account, maybe we will later use GBP.
    Reference - http://lists.mysql.com/mysql/221541
    """
    base_currency = models.CharField(max_length=3, null=False, blank=False)
    currency = models.CharField(max_length=3, null=False, blank=False)
    date_time = models.DateTimeField()
    exchange_rate = models.DecimalField(max_digits=15, decimal_places=6)

    def __unicode__(self):
        return '%s(%s) - %f' % (self.currency, self.base_currency, self.exchange_rate)

    @property
    def last_run(self):
        pass

    @staticmethod
    def convert(amount, to_currency, from_currency='GBP'):
        """
        Currently we only have GBP as source currency.
        """
        if to_currency == from_currency:
            return amount
        amounts = CurrencyExchangeRate.amount_in_all_currencies(amount)
        return amounts[to_currency]

    @staticmethod
    def get_all_rates(base_currency='GBP'):
        """
        Currently we assume all base rates to be GBP and convert from there.
        """
        latest = CurrencyExchangeRate.objects.all().aggregate(Max('date_time'))
        # The following syntax will run only on Py 2.7+ or 3
        exchange_rates = {str(c.currency): float(c.exchange_rate) for c in CurrencyExchangeRate.objects.filter(date_time=latest['date_time__max'])}
        return exchange_rates

    @staticmethod
    def amount_in_all_currencies(amount, from_currency='GBP'):
        """
        Currently we assume from_currency (the base) as GBP.
        """
        exchange_rates = CurrencyExchangeRate.get_all_rates()
        amounts = {k: round((v * amount), 2) for k, v in exchange_rates.items()}
        return amounts


class StallStatusLog(models.Model):
    stall = models.ForeignKey('marketplace.Stall', related_name='status_log')
    renewal_tier = models.PositiveSmallIntegerField(default=2)
    is_suspended = models.BooleanField(default=False)
    reason_for_suspension = models.PositiveSmallIntegerField(choices=REASON_FOR_SUSPENSION,
        blank=True, null=True)
    updated_at = models.DateTimeField()


class StallSuspendProxy(Stall):
    class Meta:
        proxy = True
        verbose_name = 'Stall Suspension'
        verbose_name_plural = 'Stall Suspensions'


class StallCallNotes(models.Model):
    stall = models.ForeignKey('marketplace.stall', related_name='call_notes',
        verbose_name='Stall')
    notes = models.TextField(blank=True, null=True, verbose_name='Notes')
    created = models.DateTimeField(auto_now_add=True, editable=False)