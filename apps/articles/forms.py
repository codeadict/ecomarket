import logging

from django import forms
from django.contrib.sites.models import Site
from django.utils.translation import ugettext_lazy as _
from models import Article, Tag

from ckeditor.widgets import CKEditorWidget

log = logging.getLogger('articles.forms')


def tag(name):
    """Returns a Tag object for the given name"""

    slug = Tag.clean_tag(name)

    log.debug('Looking for Tag with slug "%s"...' % (slug,))
    t, created = Tag.objects.get_or_create(slug=slug, defaults={'name': name})
    log.debug('Found Tag %s. Name: %s Slug: %s Created: %s' % (t.pk, t.name, t.slug, created))

    if not t.name:
        t.name = name
        t.save()

    return t


class ArticleAdminForm(forms.ModelForm):
    tags = forms.CharField(initial='', required=False,
                           widget=forms.TextInput(attrs={'size': 100}),
                           help_text=_('Words that describe this article'))
    content = forms.CharField(widget=CKEditorWidget())

    def __init__(self, *args, **kwargs):
        """Sets the list of tags to be a string"""

        instance = kwargs.get('instance', None)
        if instance:
            init = kwargs.get('initial', {})
            init['tags'] = ' '.join([t.name for t in instance.tags.all()])
            kwargs['initial'] = init

        super(ArticleAdminForm, self).__init__(*args, **kwargs)

    def clean_tags(self):
        """Turns the string of tags into a list"""

        tags = [tag(t.strip()) for t in self.cleaned_data['tags'].split() if len(t.strip())]

        log.debug('Tagging Article %s with: %s' % (self.cleaned_data['title'], tags))
        self.cleaned_data['tags'] = tags
        return self.cleaned_data['tags']

    def save(self, *args, **kwargs):
        """Remove any old tags that may have been set that we no longer need"""
        if self.instance.pk:
            self.instance.tags.clear()
        article = super(ArticleAdminForm, self).save(*args, **kwargs)
        return article

    class Meta:
        model = Article

    class Media:
        css = {
            'all': ('css/jquery.autocomplete.css',),
        }
        js = (
            'js/jquery-1.7.2.min.js',
            'js/jquery.bgiframe.min.js',
            'js/jquery.autocomplete.pack.js',
            'js/tag_autocomplete.js',
        )
