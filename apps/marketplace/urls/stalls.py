from django.conf.urls.defaults import patterns, url

from marketplace.views.shipping import ShippingProfileAjaxView, \
    ShippingProfileRuleAjaxView, \
    add_shipping_profile, delete_shipping_profile

urlpatterns = patterns(
    'marketplace.views',
    url(r'^new/$',
        'create_stall',
        name='create_stall'),

    url(r'^(?P<slug>[\w\-]+)/edit/$',
        'edit_stall',
        name='edit_stall'),

    url(r'^(?P<slug>[\w\-]+)/$',
        'my_stall',
        name='my_stall'),

    url(r'^shipping/profile/$',
        ShippingProfileAjaxView.as_view(),
        name="stall_shipping_profile"),

    url(r'^shipping/profile/add/$',
        add_shipping_profile,
        name="stall_shipping_profile_add"),
    url(r'^shipping/profile/delete/$',
        delete_shipping_profile,
        name="stall_shipping_profile_delete"),

    url(r'^shipping/profile/rule/$',
        ShippingProfileRuleAjaxView.as_view(),
        name="stall_shipping_profile_rule")
)
