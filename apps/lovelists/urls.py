from django.conf.urls.defaults import patterns, url

urlpatterns = patterns("lovelists.views",
    url(r'^$', "main", name="main"),
    url(r'^ajax/add/(?P<product_slug>[\w\-]+)/$', "ajax_add_to_list"),
    url(r'^ajax/add/(?P<product_slug>[\w\-]+)/(?P<identifier>\d{8})/$', "ajax_add_to_list"),
    url(r'^ajax/remove/(?P<product_slug>[\w\-]+)/(?P<identifier>\d{8})/$', "ajax_remove_from_list"),
    url(r'^ajax/current_love_list/$', "ajax_current_love_list"),
    url(r'^ajax/current_love_list/(?P<product_slug>[\w\-]+)/$', "ajax_current_love_list"),
    url(r'^ajax/love_list_select/(?P<product_slug>[\w\-]+)/$', "ajax_love_list_select", name="ajax_love_list_select"),
    url(r'^(?P<identifier>\d{8})/$', "view"),
    url(r'^(?P<identifier>\d{8})/edit/$', "edit", name="edit"),
    url(r'^(?P<identifier>\d{8})/delete/$', "delete", name="delete"),
    url(r'^([a-zA-Z0-9 @_\.,+!?-]+)/$', "lists", name="lists"),
    url(r'^(?P<category>[\w-]+)/(?P<slug>[a-zA-Z0-9 @_\.,+!?-]+)/(?P<identifier>\d{8})/$', "view", name="view"),
)
