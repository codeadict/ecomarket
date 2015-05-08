from django.contrib import admin

from lovelists.forms import LoveListProductForm
from lovelists.formsets import LoveListProductFormSet
from lovelists.models import LoveList, LoveListProduct, PromotionScheduler


class LoveListProductInline(admin.TabularInline):

    model = LoveListProduct
    formset = LoveListProductFormSet
    form = LoveListProductForm


class LoveListAdmin(admin.ModelAdmin):

    inlines = [LoveListProductInline]


class PromotionSchedulerAdmin(admin.ModelAdmin):

    list_display = ("love_list", "start_date", "actioned")
    exclude = ("actioned", )


admin.site.register(LoveList, LoveListAdmin)
admin.site.register(PromotionScheduler, PromotionSchedulerAdmin)
