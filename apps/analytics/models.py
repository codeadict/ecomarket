# coding=utf-8
from django.db import models
from django.contrib.auth.models import User


class CampaignTrack(models.Model):
    """
    We track all the campaigns that a user may have come across.
    We send ONLY the first campaign's details to SailThru, and only ONCE
    """
    # The user field (strangely) has a default values 0.
    # was needed since South complained at migration.
    # This user feild was not-null earlier, we changed to null.
    user = models.ForeignKey(
        User,
        null=True, blank=True, editable=False,
        related_name='campaigns'
    )
    email_lead = models.ForeignKey(
        "mailing_lists.MailingListSignup",
        null=True,
        blank=True,
        related_name='campaigns',
        editable=False
    )
    # Eco Market Lifetime Cookie (separate from Django's own session cookie)
    cookie = models.ForeignKey('analytics.LifetimeTrack', null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    source = models.CharField(max_length=60, null=True, blank=True)
    name = models.CharField(max_length=200, null=False, blank=False)
    medium = models.CharField(max_length=60, null=True, blank=True)
    term = models.CharField(max_length=100, null=True, blank=True)
    content = models.CharField(max_length=60, null=True, blank=True)
    utmz = models.CharField(max_length=1000, null=False, blank=False)
    query_string = models.CharField(max_length=1000, null=True, blank=True)
    sent_to_sailthru = models.BooleanField(default=False, blank=False, null=False)

    class Meta:
        unique_together = ('user', 'name')

    def __unicode__(self):
        return u'%s - %s' % (self.user, self.name)


class AggregateData(models.Model):
    """
    We aggregate a bunch of data on a daily basis and store here,
    so that its easy to query and visualize such data.
    """
    created_at = models.DateTimeField(auto_now_add=True, null=False, blank=False)
    campaign = models.CharField(max_length=60, null=False, blank=False)
    
    # These are customers acquired only through this campaign
    daily_acquired = models.PositiveSmallIntegerField()

    # Everyday's cost to run this campaign, in GBP
    campaign_cost = models.FloatField()
    # Average cost to acquire each customer
    customer_acquistion_cost = models.FloatField()
    # Total number of Orders by Campaign users
    order_count = models.PositiveSmallIntegerField(default=0)
    # Everyday's total value of purchases made through this campaign, in GBP
    gross_merchant_value = models.FloatField()
    # Purchase worth - campaign cost, GBP
    revenue_after_commission = models.FloatField()

    class Meta:
        ordering = ('-created_at', )


STATUS_CHOICES = (
    (1, 'Visited'),
    (2, 'Acquired'),
    (4, 'Activated'),
    (8, 'Retained'),
    (16, 'Referred'),
    (32, 'Purchased'),
)


class LifetimeTrack(models.Model):
    cookie_key = models.CharField(max_length=60, blank=False, null=False, unique=True)
    user = models.ForeignKey(
        User,
        null=True, blank=True, editable=False,
        related_name='+'
    )
    email_lead = models.ForeignKey(
        "mailing_lists.MailingListSignup",
        null=True,
        blank=True,
        related_name='+',
        editable=False
    )
    status = models.PositiveSmallIntegerField(default=0, choices=STATUS_CHOICES)
    url_count = models.PositiveSmallIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True, null=False, blank=False)
    acquired_at = models.DateTimeField(null=True, blank=True)
    activated_at = models.DateTimeField(null=True, blank=True)
    actual_activated_at = models.DateTimeField(null=True, blank=True)
    retained_at = models.DateTimeField(null=True, blank=True)
    actual_retained_at = models.DateTimeField(null=True, blank=True)
    referred_at = models.DateTimeField(null=True, blank=True)
    actual_referred_at = models.DateTimeField(null=True, blank=True)
    purchased_at = models.DateTimeField(null=True, blank=True)


class ProductFormErrors(models.Model):
    stall = models.ForeignKey('marketplace.Stall')
    product = models.ForeignKey('marketplace.Product', blank=True, null=True)

    # Major kinds of errors tracked
    product_form_error = models.BooleanField(default=False)
    price_form_error = models.BooleanField(default=False)
    shipping_form_error = models.BooleanField(default=False)
    images_formset_error = models.BooleanField(default=False)

    # Individual errors tracked
    # Product form related
    description_error = models.BooleanField(default=False)
    recipients_error = models.BooleanField(default=False)
    title_error = models.BooleanField(default=False)
    colors_error = models.BooleanField(default=False)
    keywords_field_error = models.BooleanField(default=False)
    primary_category_error = models.BooleanField(default=False)
    shipping_profile_error = models.BooleanField(default=False)

    # Price form related
    amount_error = models.BooleanField(default=False)

    # A flag whether this product create/edit had errors
    had_error = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True, null=False, blank=False)

    class Meta:
        verbose_name_plural = 'Product Form Errors'