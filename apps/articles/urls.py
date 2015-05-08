from django.conf.urls.defaults import patterns, url

from . import views
from .feeds import TagFeed, LatestEntries, TagFeedAtom, LatestEntriesAtom, CategoryFeed, CategoryFeedAtom

# FIXME the below have been commented out because they are broken.
# Either fix the tag/category system (currently hidden) or delete it
#tag_rss = TagFeed()
#cat_rss = CategoryFeed()

latest_rss = LatestEntries()
tag_atom = TagFeedAtom()
cat_atom = CategoryFeedAtom()
latest_atom = LatestEntriesAtom()

urlpatterns = patterns('',
    (r'^(?P<year>\d{4})/(?P<month>.{3})/(?P<day>\d{1,2})/(?P<slug>.*)/$', views.redirect_to_article),
    url(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/page/(?P<page>\d+)/$', views.display_blog_page, name='articles_in_month_page'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/$', views.display_blog_page, name='articles_in_month'),
)

urlpatterns += patterns('',
    url(r'^$', views.display_blog_page, name='articles_archive'),
    url(r'^page/(?P<page>\d+)/$', views.display_blog_page, name='articles_archive_page'),

    url(r'^tag/(?P<tag>.*)/page/(?P<page>\d+)/$', views.display_blog_page, name='articles_display_tag_page'),
    url(r'^tag/(?P<tag>.*)/$', views.display_blog_page, name='articles_display_tag'),

    url(r'^category/(?P<category>.*)/page/(?P<page>\d+)/$', views.display_category_page, name='articles_display_category_page'),
    url(r'^category/(?P<category>.*)/$', views.display_category_page, name='articles_display_category'),

    #url(r'^author/(?P<username>.*)/page/(?P<page>\d+)/$', views.display_blog_page, name='articles_by_author_page'),
    #url(r'^author/(?P<username>.*)/$', views.display_blog_page, name='articles_by_author'),

    url(r'^(?P<year>\d{4})/(?P<slug>.*)/$', views.display_article, name='articles_display_article'),

    # AJAX
    url(r'^ajax/tag/autocomplete/$', views.ajax_tag_autocomplete, name='articles_tag_autocomplete'),

    # RSS
    url(r'^feeds/latest\.rss$', latest_rss, name='articles_rss_feed_latest'),
    url(r'^feeds/latest/$', latest_rss),
    #url(r'^feeds/tag/(?P<slug>[\w_-]+)\.rss$', tag_rss, name='articles_rss_feed_tag'),
    #url(r'^feeds/tag/(?P<slug>[\w_-]+)/$', tag_rss),
    #url(r'^feeds/category/(?P<slug>[\w_-]+)\.rss$', cat_rss, name='articles_rss_feed_category'),
    #url(r'^feeds/category/(?P<slug>[\w_-]+)/$', cat_rss),

    # Atom
    url(r'^feeds/atom/latest\.xml$', latest_atom, name='articles_atom_feed_latest'),
    #url(r'^feeds/atom/tag/(?P<slug>[\w_-]+)\.xml$', tag_atom, name='articles_atom_feed_tag'),
    #url(r'^feeds/atom/category/(?P<slug>[\w_-]+)\.xml$', cat_atom, name='articles_atom_feed_category'),
)
