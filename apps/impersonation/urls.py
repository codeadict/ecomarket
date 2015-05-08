from django.conf.urls.defaults import patterns, url


urlpatterns = patterns('impersonation.views',
    url(r'^deimpersonate/$', 'deimpersonate', name='deimpersonate'),
    url(r'^(?P<user_id>[a-zA-Z0-9 @_\.,+!?-]+)/$', 'impersonate', name='impersonate'),
)
