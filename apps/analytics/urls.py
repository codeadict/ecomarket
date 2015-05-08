from django.conf.urls.defaults import patterns, url

from apps.analytics.views import clicktale_recorded_page


urlpatterns = patterns('',
    url(r'^ct/$', clicktale_recorded_page, name='clicktale_fetch'),
    url(r'^ct/(?P<hash>[a-z0-9]+)/$', clicktale_recorded_page, name='clicktale_fetch')
)