from django.conf import settings
from django.conf.urls.defaults import patterns, url

from django.views.generic import RedirectView

from marketplace.views.product import \
    ProductDetailView, ProductCreateView, product_taxonomy, \
    certificate_search, ProductUpdate, ProductImageUploaderAjax, \
    product_credentials


urlpatterns = patterns(
    'marketplace.views',
    url(r'^taxonomy/$',
        product_taxonomy,
        name='product_taxonomy'),

    url(r'^certificates/$',
        certificate_search,
        name='certificate_search'),

    url(r'^new/$',
        ProductCreateView.as_view(),
        name='create_product'),

    url(r'^(?P<stall_identifier>\d{8})/(?P<product_name>[\w\-]+)/credentials$',
        product_credentials,
        name='product_credentials'),

    url(r'^(?P<stall_identifier>\d{8})/(?P<product_name>[\w\-]+)/$',
        ProductDetailView.as_view(),
        name='product_page'),

    url(r'^(?P<stall_identifier>\d{8})/(?P<product_name>[\w\-]+)/(?P<currency>\w{3})/$',
        ProductDetailView.as_view(),
        name='product_page_fixed_currency'),

    url(r'^(?P<stall_identifier>\d{8})/(?P<product_name>[\w\-]+)/edit/$',
        ProductUpdate.as_view(),
        name='product_edit'),

    url(r'^image/upload/$', ProductImageUploaderAjax.as_view(),
        name='product_image_upload'),
    url(r'^product_feed/', RedirectView.as_view(
        url=settings.MEDIA_URL + "/product/product_feed.xml", permanent=True),
        name='product_feed'),

)
