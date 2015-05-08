from django.conf.urls.defaults import patterns, url

from apps.search.forms import ProductSearchForm
from apps.search.views import ProductSearchView

product_search_view = ProductSearchView(form_class=ProductSearchForm, as_discover=True)

urlpatterns = patterns('search.views',
    url(r'^$', 'category_discover', name='category_discover'),
    url(r'^(?P<category>[\w-]+)/$', 'category_discover', name='category_discover'),
    url(r'^([\w-]+)/([\w-]+)/$', product_search_view, name='category_discover'),
    url(r'^([\w-]+)/([\w-]+)/([\w-]+)/$', product_search_view, name='category_discover'),
    url(r'^([\w-]+)/([\w-]+)/([\w-]+)/([\w-]+)/$', product_search_view, name='category_discover'),
)
