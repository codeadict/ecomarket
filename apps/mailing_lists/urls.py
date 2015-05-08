from django.conf.urls import url, patterns
from django.views.generic import TemplateView

from .views import CreateSignup, QuickRegisterView, sailthru_sync, BlogSignup, BlogQuickRegisterView

urlpatterns = patterns('',
    url(r'^signup/$', view=CreateSignup.as_view(), name='email_capture'),
    url(r'^signup/blog/$', view=BlogSignup.as_view(), name='email_capture_from_blog'),
    url(r'^site_register/$', view=QuickRegisterView.as_view(), name='quick_register'),
    url(r'^site_register/blog/$', view=BlogQuickRegisterView.as_view(), name='quick_register_from_blog'),
    url(r'^sync/sailthru$', view=sailthru_sync, name='sync-from-sailthru'),
)
