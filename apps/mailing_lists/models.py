# coding=utf-8
import datetime, pytz

from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.db.models import Q
from django.db.models.signals import post_save, post_delete

from django.contrib.auth.models import User

from south.modelsinspector import add_introspection_rules

from accounts.models import UserProfile, EmailNotification
from lovelists.models import LoveList
from marketplace.models import Stall, Category, Product, StallStatusLog
import purchase.models  # required for user.orders
from social_network.models import UserFollow

from mailing_lists.batch import BatchJobAPI
from mailing_lists.constants import LeadSources, MemberTypes, BatchStatus
from mailing_lists.managers import MailingListManager


class EditableAutoNowAddDateTimeField(models.DateTimeField):

    # It is impossible to have auto_now_add=True and editable=True on a
    # normal DateTimeField

    def __init__(self, auto_now_add=True, editable=True, **kwargs):
        super(EditableAutoNowAddDateTimeField, self).__init__(
            editable=editable, **kwargs)
        self.auto_now_add = auto_now_add

add_introspection_rules(
    [], ["^apps\.mailing_lists\.models\.EditableAutoNowAddDateTimeField",
    "^mailing_lists\.models\.EditableAutoNowAddDateTimeField"])


def get_client_ip(request):
    # Taken from
    # http://stackoverflow.com/questions/4581789/
    # how-do-i-get-user-ip-address-in-django
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


class MailingListSignup(models.Model):
    class Meta:
        verbose_name_plural = 'Email Leads'

    LEAD_SOURCES = (
        (LeadSources.GATE_MODAL, 'Homepage Modal'),
        (LeadSources.BLOG_POPUP, 'Blog Popup'),
        (LeadSources.DATA_COLLECTION, 'Data collection'),
        (LeadSources.GOOGLE_CPC, 'Google CPC'),
        (LeadSources.REGISTER_PAGE, 'Register Page'),
        (LeadSources.PRODUCT_GIVEAWAY, 'Product Giveaway'),
    )
    MEMBER_TYPES = (
        (MemberTypes.NORMAL, 'Normal user'),
        (MemberTypes.SELLER, 'Seller'),
    )
    email_address = models.EmailField(unique=True, max_length=255)
    user = models.ForeignKey(User, blank=True, null=True)
    first_name = models.CharField(blank=True, null=True, max_length=255)
    last_name = models.CharField(blank=True, null=True, max_length=255)
    company_name = models.CharField(blank=True, null=True, max_length=255)
    category = models.ForeignKey(
        Category, blank=True, null=True,
        choices=Category.objects.get_toplevel().values_list("id", "name"))
    telephone_number = models.CharField(blank=True, null=True, max_length=255)
    country = models.ForeignKey("marketplace.Country", blank=True, null=True)
    source = models.CharField(max_length=2, choices=LEAD_SOURCES,
                              default=LeadSources.REGISTER_PAGE)
    member_type = models.SmallIntegerField(choices=MEMBER_TYPES, blank=True,
                                           null=True)
    is_seller_lead = models.BooleanField(default=False)
    date_added = EditableAutoNowAddDateTimeField()
    marketing_optin = models.BooleanField(default=True)

    # This is currently unused, but the data will later be used to set currency
    # based on a user's estimated address.
    ip_address = models.IPAddressField(blank=True, null=True)

    objects = MailingListManager()

    def __unicode__(self):
        return unicode(self.email_address)

    def set_ip_address(self, request):
        self.ip_address = get_client_ip(request)

    # Data retrieval methods

    def export(self):
        """
        Prepares data for sailthru export.

        :return:
        """
        export_vars = {
            "email": self.get_email_address(),
            "first_name": self.get_first_name(),
            "last_name": self.get_last_name(),
            "user_profile_has_avatar": self.get_user_profile_has_avatar(),
            "business_name": self.company_name,
            "city_or_town": self.get_user_profile_city_or_town(),
            "email_referrer": None,  # This to come later
            "lists": self.get_lists(),
            "login_date": self.get_user_login_date(),
            "phone": self.get_phone_number(),
            "signup_source_data_collection": (
                self.source == LeadSources.DATA_COLLECTION),
            "signup_source_homepage_modal": (
                self.source == LeadSources.GATE_MODAL),
            "signup_source_blog_popup": (
                self.source == LeadSources.BLOG_POPUP),
            "signup_source_google_cpc": (
                self.source == LeadSources.GOOGLE_CPC),
            "signup_source_register_page": (
                self.source == LeadSources.REGISTER_PAGE),
            "signup_source_product_giveaway": (
                self.source == LeadSources.PRODUCT_GIVEAWAY),
            "is_seller_lead": self.is_seller_lead,
            "birthday": self.get_user_profile_dob(),
            "is_user": self.get_is_user(),
            "is_seller": self.get_is_seller(),
            "gender": self.get_user_profile_gender(),
            "country": self.get_country(),
            "stall_title": self.get_stall_title(),
            "stall_short_description": self.get_stall_short_description(),
            "stall_full_description": self.get_stall_full_description(),
            "stall_paypal_email": self.get_stall_paypal_email(),
            "username": self.get_user_username(),
            "user_purchased_orders": self.get_user_purchased_orders(),
            "stall_product_count": self.get_stall_product_count(),
            "stall_active_product_count": (
                self.get_stall_active_product_count()),
            "stall_out_of_stock_product_count": (
                self.get_stall_out_of_stock_product_count()),
            "stall_orders_sold": self.get_stall_orders_sold(),
            "user_lovelist_count": self.get_user_lovelist_count(),
            "user_products_loved_count": self.get_user_products_loved_count(),
            "user_following_count": self.get_user_following_count(),
            "user_followers_count": self.get_user_followers_count(),
            "user_lifetime_value": self.get_user_lifetime_value(),
            "stall_total_gmv": self.get_stall_total_gmv(),
            "signup_date": self.get_signup_date(),
            'users_detected_country': self.get_users_detected_country(),
            'users_currency': self.get_users_currency(),
        }
        if self.get_is_seller():
            stall = self.get_stall()
            if stall.is_suspended:
                export_vars['stall_is_suspended'] = True
                export_vars['stall_latest_suspension_reason'] = stall.reason_for_suspension
            else:
                export_vars['stall_is_suspended'] = False
                export_vars['stall_latest_suspension_reason'] = False
            export_vars['stall_total_suspensions'] = StallStatusLog.objects.filter(stall=stall, is_suspended=True).count()
            export_vars['stall_renewal_tier'] = stall.renewal_tier
            export_vars['stall_is_active'] = stall.is_active
            export_vars['stall_days_left_to_stock_check'] = stall.days_to_next_stockcheck
            export_vars['stall_has_stock_checked_ever'] = stall.has_stock_checked_ever

        return dict((key, value) for key, value in export_vars.items()
                    if value is not None)

    def get_users_currency(self):
        if self.user:
            currency = self.user.get_profile().preferred_currency
            if currency in ['', None]:
                currency = 'GBP'
            return currency

    def get_users_detected_country(self):
        if self.user:
            return self.user.get_profile().detected_country

    def get_email_address(self):
        if self.user and self.user.email:
            return self.user.email
        return self.email_address

    def get_first_name(self):
        if self.user and self.user.first_name:
            return self.user.first_name
        return self.first_name

    def get_last_name(self):
        if self.user and self.user.last_name:
            return self.user.last_name
        return self.last_name

    def get_user_profile_gender(self):
        if self.user:
            return self.user.get_profile().gender
        return None

    def get_stall(self):
        if not self.user:
            return None
        try:
            return self.user.stall
        except ObjectDoesNotExist:
            return None

    def get_stall_title(self):
        stall = self.get_stall()
        if stall and stall.title:
            return stall.title
        return None

    def get_signup_date(self):
        if self.user:
            return self.user.date_joined.isoformat()
        return self.date_added.isoformat()

    def get_user_login_date(self):
        if self.user:
            return self.user.last_login.isoformat()
        return None

    def get_phone_number(self):
        number = None
        if self.user:
            try:
                stall = self.user.stall
            except ObjectDoesNotExist:
                stall = None
            if getattr(stall, "phone_landline", None):
                number = stall.phone_landline
            elif getattr(stall, "phone_mobile", None):
                number = stall.phone_mobile
        if number is None:
            number = self.telephone_number
            if number is None or not number.startswith("+"):
                return number
        # Sailthru has a bug (from PHP) where our international phone numbers
        # are converted into integers, thus corrupting them. Adding a space
        # after the + supposedly works around this.
        return "+ {}".format(number[1:])

    def get_country(self):
        if self.user:
            profile = self.user.get_profile()
            try:
                return profile.country.code
            except Exception:
                pass
        return None

    def get_user_profile_dob(self):
        if self.user:
            profile = self.user.get_profile()
            if profile.birthday:
                return profile.birthday.strftime('%Y-%m-%d')
        return None

    def get_user_profile_city_or_town(self):
        if self.user:
            profile = self.user.get_profile()
            if profile.city:
                return profile.city
        return None

    def get_stall_short_description(self):
        stall = self.get_stall()
        if stall:
            return stall.description_short
        return None

    def get_stall_full_description(self):
        stall = self.get_stall()
        if stall:
            return stall.description_full
        return None

    def get_stall_paypal_email(self):
        stall = self.get_stall()
        if stall and stall.paypal_email:
            return stall.paypal_email
        return None

    def get_user_username(self):
        if self.user:
            return self.user.username
        return None

    def get_user_purchased_orders(self):
        if self.user:
            orders = self.user.orders
            return orders.filter(
                Q(is_joomla_order=True) | ~Q(payment=None)).count()
        return None

    def get_user_lifetime_value(self):
        if self.user:
            profile = self.user.get_profile()
            if profile:
                return profile.total_gmv.amount

    def get_stall_total_gmv(self):
        stall = self.get_stall()
        if stall:
            return stall.total_gmv.amount

    def get_stall_product_count(self):
        stall = self.get_stall()
        if stall:
            return stall.products.count()
        return None

    def get_stall_active_product_count(self):
        stall = self.get_stall()
        if stall:
            # 'active' only excludes deleted, not unpublished items
            return stall.products.filter(status=Product.PUBLISHED_LIVE).count()
        return None

    def get_stall_out_of_stock_product_count(self):
        stall = self.get_stall()
        if stall:
            return stall.products.sold_out().count()
        return None

    def get_stall_orders_sold(self):
        stall = self.get_stall()
        if stall:
            return (stall.orders.exclude(payment=None).count()
                    + stall.orders.filter(is_joomla_order=True).count())
        return None

    def get_user_lovelist_count(self):
        if self.user:
            # FIXME: We were using self.user.love_lists here but for some
            # reason this was raising AttributeError. Find out why.
            return LoveList.objects.filter(user=self.user).count()
        return None

    def get_user_products_loved_count(self):
        if self.user:
            products = set()
            for love_list in self.user.love_lists.all():
                for product in love_list.products.all():
                    products.add(product)
            return len(products)
        return None

    def get_user_following_count(self):
        if self.user:
            return UserFollow.user_follow(self.user).count()
        return None

    def get_user_followers_count(self):
        if self.user:
            return UserFollow.user_following(self.user).count()
        return None

    def get_user_profile_has_avatar(self):
        if self.user:
            avatar = self.user.get_profile().avatar
            hasfile = (avatar is not None and avatar.name not in ["", None])
            if hasfile:
                try:
                    return avatar.size > 0
                except:
                    pass
        return False

    def get_is_user(self):
        return self.user is not None

    def get_is_seller(self):
        return self.get_stall() is not None

    def _get_notification_data(self, name):
        if self.user is None:
            if name in ['products_you_might_like', 'site_updates_features',
                        'blogs_you_might_like']:
                return self.marketing_optin
            return None
        return getattr(self.user.email_notification, name)

    def get_lists(self):
        lists = {}
        list_names = ["follower_notifications", "stall_owner_tips",
                      "site_updates_features", "blogs_you_might_like",
                      "products_you_might_like", "product_discounts"]
        for name in list_names:
            lists[name] = self._get_notification_data(name)
        return lists


def _update_signup_normal(ml):
    ml.member_type = MemberTypes.NORMAL
    ml.save()


def _update_signup_seller(ml):
    ml.member_type = MemberTypes.SELLER
    ml.is_seller_lead = False
    ml.save()


def update_signup(sender, instance, **kwargs):
    if sender is User:
        user = instance
        mls = MailingListSignup.objects.filter(user=user)
        if mls.exists():
            # MailingListSignup for user already exists - update it
            for ml in mls:
                try:
                    user.stall
                except ObjectDoesNotExist:
                    _update_signup_normal(ml)
                else:
                    _update_signup_seller(ml)
            return

    elif sender in (UserProfile, Stall, EmailNotification):
        user = instance.user
        mls = MailingListSignup.objects.filter(user=user)
        if mls.exists() and sender is Stall:
            # User is a seller and MailingListSignup already exists
            for ml in mls:
                _update_signup_seller(ml)
            return

post_save.connect(update_signup, sender=User)
post_save.connect(update_signup, sender=UserProfile)
post_save.connect(update_signup, sender=Stall)
post_save.connect(update_signup, sender=EmailNotification)


class BatchJob(models.Model):

    STATUSES = [
        (BatchStatus.NEW, "New"),
        (BatchStatus.IN_PROGRESS, "In Progress"),
        (BatchStatus.COMPLETED, "Completed"),
        (BatchStatus.FAILED, "Failed"),
    ]

    created = models.ManyToManyField(MailingListSignup, related_name="+b1")
    updated = models.ManyToManyField(MailingListSignup, related_name="+b2")

    remote_id = models.CharField(max_length=24, null=True, blank=True)
    status = models.SmallIntegerField(choices=STATUSES,
                                      default=BatchStatus.NEW)
    submitted = models.DateTimeField(null=True, blank=True)
    completed = models.DateTimeField(null=True, blank=True)

    def get_data(self):
        created = self.created.all()
        updated = self.updated.all()
        deleted = self.deleted.all()

        def is_deleted(mls):
            return deleted.filter(email_address=mls.email_address).count() > 0

        for mls in created:
            if is_deleted(mls):
                # No point in creating, then immediately deleting the same item
                continue
            yield mls.export()
        for mls in updated:
            if mls in created or is_deleted(mls):
                continue
            yield mls.export()
        for deleted_email in deleted:
            filtered = created.filter(
                email_address=deleted_email.email_address)
            is_created = (filtered.count())
            if is_created:
                continue
            yield {
                "email": deleted_email.email_address,
                "subscribe": False,
            }

    def get_api(self, provider):
        attr_name = "{}_api".format(provider)
        if not hasattr(self, attr_name):
            setattr(self, attr_name, BatchJobAPI(provider))
        return getattr(self, attr_name)

    def submit(self, provider, json_output=None):
        self.get_api(provider).submit_job(self, json_output=json_output)

    def check_status(self, provider):
        return self.get_api(provider).check_status(self)

    def __unicode__(self):
        data = [u"status='{}'".format(self.get_status_display())]
        if self.created.count():
            data.append(u"created_count={0}".format(self.created.count()))
        if self.updated.count():
            data.append(u"updated_count={0}".format(self.updated.count()))
        if self.deleted.count():
            data.append(u"deleted_count={0}".format(self.deleted.count()))
        return u", ".join(data)


class DeletedEmail(models.Model):

    job = models.ForeignKey(BatchJob, related_name="deleted")
    email_address = models.EmailField(unique=True, max_length=255)

    def __unicode__(self):
        return unicode(self.email_address)


def update_batch_job(sender, instance, created=False, deleted=False, **kwargs):
    jobs = BatchJob.objects.filter(status=BatchStatus.NEW)
    try:
        batch = jobs.get()
    except BatchJob.DoesNotExist:
        batch = jobs.create()
    except BatchJob.MultipleObjectsReturned:
        # This should never happen, but it pays to be safe...
        batch = jobs[0]
    if created:
        batch.created.add(instance)
    elif deleted:
        try:
            batch.deleted.create(email_address=instance.email_address)
        except:
            pass
    else:
        batch.updated.add(instance)

post_save.connect(update_batch_job, sender=MailingListSignup)


def update_batch_job_deleted(*args, **kwargs):
    # For some reason functools.partial is silently failing with signals
    return update_batch_job(*args, deleted=True, **kwargs)


post_delete.connect(update_batch_job_deleted,
                    sender=MailingListSignup)
