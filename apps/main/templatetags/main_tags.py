"""
Contains generic tags/filters for use across the site.
"""

from django import template
from django.conf import settings
from marketplace.models import Category

register = template.Library()


@register.filter
def to_js_bool(value):
    """Converts a python value to a javascript boolean i.e False -> flase"""
    if value:
        return "true"
    return "false"


@register.filter
def none_to_zero(value):
    if value is None:
        return 0
    return value


@register.filter
def mixpanel_date(value):
    return value.strftime("%Y-%m-%dT%H:%M:%S")


@register.simple_tag
def setting(name):
    """
    Allows you to pull settings to templates

    {% setting 'FACEBOOK_APP_ID' %}
    """
    return str(settings.__getattr__(name))


class AssignNode(template.Node):
    """
    Source: http://www.djangosnippets.org/snippets/539/
    """
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def render(self, context):
        context[self.name] = self.value.resolve(context, True)
        return ''


@register.tag(name='assign')
def do_assign(parser, token):
    """
    Assign an expression to a variable in the current context.

    Syntax::
        {% assign [name] [value] %}
    Example::
        {% assign list entry.get_related %}

    """
    bits = token.contents.split()
    if len(bits) != 3:
        raise template.TemplateSyntaxError("'%s' tag takes two arguments" % bits[0])
    value = parser.compile_filter(bits[2])
    return AssignNode(bits[1], value)


# Custom Generic Filter
# ======================

@register.filter
def multiply(value, arg):
    try:
        value = float(value) * float(arg)
    except:
        value = None
    return value


@register.filter
def divide(value, arg):
    try:
        value = float(value) / float(arg)
    except:
        value = None
    return value


# String filters
# ==============
@register.filter
def split(str, splitter):
    return str.split(splitter)


@register.filter
def strip(str):
    return str.strip()


@register.inclusion_tag("fragments/category_footer.html")
def show_categories_footer():
    categories = Category.objects.get_toplevel()
    return {"categories": categories}
