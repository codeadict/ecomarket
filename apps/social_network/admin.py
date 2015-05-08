from django.contrib import admin

from apps.social_network.models import UserFollow


class UserFollowAdmin(admin.ModelAdmin):
    pass


admin.site.register(UserFollow, UserFollowAdmin)