from django.contrib import admin

from discounts.models import CurebitSite, UTMCode, Discount, PLACampaign, FreeShipping


# This is no longer used but remains here for posterity
class PLACampaignAdmin(admin.ModelAdmin):

    raw_id_fields = ("products", )
    filter_horizontal = ("countries", )


class FreeShippingAdmin(admin.ModelAdmin):
    list_display = ('description', 'percent_discount')


admin.site.register(CurebitSite)
admin.site.register(UTMCode)
admin.site.register(Discount)
admin.site.register(FreeShipping, FreeShippingAdmin)