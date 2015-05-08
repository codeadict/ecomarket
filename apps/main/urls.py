from django.conf.urls.defaults import patterns, url
from django.views.generic import TemplateView

from main.views import HomePageView, SellPageView, sitemap_xml, robots_txt, activities_modal


urlpatterns = patterns('main.views',
    url(r'^sell-my-products/$', SellPageView.as_view(), name="sell_page"),
    url(r'^sitemap\.xml$', sitemap_xml, name="sitemap_xml"),
    url(r'^robots\.txt$', robots_txt, name="robots_txt"),
    url(r'^activities/info/$', activities_modal, name="activities_modal"),
    url(r'^$', HomePageView.as_view(), name='home'),
)
