"""
Source:
http://gist.github.com/246727

"""
import logging

from django import template
from django.template import Context, Template, Variable, VariableDoesNotExist, Library
from django.template.defaulttags import URLNode, url
from django.template.defaultfilters import stringfilter
from django.template.loader import get_template


register = template.Library()

IGNORE_METHODS = ['join', 'title']
@register.simple_tag
def stringmethod(name, value, first=None, second=None, third=None):
    return make_filter(name)(value, first, second, third)

@stringfilter
def make_filter(name):
    def filter(value, first=None, second=None, third=None):
        args = [first, second, third]
        method = getattr(value, name)

        while True:
            try:
                return method(*args)
            except TypeError:
                args.pop(len(args) - 1)

    return filter

for name in dir(u''):
    # Ignore all private string methods
    if name.startswith('_'):
        continue

    # Ignore ``join`` method
    if name in IGNORE_METHODS:
        continue

    # Create new template filters for all string methods that not yet added
    # to Django template built-ins
    register.filter(name, make_filter(name))

