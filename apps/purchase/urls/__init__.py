from django.conf.urls.defaults import patterns, url
from purchase.views import RefundView, CartProductsView, CartStallView
from purchase.admin import AdminOrderView

import settings
import purchase.receivers


urlpatterns = patterns(
    'purchase.views',
    url(r'^add/(?P<slug>[\w\-]+)/$', 'checkout_add', name='checkout_add'),
    url(r'^cart/$', 'checkout_cart', name='checkout_cart'),
    url(r'^pay/(?P<cart_stall_id>\d+)/$', 'checkout_pay_stall',
        name='checkout_pay_stall'),
    url(r'^review/(?P<order_id>\d+)/$', 'checkout_review',
        name='checkout_review'),
    url(r'^shipping/(?P<cart_stall_id>\d+)/$', 'checkout_shipping',
        name='checkout_shipping'),
    url(r'^shipping/s(?P<stall_id>\d+)/$', 'checkout_shipping_stall',
        name='checkout_shipping_stall'),
    url(r'^orders/(?P<order_id>\d+)/refunds$', RefundView.as_view(), name='refund'),
    url(r'^orders/(?P<order_id>\d+)/mark_dispatched$',
        'mark_dispatched',
        name='mark_dispatched'),
)

# Cart views
urlpatterns += patterns('purchase.views',
                        url(r'cart/(?P<cart_id>\d+)/products/(?P<product_id>\d+)$',
                            CartProductsView.as_view(),
                            name='cart_products'),
                        url(r'cart/(?P<cart_id>\d+)/products$',
                            CartProductsView.as_view(),
                            name='cart_products'),
                        url(r'cart_stalls/(?P<cart_stall_id>\d+)$',
                            CartStallView.as_view(),
                            name='cart_stalls'),
                        url(r'cart_stalls$',
                            CartStallView.as_view(),
                            name='cart_stalls'))


# Paypal Adaptive
# ===============
urlpatterns += patterns('purchase.views',
    url(r'^cancel/pay/(?P<payment_id>\d+)/(?P<payment_secret_uuid>[\d\w\-]+)$',
        'payment_cancel',
        name="paypal_adaptive_cancel"),
    url(r'^return/pay/(?P<payment_id>\d+)/(?P<payment_secret_uuid>[\d\w\-]+)/$',
        'payment_return',
        name="paypal_adaptive_return"),
    url(r'^tracking/(?P<payment_id>\d+)$',
        'payment_tracking_complete',
        name='payment_tracking_complete'),
    url(r'^ipn_handler/(?P<payment_id>\d+)/(?P<payment_secret_uuid>[\d\w\-]+)/$', 'ipn_handler', name='ipn_handler'),
    url(r'pending/(?P<payment_id>\d+)/', 'payment_pending', name='payment_pending'),
    url(r'check_payment_status/(?P<payment_id>\d+)/', 'check_payment_status', name='check_payment_status'),
    url(r'payment_check_timeout/(?P<payment_id>\d+)/', 'payment_check_timeout', name='payment_check_timeout'),
    url(r'store_phone_number/', 'store_phone_number', name='store_phone_number'),
)

adminpatterns = patterns('purchase.views.admin',
                        url(r'orders', AdminOrderView.as_view(),
                            name='orders_admin'),)
