from __future__ import absolute_import
import datetime
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe
import pytz

from django.contrib import admin
from categories.admin import CategoryBaseAdmin
from django.contrib.admin import SimpleListFilter
from django.utils.translation import ugettext_lazy as _
from django.db.models import Count

from apps.marketplace.models import \
    Cause, Certificate, Color, Ingredient, \
    Material, Keyword, Occasion, Recipient, \
    Category, Product, Stall, ProductImage, \
    Price, StallCategory, ShippingProfile, \
    ShippingRule, SuggestedCertificate, StallVideo, \
    StallSuspendProxy, StallCallNotes


class CategoryAdmin(CategoryBaseAdmin):
    fields = (
        "parent",
        "name",
        "seo_title",
        "slug",
        "description",
        "image_src",
        "active",
        "navigation_name"
    )

    list_display = (
        'name',
        'navigation_name',
        'active'
    )

    def get_form(self, *args):
        form = super(CategoryAdmin, self).get_form(*args)
        form.base_fields["description"].widget = \
            admin.widgets.AdminTextareaWidget()
        return form


class CauseAdmin(admin.ModelAdmin):
    pass


class CertificateAdmin(admin.ModelAdmin):
    pass


class ColorAdmin(admin.ModelAdmin):
    pass


class IngredientAdmin(admin.ModelAdmin):
    pass


class MaterialAdmin(admin.ModelAdmin):
    pass


class KeywordAdmin(admin.ModelAdmin):
    pass


class OccasionAdmin(admin.ModelAdmin):
    pass


class RecipientAdmin(admin.ModelAdmin):
    pass


class StallVideoAdmin(admin.ModelAdmin):
    search_fields = ('url', 'title')
    list_display = ('stall', 'title', 'url')
    list_filter = ('is_welcome', 'is_published')


class StallAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'title', 'created', 'is_in_video_beta')
    list_editable = ('is_in_video_beta',)
    list_filter = ('created', 'updated',)
    search_fields = ('title', 'description_short')
    readonly_fields = ('is_closed', )
    list_display_links = ('title', )
    search_fields = ('title', 'user__first_name', 'user__last_name', 'user__email')

    def close_stall(self, request, queryset):
        rows_updated = queryset.count()
        for st in queryset.all():
            st.delete()
        if rows_updated == 1:
            message_bit = "1 stall was"
        else:
            message_bit = "%s stalls were" % rows_updated
        self.message_user(request, "%s successfully closed." % message_bit)
    close_stall.short_description = "Close selected stalls"

    actions = ('close_stall',)

    def queryset(self, request):
        qs = super(StallAdmin, self).queryset(request)
        return qs.filter(is_closed=False)


class StallCategoryAdmin(CategoryBaseAdmin):
    pass


class ProductImageInline(admin.TabularInline):
    model = ProductImage


class PriceAdmin(admin.ModelAdmin):
    model = Price
    list_display = ('product', 'amount', 'amount_currency')


class PriceInline(admin.TabularInline):
    model = Price
    extra = 0
    max_num = 1


class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'stall', 'created', 'flag',)
    list_filter = ('created', 'updated', 'status', 'flag',)
    search_fields = ('title', 'description', 'stall__title',)
    inlines = [ProductImageInline]


class ShippingProfileAdmin(admin.ModelAdmin):
    model = ShippingProfile


class ShippingRuleAdmin(admin.ModelAdmin):
    model = ShippingRule


class SuggestedCertificateAdmin(admin.ModelAdmin):
    model = SuggestedCertificate


class OrderRangeFilter(SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = _('Total Orders')

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'orders'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        return (
            ('zero', _('Zero')),
            ('eq1', _('1')),
            ('gt1', _('> 1')),
            ('gt2', _('> 2')),
            ('gt3', _('> 3')),
            ('gt5', _('> 5')),
            ('gt10', _('> 10')),
            ('gt50', _('> 50')),
            ('gt100', _('> 100')),
            ('gt500', _('> 500')),
            ('gt1000', _('> 1000')),
        )

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        # Compare the requested value (either '80s' or 'other')
        # to decide how to filter the queryset.
        if self.value() == 'zero':
            return queryset.filter(total_orders_till_yesterday=0)

        if self.value() == 'eq1':
            return queryset.filter(total_orders_till_yesterday=1)

        if self.value() == 'gt1':
            return queryset.filter(total_orders_till_yesterday__gt=1)

        if self.value() == 'gt2':
            return queryset.filter(total_orders_till_yesterday__gt=2)

        if self.value() == 'gt3':
            return queryset.filter(total_orders_till_yesterday__gt=3)

        if self.value() == 'gt5':
            return queryset.filter(total_orders_till_yesterday__gt=5)

        if self.value() == 'gt10':
            return queryset.filter(total_orders_till_yesterday__gt=10)

        if self.value() == 'gt50':
            return queryset.filter(total_orders_till_yesterday__gt=50)

        if self.value() == 'gt100':
            return queryset.filter(total_orders_till_yesterday__gt=100)

        if self.value() == 'gt500':
            return queryset.filter(total_orders_till_yesterday__gt=500)

        if self.value() == 'gt1000':
            return queryset.filter(total_orders_till_yesterday__gt=1000)


class LiveProductsRangeFilter(SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = _('Live Products')

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'live_products'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        return (
            ('zero', _('Zero')),
            ('eq1', _('1')),
            ('gt1', _('> 1')),
            ('gt2', _('> 2')),
            ('gt3', _('> 3')),
            ('gt5', _('> 5')),
            ('gt10', _('> 10')),
            ('gt50', _('> 50')),
            ('gt100', _('> 100')),
            ('gt500', _('> 500')),
            ('gt1000', _('> 1000')),
        )

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        # Compare the requested value (either '80s' or 'other')
        # to decide how to filter the queryset.
        if self.value() == 'zero':
            return queryset.filter(total_live_products_till_yesterday=0)

        if self.value() == 'eq1':
            return queryset.filter(total_live_products_till_yesterday=1)

        if self.value() == 'gt1':
            return queryset.filter(total_live_products_till_yesterday__gt=1)

        if self.value() == 'gt2':
            return queryset.filter(total_live_products_till_yesterday__gt=2)

        if self.value() == 'gt3':
            return queryset.filter(total_live_products_till_yesterday__gt=3)

        if self.value() == 'gt5':
            return queryset.filter(total_live_products_till_yesterday__gt=5)

        if self.value() == 'gt10':
            return queryset.filter(total_live_products_till_yesterday__gt=10)

        if self.value() == 'gt50':
            return queryset.filter(total_live_products_till_yesterday__gt=50)

        if self.value() == 'gt100':
            return queryset.filter(total_live_products_till_yesterday__gt=100)

        if self.value() == 'gt500':
            return queryset.filter(total_live_products_till_yesterday__gt=500)

        if self.value() == 'gt1000':
            return queryset.filter(total_live_products_till_yesterday__gt=1000)


class MessagesReceivedRangeFilter(SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = _('Messages Received')

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'messages_received'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        return (
            ('zero', _('Zero')),
            ('eq1', _('1')),
            ('gt1', _('> 1')),
            ('gt2', _('> 2')),
            ('gt3', _('> 3')),
            ('gt5', _('> 5')),
            ('gt10', _('> 10')),
            ('gt50', _('> 50')),
            ('gt100', _('> 100')),
            ('gt500', _('> 500')),
            ('gt1000', _('> 1000')),
        )

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        # Compare the requested value (either '80s' or 'other')
        # to decide how to filter the queryset.
        if self.value() == 'zero':
            return queryset.filter(total_messages_received_till_yesterday=0)

        if self.value() == 'eq1':
            return queryset.filter(total_messages_received_till_yesterday=1)

        if self.value() == 'gt1':
            return queryset.filter(total_messages_received_till_yesterday__gt=1)

        if self.value() == 'gt2':
            return queryset.filter(total_messages_received_till_yesterday__gt=2)

        if self.value() == 'gt3':
            return queryset.filter(total_messages_received_till_yesterday__gt=3)

        if self.value() == 'gt5':
            return queryset.filter(total_messages_received_till_yesterday__gt=5)

        if self.value() == 'gt10':
            return queryset.filter(total_messages_received_till_yesterday__gt=10)

        if self.value() == 'gt50':
            return queryset.filter(total_messages_received_till_yesterday__gt=50)

        if self.value() == 'gt100':
            return queryset.filter(total_messages_received_till_yesterday__gt=100)

        if self.value() == 'gt500':
            return queryset.filter(total_messages_received_till_yesterday__gt=500)

        if self.value() == 'gt1000':
            return queryset.filter(total_messages_received_till_yesterday__gt=1000)


class StockCheckDaysRangeFilter(SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = _('Stock Check Due In')

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'stock_check_due'

    def lookups(self, request, model_admin):
        """
        Filter by the number of days left to do the next stock check
        """
        return (
            ('1day', _('1 day')),
            ('2days', _('2 days')),
            ('3days', _('3 days')),
            ('4days', _('4 days')),
            ('5days', _('5 days')),
            ('lt7', _('Less than 7 days')),
            ('lt14', _('Less than 14 days')),
            ('lt30', _('Less than 30 days')),
        )

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        # Compare the requested value (either '80s' or 'other')
        # to decide how to filter the queryset.
        if self.value() == '1day':
            now = datetime.datetime.now(tz=pytz.utc)
            return queryset.filter(days_to_next_stockcheck_till_yesterday=1)

        if self.value() == '2days':
            now = datetime.datetime.now(tz=pytz.utc)
            return queryset.filter(days_to_next_stockcheck_till_yesterday=2)

        if self.value() == '3days':
            now = datetime.datetime.now(tz=pytz.utc)
            return queryset.filter(days_to_next_stockcheck_till_yesterday=3)

        if self.value() == '4days':
            now = datetime.datetime.now(tz=pytz.utc)
            return queryset.filter(days_to_next_stockcheck_till_yesterday=4)

        if self.value() == '5days':
            now = datetime.datetime.now(tz=pytz.utc)
            return queryset.filter(days_to_next_stockcheck_till_yesterday=5)

        if self.value() == 'lt7':
            now = datetime.datetime.now(tz=pytz.utc)
            return queryset.filter(days_to_next_stockcheck_till_yesterday__lt=7)

        if self.value() == 'lt14':
            now = datetime.datetime.now(tz=pytz.utc)
            return queryset.filter(days_to_next_stockcheck_till_yesterday__lt=14)

        if self.value() == 'lt30':
            now = datetime.datetime.now(tz=pytz.utc)
            return queryset.filter(days_to_next_stockcheck_till_yesterday__lt=30)


class CallNotesInline(admin.TabularInline):
    model = StallCallNotes
    extra = 1


class StallSuspendAdmin(admin.ModelAdmin):
    model = StallSuspendProxy

    def username(self, instance):
        url = reverse('admin:auth_user_change', args=(instance.user.id,))
        return mark_safe(
            '<a href="%s">%s</a>'
            % (url, instance.user.username))
    username.short_description = 'Username'
    username.allow_tags = True

    def name(self, instance):
        return u'%s %s' % (instance.user.first_name, instance.user.last_name)
    name.short_description = 'Name'

    def email(self, instance):
        return instance.user.email
    email.short_description = 'Email'

    def last_login_date(self, instance):
        return instance.user.last_login_date
    last_login_date.short_description = 'Last Login Date'

    def has_stock_checked(self, instance):
        return instance.has_stock_checked_ever
    has_stock_checked.short_description = 'Stock checked ever?'
    has_stock_checked.boolean = True

    def queryset(self, request):
        # qs = super(StallSuspendAdmin, self).queryset(request)
        return Stall.objects.filter(is_closed=False)

    list_display = ('name', 'username', 'title', 'phone_mobile', 'phone_landline',
        'total_live_products_till_yesterday', 'total_orders_till_yesterday', 
        'total_messages_received_till_yesterday', 'total_gmv_till_yesterday',
        'is_active', 'is_suspended', 'reason_for_suspension',
        'days_to_next_stockcheck_till_yesterday', 'has_stock_checked', 'created')
    
    list_filter = ('is_active', 'is_suspended', OrderRangeFilter,
        LiveProductsRangeFilter, MessagesReceivedRangeFilter,
        StockCheckDaysRangeFilter)
    search_fields = ('title', 'user__first_name', 'user__last_name', 'user__email')

    fields = ('username', 'name', 'title', 'description_short', 'description_full',
        'email', 'phone_mobile', 'phone_landline', 'total_orders_till_yesterday',
        'total_gmv_till_yesterday', 'total_live_products_till_yesterday',
        'total_products_till_yesterday', 'is_active', 'last_login_date',
        'reason_for_suspension', 'number_of_calls')
    readonly_fields = ('username', 'name', 'email', 'total_orders_till_yesterday',
        'total_gmv_till_yesterday', 'total_live_products_till_yesterday',
        'total_products_till_yesterday', 'is_active', 'last_login_date', 'title',
        'description_short', 'description_full')

    list_display_links = ('title', )
    list_per_page = 500
    list_max_show_all = 2000

    inlines = (CallNotesInline, )


admin.site.register(Category, CategoryAdmin)
admin.site.register(Cause, CauseAdmin)
admin.site.register(Certificate, CertificateAdmin)
admin.site.register(Color, ColorAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Material, MaterialAdmin)
admin.site.register(Keyword, KeywordAdmin)
admin.site.register(Occasion, OccasionAdmin)
admin.site.register(Recipient, RecipientAdmin)
admin.site.register(Stall, StallAdmin)
admin.site.register(StallVideo, StallVideoAdmin)
admin.site.register(StallCategory, StallCategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Price, PriceAdmin)
admin.site.register(ShippingProfile, ShippingProfileAdmin)
admin.site.register(ShippingRule, ShippingRuleAdmin)
admin.site.register(SuggestedCertificate, SuggestedCertificateAdmin)
admin.site.register(StallSuspendProxy, StallSuspendAdmin)