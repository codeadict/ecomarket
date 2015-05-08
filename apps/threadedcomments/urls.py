from django.conf.urls import patterns, url


urlpatterns = patterns('threadedcomments.views',
    url(r'^immediate-delete/(\d+)/$', 'delete', name='comment_immediate_delete'),
    url(r'^reply/(\d+)/$', 'reply', name='comment_reply'),
    url(r'^create/(\d+)/(\d+)/$', 'create', name='comment_create'),
)
