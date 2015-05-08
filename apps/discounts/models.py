from decimal import Decimal, ROUND_DOWN

from django.core.exceptions import ValidationError
from django.db import models

from django.utils import timezone


# This is no longer used but remains here for posterity
class PLACampaign(models.Model):

    countries = models.ManyToManyField("marketplace.Country",
                                       related_name="pla_campaigns")
    products = models.ManyToManyField("marketplace.Product",
                                      related_name="pla_campaigns")
    utm_source = models.CharField(max_length=127)
    utm_medium = models.CharField(max_length=127)
    utm_campaign = models.CharField(max_length=127)

    def __unicode__(self):
        return unicode(self.utm_campaign)

    class Meta:
        verbose_name = "UTM URL for XML Feed"
        verbose_name_plural = "UTM URLs for XML Feed"

    def __iter__(self):
        # Used for easy conversion into a dict
        yield ("utm_source", self.utm_source)
        yield ("utm_medium", self.utm_medium)
        yield ("utm_campaign", self.utm_campaign)


class CurebitSite(models.Model):

    slug = models.SlugField(unique=True)

    def __unicode__(self):
        return unicode(self.slug)


class UTMCode(models.Model):

    code = models.CharField(unique=True, max_length=127)
    site = models.ForeignKey(CurebitSite, related_name="discounts")

    def __unicode__(self):
        return u"'{}' on {}".format(self.code, self.site)

    class Meta:
        verbose_name = "UTM code for Curebit site"
        verbose_name_plural = "UTM codes for Curebit sites"


class DiscountManager(models.Manager):

    def active(self):
        return self.all().filter(
            models.Q(expires=None) | models.Q(expires__gte=timezone.now()))


class Discount(models.Model):

    code = models.CharField(max_length=100)
    percent_discount = models.SmallIntegerField(default=0)
    price_discount = models.DecimalField(max_digits=5, decimal_places=2,
                                         default=0)
    expires = models.DateTimeField(blank=True, null=True)

    objects = DiscountManager()

    def clean(self):
        if self.percent_discount and self.price_discount:
            raise ValidationError(
                "Please set only percent discount or price discount, not both")
        elif self.percent_discount == 0 and self.price_discount == 0:
            raise ValidationError("Please set a discount")

    def __unicode__(self):
        discount = (u"\u00A3{}".format(self.price_discount)
                    if self.price_discount
                    else u"{}%".format(self.percent_discount))
        return u"{}: {} discount".format(self.code, discount)

    def calculate(self, original_price):
        """Calculate discount from original price"""
        if self.percent_discount:
            discount = (original_price / 100) * self.percent_discount
            return discount.quantize(Decimal("0.01"), rounding=ROUND_DOWN)
        return self.price_discount

    class Meta:
        verbose_name = "Discount coupon codes"
        verbose_name_plural = "Discount coupon codes"


class FreeShipping(models.Model):
    """
    Class for shipping discounts for certain countries.
    Conditions for free shipping:

    1) A product needs to match the given destination country.
    2) A product's shipping cost need to be higher than (product price - ecomarket_share)
       otherwise ecomarket would make no profit

    The shipping_from field got deactivated, because it does not matter where the product comes from
    as long as ecomarket still makes profit.

    For more info see: http://bit.ly/18JuGZi (Trello Card)
    """
    description = models.CharField(max_length=255)
    # shipping_from = models.ManyToManyField(
    #     "marketplace.Country",
    #     related_name='shipping_from',
    #     verbose_name='origin country',
    # )
    shipping_to = models.ManyToManyField(
        "marketplace.Country",
        related_name='shipping_to',
        verbose_name='destination country',
    )
    percent_discount = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=10.0,
        help_text="The shipping cost of a product needs to be higher than"
                  " this amount to qualify for free shipping (10% = 0.1)!"
    )
    date_start = models.DateTimeField(
        blank=True,
        null=True,
        help_text="The day the free shipping period starts",
    )
    date_end = models.DateTimeField(
        blank=True,
        null=True,
        help_text="The day the free shipping period ends",
    )
