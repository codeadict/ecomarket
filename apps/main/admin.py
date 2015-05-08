from django import forms
from django.contrib import admin
from django.contrib.flatpages.models import FlatPage
from django.contrib.flatpages.admin import FlatPageAdmin as FlatPageAdminBase
from django.contrib.sessions.models import Session

from tinymce.widgets import TinyMCE
from actstream.models import Follow


class SessionAdmin(admin.ModelAdmin):
    def _session_data(self, obj):
        return obj.get_decoded()
    list_display = ['session_key', '_session_data', 'expire_date']

class FlatPageForm(forms.ModelForm):
    content = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 30}))

    class Meta:
        model = FlatPage

class FlatPageAdmin(FlatPageAdminBase):
    form = FlatPageForm


admin.site.register(Session, SessionAdmin)
try:
    admin.site.unregister(FlatPage)
except admin.sites.NotRegistered:
    pass
admin.site.register(FlatPage, FlatPageAdmin)

#Hiding Follow model in the admin interface
admin.site.unregister(Follow)
