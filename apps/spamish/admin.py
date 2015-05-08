from django.contrib import admin

from .models import BannedWord


class BannedWordAdmin(admin.ModelAdmin):
    list_display = ('word', 'active',)
    list_filter = ('active',)


admin.site.register(BannedWord, BannedWordAdmin)
