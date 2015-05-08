"""
Contains generic comments tags/filters for use across the site.
"""

from django import template
from django.conf import settings
from django.contrib import comments
from django.contrib.contenttypes.models import ContentType

register = template.Library()


class CommentListNode(template.Node):
    """
    Class for handling the get_comment_* template tags.
    """
    
    def __init__(self, ctype=None, as_varname=None, comment=None):
        if ctype is None:
            raise template.TemplateSyntaxError("Comment nodes must be given a ctype.")
        self.comment_model = comments.get_model()
        self.as_varname = as_varname
        self.ctype = ctype
        self.comment = comment

    def render(self, context):
        qs = self.get_query_set(context)
        context[self.as_varname] = self.get_context_value_from_queryset(context, qs)
        return ''

    def get_query_set(self, context):
        qs = self.comment_model.objects.filter(
            content_type = self.ctype,
            site__pk     = settings.SITE_ID,
        )
        # The is_public and is_removed fields are implementation details of the
        # built-in comment model's spam filtering system, so they might not
        # be present on a custom comment model subclass. If they exist, we
        # should filter on them.
        field_names = [f.name for f in self.comment_model._meta.fields]
        if 'is_public' in field_names:
            qs = qs.filter(is_public=True)
        if getattr(settings, 'COMMENTS_HIDE_REMOVED', True) and 'is_removed' in field_names:
            qs = qs.filter(is_removed=False)
        if 'submit_date' in field_names:
            qs = qs.order_by('-submit_date')
        count = getattr(settings, 'APP_COMMENTS_TO_SHOW', None)
        if count is not None:
            qs = qs[:count]
        return qs

    def get_context_value_from_queryset(self, context, qs):
        return list(qs)


@register.tag
def get_comments_for_model(parser, token):
    """
    Gets the list of comments for the given params and populates the template
    context with a variable containing that value, whose name is defined by the
    'as' clause.

    Syntax::

        {% get_comments_for_model for [app].[model] as [varname]  %}

    """
    tokens = token.contents.split()
    if tokens[1] != 'for':
        raise template.TemplateSyntaxError("Second argument in %r tag must be 'for'" % tokens[0])
    # {% get_whatever for obj as varname %}
    if len(tokens) == 5:
        if tokens[3] != 'as':
            raise template.TemplateSyntaxError("Third argument in %r must be 'as'" % tokens[0])
    else:
        raise template.TemplateSyntaxError("%r tag requires 4 arguments" % tokens[0])
    try:
        app, model = tokens[2].split('.')
        ctype = ContentType.objects.get_by_natural_key(app, model)
    except ValueError:
        raise template.TemplateSyntaxError("Third argument in %r must be in the format 'app.model'" % tokens[0])
    except ContentType.DoesNotExist:
        raise template.TemplateSyntaxError("%r tag has non-existant content-type: '%s.%s'" % (tokens[0], app, model))         
    return CommentListNode(ctype, tokens[4])
