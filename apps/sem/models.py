# coding=utf-8
from decimal import Decimal
from django.db import models
from money.Money import Money
from money.contrib.django.models.fields import MoneyField

from django.utils.translation import ugettext_lazy as _
from purchase import settings as purchase_settings


class ProductAdWords(models.Model):
    product = models.ForeignKey('marketplace.Product', related_name='product_adword')
    ad_group_id = models.CharField(max_length=30, null=False, blank=False)

    status = models.CharField(max_length=40, null=False, blank=False, default='ENABLED')
    campaign_id = models.CharField(max_length=30, null=True, blank=True)
    cost = models.PositiveIntegerField(
        _(u'Total Lifetime Cost'),
        null=True, blank=True)
    average_cpc = models.PositiveIntegerField(
        _(u'Average CPC'),
        null=True, blank=True)
    profit_banked = MoneyField(
        _(u'Profit Banked'), max_digits=6, decimal_places=2,
        null=True, blank=True,
        default_currency=purchase_settings.DEFAULT_CURRENCY)
    
    clicks = models.PositiveSmallIntegerField(null=True, blank=True)
    impressions = models.PositiveIntegerField(null=True, blank=True)

    # https://developers.google.com/adwords/api/docs/reference/v201306/AdGroupService.Stats#conversions
    conversions = models.PositiveSmallIntegerField(_('Conversions'), null=True, blank=True)

    # Total sales. If 1 click had 3 sales, then this value will be 3
    total_sales = models.PositiveSmallIntegerField(_('Total Sales'), null=True, blank=True, default=0)

    velocity = models.DecimalField(max_digits=4, decimal_places=2, default=.5)
    max_cpc = MoneyField(
        _(u'CPC Cost'), max_digits=4, decimal_places=2,
        default=0.0,
        default_currency=purchase_settings.DEFAULT_CURRENCY
    )

    datetime_added = models.DateTimeField(
        _('When was this added'),
        auto_now_add=True,
        editable=False
    )
    datetime_updated = models.DateTimeField(
        _('When last updated'),
        auto_now=True,
        editable=False
    )

    class Meta:
        unique_together = ('product', 'ad_group_id')
        verbose_name_plural = 'Product AdWord Ads'
        ordering = ('-impressions', '-clicks')

    def __init__(self, *args, **kwargs):
        super(ProductAdWords, self).__init__(*args, **kwargs)
        self.changed_essentials = False

    def __unicode__(self):
        return str(self.product)

    @property
    def formatted_cost(self):
        return Money(float(self.cost) / float(1000000), currency=purchase_settings.DEFAULT_CURRENCY)

    def total_price_budget(self, country):
        base = self.product.get_price_budget(country)
        value = base + (base * self.total_sales)
        return value

    def update_adwords_data(self, country):
        max_cpc = self._get_max_cpc(country)

        if self.max_cpc.amount != max_cpc:
            self.changed_essentials = True
            self.max_cpc = max_cpc

        # set new status
        if self.product.stock == 0 or self.max_cpc.amount == Decimal("0.01"):
            new_status = "PAUSED"
        else:
            new_status = "ENABLED"

        if self.status != new_status:
            self.changed_essentials = True
            self.status = new_status

    def _get_max_cpc(self, country):
        value = self.formatted_cost / self.total_price_budget(country)

        if 0 <= value <= .5:
            max_cpc = Decimal("1")
        elif 0.5 < value <= .75:
            max_cpc = Decimal("0.5")
        elif .75 < value <= 1:
            max_cpc = Decimal("0.25")
        else:
            max_cpc = Decimal("0.01")

        return max_cpc


class ActiveCampaignId(models.Model):
    campaign = models.CharField(max_length=30)

    def __unicode__(self):
        return "<ActiveCampaignId: %s>" % self.campaign