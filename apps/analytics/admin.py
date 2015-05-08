from django.contrib import admin

from apps.analytics.models import (CampaignTrack, AggregateData,
    LifetimeTrack, ProductFormErrors)


class CampaignTrackAdmin(admin.ModelAdmin):
    list_display = ('user', 'email_lead', 'source', 'name', 'medium', 'created_at', 'sent_to_sailthru',)
    search_fields = ('user__username', 'user__email', 'source', 'medium')
    readonly_fields=('user', 'email_lead', 'query_string', 'utmz')
    list_filter = ('sent_to_sailthru',)

admin.site.register(CampaignTrack, CampaignTrackAdmin)


class AggregateDataAdmin(admin.ModelAdmin):
    list_display = ('campaign', 'daily_acquired', 'campaign_cost',
        'customer_acquistion_cost', 'order_count', 'gross_merchant_value', 'revenue_after_commission', 'created_at')
    list_filter = ('created_at',)

admin.site.register(AggregateData, AggregateDataAdmin)


class LifetimeTrackAdmin(admin.ModelAdmin):
    list_display = ('cookie_key', 'user', 'email_lead', 'status', 'created_at',
        'acquired_at', 'activated_at', 'retained_at', 'purchased_at')
    readonly_fields = ('user', 'email_lead', 'created_at', 'acquired_at', 'activated_at', 'retained_at',
        'referred_at', 'purchased_at',)
    list_filter = ('status', 'acquired_at')

admin.site.register(LifetimeTrack, LifetimeTrackAdmin)


class ProductFormErrorsAdmin(admin.ModelAdmin):
    list_display = ('stall', 'had_error', 'product_form_error', 'price_form_error',
        'shipping_form_error', 'images_formset_error', 'created_at')
    readonly_fields = ('stall', 'product_form_error', 'price_form_error', 'shipping_form_error',
        'images_formset_error', 'created_at', 'description_error', 'recipients_error',
        'title_error', 'colors_error', 'keywords_field_error', 'primary_category_error',
        'shipping_profile_error', 'amount_error')
    list_filter = ('created_at',)

admin.site.register(ProductFormErrors, ProductFormErrorsAdmin)