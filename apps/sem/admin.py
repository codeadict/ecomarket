from django.contrib import admin

from apps.sem.models import ProductAdWords, ActiveCampaignId


class ProductAdsAdmin(admin.ModelAdmin):
    list_display = ('product', 'campaign_id', 'ad_group_id', 'status',
        'impressions', 'clicks', 'cost', 'average_cpc', 'total_sales', 'profit_banked',
        'datetime_updated')

admin.site.register(ProductAdWords, ProductAdsAdmin)
admin.site.register(ActiveCampaignId)