from django.conf.urls.defaults import patterns, url
from purchase.admin import AdminOrderView, AdminOrderDetailView

urlpatterns = patterns('purchase.views.admin',
                        url(r'orders$', AdminOrderView.as_view(),
                            name='orders_admin'),
                       url(r'orders/(?P<order_id>\d+)$',
                           AdminOrderDetailView.as_view(),
                           name='orders_admin_detail'),)
