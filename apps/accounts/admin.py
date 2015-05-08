# coding=utf-8
import datetime
from django.conf.urls import patterns, url
from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django.core.urlresolvers import reverse

from accounts.models import UserProfile, VideoType, Video
from django.http import HttpResponse
from django.template.response import TemplateResponse
from django.utils.safestring import mark_safe
import pytz
from django.utils.translation import ugettext_lazy as _


class CustomUserAdmin(UserAdmin):
    def impersonate(self, obj):
        impersonate_url = reverse('impersonate', kwargs={'user_id': obj.id})
        return '<a href="%s">Go</a>' % (impersonate_url)
    impersonate.allow_tags = True
    impersonate.short_description = 'Impersonate User'

    def stall_link(self, instance):
        if hasattr(instance, 'stall'):
            return '<a href="%s">Stall %s</a>' % (instance.stall.admin_url,
                instance.stall.id)
        else:
            return None
    stall_link.short_description = 'Stall'
    stall_link.allow_tags = True

    list_display = ('username', 'stall_link', 'email', 'first_name', 'last_name', 'is_active', 'impersonate' )
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'date_joined', 'last_login')


class UserProfileAdmin(admin.ModelAdmin):
    search_fields = ('user__username', 'user__email', 'user__first_name', 'user__last_name')
    list_filter = ('user__is_staff', 'user__is_superuser', 'user__is_active', 'user__date_joined', 'user__last_login')


class VideoTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'time_limit')


class CreatedDaysRangeFilter(SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = _('Created')

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'created_date'

    def lookups(self, request, model_admin):
        """
        Filter by the number of days left to do the next stock check
        """
        return (
            ('today', _('Today')),
            ('last7', _('last 7 days')),
            ('last30', _('last 30 days')),
            ('all', _('All')),
        )

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        # Compare the requested value (either '80s' or 'other')
        # to decide how to filter the queryset.
        if self.value() == 'today':
            now = datetime.datetime.now(tz=pytz.utc)
            range_start = now.replace(hour=0, minute=0, second=0)
            range_stop = now.replace(hour=23, minute=59, second=59)
            return queryset.filter(created__range=(range_start, range_stop))

        if self.value() == 'last7':
            now = datetime.datetime.now(tz=pytz.utc)
            date_start = (now - datetime.timedelta(days=7)).replace(hour=0, minute=0, second=0)
            return queryset.filter(created__gte=date_start)

        if self.value() == 'last30':
            now = datetime.datetime.now(tz=pytz.utc)
            date_start = (now - datetime.timedelta(days=30)).replace(hour=0, minute=0, second=0)
            return queryset.filter(created__gte=date_start)

        if self.value() == 'all':
            return queryset.all()


class VideoAdmin(admin.ModelAdmin):
    model = Video
    search_fields = ('user__stall__title', 'user__first_name', 'user__last_name', 'user__email')
    list_display = (
        'id',
        'name',
        'author',
        'stall',
        'phone_mobile',
        'phone_landline',
        'thumbnail',
        'created',
    )
    list_filter = (
        CreatedDaysRangeFilter,
    )

    actions = ['status_update']

    def author(self, instance):
        url = reverse('admin:auth_user_change', args=(instance.user.id,))
        return mark_safe(
            '<a href="%s">%s</a>'
            % (url, instance.user.username))
    author.short_description = 'User'
    author.allow_tags = True

    def name(self, instance):
        return u'%s %s' % (instance.user.first_name, instance.user.last_name)
    name.short_description = 'Name'

    def stall(self, instance):
        url = reverse('admin:marketplace_stall_change', args=(instance.id,))
        return mark_safe('<a href="%s">%s</a>' % (url, instance.user.stall.title))
    stall.allow_tags = True

    def phone_mobile(self, instance):
        return instance.user.stall.phone_mobile

    def phone_landline(self, instance):
        return instance.user.stall.phone_landline

    def thumbnail(self, instance):
        url = reverse('admin:admin_watch_video', args=(instance.id,))
        return mark_safe('<a href="%s"><img src="%s" width="120" height="80"/></a>' % (url, instance.splash_url))
    thumbnail.short_description = 'Video'
    thumbnail.allow_tags = True

    def status_update(self, request, queryset):
        if request.POST.get('post'):
            pass
        else:
            context = {
                'queryset': queryset,
            }
            return TemplateResponse(
                request,
                'accounts/video/admin/status_update.html',
                context,
                current_app=self.admin_site.name
            )

    def get_urls(self):
        urls = super(VideoAdmin, self).get_urls()
        my_urls = patterns(
            '',
            url(r'^(.+)/watch/$', self.admin_site.admin_view(self.watch_video), name='admin_watch_video')
        )
        return my_urls + urls

    def watch_video(self, request, object_id):
        video = self.model.objects.get(id=object_id)

        context = {
            'video': video
        }

        return TemplateResponse(
            request,
            'accounts/video/admin/watch_video.html',
            context,
            current_app=self.admin_site.name
        )

try:
    admin.site.unregister(User)
except admin.sites.NotRegistered:
    pass

admin.site.register(User, CustomUserAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(VideoType, VideoTypeAdmin)
admin.site.register(Video, VideoAdmin)