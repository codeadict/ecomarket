from rollyourown import seo


class LinkTag(seo.Tag):

    def __init__(self, rel, **kwargs):
        self.rel = rel
        name = kwargs.pop("name", "link")
        super(LinkTag, self).__init__(name=name, **kwargs)

    def render(self, value):
        return u'<%s rel="%s" href="%s" />' % (self.name, self.rel, value)


class Metadata(seo.Metadata):

    title          = seo.Tag(head=True, max_length=255)
    description    = seo.MetaTag(max_length=255)
    keywords       = seo.KeywordTag()
    canonical_url  = LinkTag(rel="canonical", head=True)
    og_title       = seo.OgMetaTag(name='og:title', help_text='Og Title', populate_from='title', verbose_name='OpenGraph og:title')
    og_description = seo.OgMetaTag(name='og:description', help_text='Og Description', populate_from='description', verbose_name='OpenGraph og:description')
    og_type        = seo.OgMetaTag(name='og:type', verbose_name='OpenGraph og:type')
    og_image       = seo.OgMetaTag(name='og:image', verbose_name='OpenGraph og:image')
    og_url         = seo.OgMetaTag(name='og:url', verbose_name='OpenGraph og:url')
    og_video       = seo.OgMetaTag(name='og:video', verbose_name='OpenGraph og:video')
    sailthru_tags  = seo.MetaTag(name="sailthru.tags")
    sailthru_image  = seo.MetaTag(name="sailthru.image.full")
    sailthru_image_thumb  = seo.MetaTag(name="sailthru.image.thumb")
    sailthru_title  = seo.MetaTag(name="sailthru.title")
    sailthru_stall_title  = seo.MetaTag(name="sailthru.stall-title")
    sailthru_stall_url  = seo.MetaTag(name="sailthru.stall-url")
    sailthru_stall_owner_id  = seo.MetaTag(name="sailthru.stall-owner-id")

    class Meta:
        verbose_name_plural = "Metadata"
        seo_views = (
            # User
            'public_profile',

            # Stall
            'my_stall',

            # Products
            'product_page',

            # Search / Discover
            'product_search',
            'category_discover',

            # Blog / Articles
            'articles_archive', 'articles_archive_page',
            'articles_display_tag', 'articles_display_tag_page',
            'articles_display_category', 'articles_display_category_page',
            'articles_by_author', 'articles_by_author_page',
            'articles_tag_autocomplete',
            'articles_in_month', 'articles_in_month_page',
            'articles_display_article',

            # Love list stuff -
            # see https://github.com/willhardy/django-seo/issues/36 for why we
            # can't use namespacing
            "edit",
            "lists",
            "view",

            # Account Stuff
            'login', 'logout',
            'register', 'register_success',
            'account',
            'password_reset', 'password_reset_done', 'password_reset_confirm', 'password_reset_complete',
            )
        seo_models = ('articles.Article',)
