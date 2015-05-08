from django.conf.urls.defaults import patterns, url, include
from django.conf import settings
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.views.generic import RedirectView
from django.conf import settings

import sem.receivers

from rollyourown.seo.admin import register_seo_admin
from main.seo import Metadata
from apps.main.views import RecordGuestVideo


admin.autodiscover()
register_seo_admin(admin.site, Metadata)


urlpatterns = patterns('',
    # SEO.
    url(r'^people/(?P<username>[a-zA-Z0-9 @_\.,+!?-]+)/$', 'accounts.views.profile.public_profile', name='public_profile'),
    url(r'^log-in/$', 'accounts.views.login', name='login'),
    url(r'^log-in-quick$', 'accounts.views.quick_signup_login', name='quick_signup_login'),
    url(r'^register/$', 'accounts.views.register', name='register'),
    url(r'^help(-centre/?)?$', RedirectView.as_view(url=settings.SUPPORT_URL), name='help'),

    # App includes.
    url(r'^', include('main.urls',)),
    url(r'^grappelli/', include('grappelli.urls')), # grappelli URLS
    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin/purchase/', include('purchase.urls.adminpatterns')),
    url(r'^accounts/', include('accounts.urls',)),
    url(r'^accounts/social/', include('social_auth.urls')),
    url(r'^impersonation/', include('impersonation.urls',)),
    url(r'^products/', include('marketplace.urls.products',)),
    url(r'^image-crop/', include('image_crop.urls',)),
    url(r'^love/', include('lovelists.urls', namespace="lovelist")),
    url(r'^stalls/', include('marketplace.urls.stalls',)),
    url(r'^t/', include('todos.urls', namespace="todos",)),
    url(r'^messages/', include('messaging.urls',)),
    url(r'^checkout/', include('purchase.urls',)),
    url(r'^discover/', include('search.urls.discover',)),
    url(r'^search/', include('search.urls.search',)),
    url(r'^blog/', include('articles.urls')),
    url(r'^comments/', include('django.contrib.comments.urls')),
    url(r'^comments/', include('threadedcomments.urls')),
    url(r'^ckeditor/', include('ckeditor.urls')),
    url(r'^mailinglists/', include('mailing_lists.urls')),
    url(r'^activities/', include('social_network.urls')),
    url(r'^analytics/', include('apps.analytics.urls')),

    # This is a spcial one time video for invited folks
    url(r'^recordavideo/', RecordGuestVideo.as_view(), name='record_guest_video'),
)

# Adding in flat pages for terms and conditions, privacy etc.
urlpatterns += patterns('',
    ('^pages/', include('django.contrib.flatpages.urls')),
)

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()

    # Serve user uploaded media
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
    )

if settings.TESTING or settings.DEBUG:
    # serve statichtml for developer reference
    urlpatterns += static(
        '/staticfiles/',
        document_root = settings.STATIC_ROOT,
        show_indexes=True,
    )
