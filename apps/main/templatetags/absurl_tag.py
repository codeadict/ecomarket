import urlparse

from django import template
from django.conf import settings
from django.contrib.sites.models import Site
from django.template.defaulttags import URLNode, url


register = template.Library()
# -------------
# Generic Tags
# -------------
class AbsoluteURLNode(URLNode):
    """
    http://djangosnippets.org/snippets/1518/
    Usage:
        {% load absurl_tag %}
        {% absurl profile_edit %}
    """
    def render(self, context):
        path = super(AbsoluteURLNode, self).render(context)
        site = Site.objects.get_current()
        domain = "http://%s" % site.domain
        if self.asvar:
            context[self.asvar]= urlparse.urljoin(domain, context[self.asvar])
            return ''
        else:
            return urlparse.urljoin(domain, path)
        return urlparse.urljoin(domain, path)

def absurl(parser, token, node_cls=AbsoluteURLNode):
    """Just like {% url %} but ads the domain of the current site."""
    node_instance = url(parser, token)
    return node_cls(view_name=node_instance.view_name,
        args=node_instance.args,
        kwargs=node_instance.kwargs,
        asvar=node_instance.asvar)
absurl = register.tag(absurl)
