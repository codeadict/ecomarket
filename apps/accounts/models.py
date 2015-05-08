from __future__ import absolute_import

import datetime
import hashlib
import logging
import random
from datetime import date

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.core.validators import MaxLengthValidator
from django.db import models
from django.db.models import Q
from django.db.models.signals import post_save

from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.utils.timezone import now as datetime_now, utc as tz_utc
from django.utils.translation import ugettext_lazy as _
from django.core.cache import cache

from annoying.fields import AutoOneToOneField
from django_extensions.db.fields.json import JSONField
from money.Money import Money  # for total_gmv calculation

from image_crop.fields import ImageWithCroppedThumbsField
from image_crop.utils import normalize_filename, idnormalizer
from marketplace import CURRENCY_CHOICES
from social_network.models import UserFollow

from purchase.settings import DEFAULT_CURRENCY

from accounts.managers import UserProfileManager

logger = logging.getLogger(__name__)


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.get_or_create(user=instance)
post_save.connect(create_user_profile, sender=User)


class UserProfile(models.Model):
    ACTIVATED = 'ACTIVATED'

    GENDER_MALE = 'm'
    GENDER_FEMALE = 'f'
    GENDER_CHOICES = (
        (GENDER_MALE, "Male"),
        (GENDER_FEMALE, "Female"),
    )
    avatar = ImageWithCroppedThumbsField(
        upload_to=lambda instance, fn: 'avatar/%s/%s' % (
            idnormalizer.normalize(
                instance.user.username),
            normalize_filename(fn)),
        aspect_ratio=1,
        sizes=(30, 50, 60, 80, 100, 228),
        blank=True, null=True)
    user = models.OneToOneField(User, related_name='user_profile')
    gender = models.CharField(
        max_length=1, choices=GENDER_CHOICES, default='')
    birthday = models.DateField(blank=True, null=True)
    about_me = models.TextField(
        default='', validators=[MaxLengthValidator(450)])

    send_newsletters = models.BooleanField(default=True)
    activation_key = models.CharField(max_length=40, default='')
    activation_key_date = models.DateTimeField(auto_now_add=True)
    last_activities_update = models.DateTimeField(null=True)

    # Stall owner details
    address_1 = models.CharField(
        max_length=255, default='', verbose_name='Address line 1')
    address_2 = models.CharField(
        max_length=255, default='', verbose_name='Address line 2')
    city = models.CharField(
        max_length=100, default='', verbose_name='City or town')
    state = models.CharField(
        max_length=100, default='', verbose_name='County or state')
    zipcode = models.CharField(
        max_length=20, default='', verbose_name='Post Code or zip')
    country = models.ForeignKey("marketplace.Country")
    social_auth = models.CharField(
        max_length=32, null=True, default='',
        verbose_name='Social Auth Partner')

    # additional json properties, used to store avatar crop data
    data = JSONField(blank=True, default='', null=False)

    # Preferred Currency - user sets their preference manually and we save to this field.
    # If this data is not available then we detect on the fly.
    preferred_currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='')

    # Detected Country - this comes from CloudFlare
    detected_country = models.CharField(max_length=2, blank=True, null=True)

    # This is here to make sure no discounts are used more than once
    used_discounts = models.ManyToManyField("discounts.Discount")

    # When did this user last check their activities page
    activities_last_checked_at = models.DateTimeField(blank=True, null=True)

    phone_number = models.CharField(
        max_length=16,
        blank=True,
        null=True,
    )

    objects = UserProfileManager()

    def __unicode__(self):
        return unicode(self.user.username)

    def get_absolute_url(self):
        return reverse("public_profile", args=[self.user.username])

    @property
    def age(self):
        """
        Persons age in years, or None if no birthday specified
        """
        if self.birthday:
            today = date.today()
            age = today - self.birthday
            return int(age.days / 365.25)

    @property
    def full_name(self):
        return self.user.get_full_name()

    @property
    def is_seller(self):
        """ Returns True, if the user is a seller. """
        try:
            if self.user.stall:
                return True
        except:
            pass
        return False

    @property
    def has_facebook_auth(self):
        try:
            self.user.social_auth.get(provider="facebook")
        except ObjectDoesNotExist:
            return False
        return True

    @property
    def valid_sizes(self):
        return [s[0] for s in self.avatar.field.sizes]

    def avatar_or_default(self, size):
        try:
            avatar_size = self.avatar.size
        except:
            avatar_size = 0

        if self.avatar and avatar_size:
            if int(size) in self.valid_sizes:
                return getattr(
                    self.avatar, 'url_%sx%s' % (size, size))
            return self.avatar.url
        return settings.STATIC_URL + "images/avatar/%s/avatar.png" % size

    # TODO: replace these with __getattr__ slot
    @property
    def avatar_30(self):
        return self.avatar_or_default(size='30')

    @property
    def avatar_50(self):
        return self.avatar_or_default(size='50')

    @property
    def avatar_80(self):
        return self.avatar_or_default(size='80')

    @property
    def avatar_100(self):
        return self.avatar_or_default(size='100')

    @property
    def avatar_228(self):
        return self.avatar_or_default(size='228')

    # Activation process
    # ==================
    def is_activated(self):
        return (self.activation_key == self.ACTIVATED)

    def activation_key_expired(self):
        """ Checks to see if your activation key has expired. """
        expiration_date = datetime.timedelta(
            days=settings.ACTIVATION_EXPIRATION_DAYS
        )
        return self.is_activated() or \
            (self.activation_key_date + expiration_date <= datetime_now())

    def generate_activation_key(self):
        """ Creates an activation key for the user. """
        logger.info('Started generating activation key')
        salt = hashlib.sha1(str(random.random())).hexdigest()[:5]
        username = self.user.username
        activation_key = hashlib.sha1(salt + username).hexdigest()
        logger.info('Generated activation key {0} for {1}'.format(
            activation_key,
            self.user.username))
        return activation_key

    def generate_activation_key_and_save(self):
        self.activation_key = self.generate_activation_key()
        self.activation_key_date = datetime_now()
        self.save()

    @property
    def repeat_purchaser(self):
        paid_orders = self.user.orders.filter(Q(is_joomla_order=True) | ~Q(payment=None))
        return paid_orders.count() > 1

    @property
    def total_gmv(self):
        """Total Gross Merchandise Value of user purchases
        NOTE: This is the customer livetime value!!!
        See also: Stall.total_gmv
        """
        orders = self.user.orders
        paid_orders = orders.filter(Q(is_joomla_order=True) | ~Q(payment=None))
        return Money(0, DEFAULT_CURRENCY) + sum(
                [obj.total() for obj in paid_orders])

    @property
    def activities_count(self, date_since=None):
        """
        Obtains the activities count of an user and its follow list.
        :return:Returns an integer representing the quantity of
        actions performed by an user and its follow list.
        """
        cache_key = settings.CACHE_KEY_ACTIVITIES_COUNT % self.user.id
        activities = cache.get(cache_key)
        if activities:
            return activities

        date_since = (date_since or self.activities_last_checked_at)
        if date_since is None:
            # Must use a datetime in a datetime field, or else Django complains
            date_since = datetime.datetime.combine(datetime.date.today(),
                                                   datetime.time.min)
            date_since = date_since.replace(tzinfo=tz_utc)
        user_follows = list(UserFollow.objects.filter(user=self.user))
        profile_follows_ids = [follow.target.id for follow in user_follows]

        from actstream.models import Action
        content_type = ContentType.objects.get_for_model(self.user)
        activities = Action.objects.filter(
            Q(public=True),
            Q(timestamp__gte=date_since),
            Q(actor_object_id__in=profile_follows_ids) | Q(target_object_id__in=profile_follows_ids,
                                                            target_content_type_id=content_type.id)
        ).exclude(actor_object_id=self.user.id).count()

        cache.set(cache_key, activities, 60)
        return activities

    @property
    def stall(self):
        """
        Obtains the stall of the user, None if no stall was found for that user
        :return:Returns the Stall object or the user
        """
        try:
            return self.user.stall
        except ObjectDoesNotExist:
            pass

    def save(self, *args, **kwargs):
        if not self.last_activities_update:
            self.last_profile_update = datetime.datetime.now()
        super(UserProfile, self).save(*args, **kwargs)

    @property
    def recently_delivered_address(self):
        if self.user.orders:
            try:
                return self.user.orders.order_by('-created')[0].address
            except IndexError:
                return None
        else:
            return None


class EmailNotification(models.Model):
    user = AutoOneToOneField(User, related_name='email_notification')
    site_updates_features = models.BooleanField(
        _('site updates & features'), blank=True, default=True, null=False)
    stall_owner_tips = models.BooleanField(
        _('stall owner tips'), blank=True, default=True, null=False)
    follower_notifications = models.BooleanField(
        _('follower notifications'), blank=True, default=True, null=False)
    products_you_might_like = models.BooleanField(
        _('products you might like'), blank=True, default=True, null=False)
    private_messages = models.BooleanField(
        _('private messages'), blank=True, default=True, null=False)
    orders = models.BooleanField(
        _('orders'), blank=True, default=True, null=False)
    customer_reviews = models.BooleanField(
        _('customer reviews'), blank=True, default=True, null=False)
    share_orders_in_activity_feed = models.BooleanField(
        _('share orders in activity feed'), blank=True, default=True, null=False)
    blogs_you_might_like = models.BooleanField(
        _('blogs you might like'), blank=True, default=True, null=False)
    product_discounts = models.BooleanField(
        _('product discounts'), blank=True, default=True, null=False)


class Privacy(models.Model):
    user = AutoOneToOneField(User, related_name='privacy')
    profile_public = models.BooleanField(
        _('make my profile public'), blank=True, default=True, null=False)
    share_purchases_in_activity = models.BooleanField(
        _('share purchases in activity feed'),
        blank=True, default=True, null=False)
    love_list_public = models.BooleanField(
        _('make my love lists public by default'),
        blank=True, default=True, null=False)
    share_love_list_in_activity = models.BooleanField(
        _('share love lists in activity feed'),
        blank=True, default=True, null=False)


class ShippingAddress(models.Model):
    user = models.ForeignKey(User, related_name='addresses')
    name = models.CharField(_(u'Recipient name'), max_length=255, default='')
    line1 = models.CharField(_(u'Address line 1'), max_length=255)
    line2 = models.CharField(_(u'Address line 2'), max_length=255, blank=True)
    city = models.CharField(_(u'Town or city'), max_length=255)
    state = models.CharField(_(u'County or state'), max_length=50)
    country = models.ForeignKey("marketplace.Country", null=True)
    postal_code = models.CharField(_(u'Post code or zip'), max_length=15)
    created = models.DateField(auto_now_add=True, editable=False)
    updated = models.DateField(auto_now=True, editable=False)
    # is_active = models.Boolean
    # TODO: Use this instead of delete, since CartStall needs it.
    # type = models.ChoiceField()
    last_select_date_time = models.DateTimeField(blank=True, null=True, editable=False)

    class Meta:
        ordering = ('-created',)


class VideoType(models.Model):
    name = models.CharField(max_length=40)
    time_limit = models.PositiveSmallIntegerField(default=30)


class Video(models.Model):
    user = models.ForeignKey(User, related_name='videos')
    video_type = models.ForeignKey('accounts.VideoType')
    title = models.CharField(max_length=120, blank=True, null=True)

    # Sociagram related
    video_guid = models.CharField(max_length=40, blank=False, null=False)
    embed_url = models.CharField(max_length=120, blank=False, null=True)
    splash_url = models.CharField(max_length=120, blank=False, null=True)

    is_reference = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)