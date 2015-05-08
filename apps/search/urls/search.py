from django.conf.urls.defaults import patterns, url

from apps.search.forms import ProductSearchForm
from apps.search.views import ProductSearchView

product_search_view = ProductSearchView(form_class=ProductSearchForm, as_discover=False)

urlpatterns = patterns('search.views',
    url(r'^$', product_search_view, name='product_search'),
    url(r'^([\w-]+)/$', product_search_view, name='product_search'),
    url(r'^([\w-]+)/([\w-]+)/$', product_search_view, name='product_search'),
    url(r'^([\w-]+)/([\w-]+)/([\w-]+)/$', product_search_view, name='product_search'),
    url(r'^([\w-]+)/([\w-]+)/([\w-]+)/([\w-]+)/$', product_search_view, name='product_search'),
)
