from urllib import urlencode

from django import template
from django.template import resolve_variable

register = template.Library()


@register.simple_tag(takes_context=True)
def add_get_parameter(context, **kwargs):
    request = resolve_variable('request', context)
    data = request.GET.copy()
    for key in kwargs.keys():
        if key in data:
            del data[key]
        if kwargs[key] is None or kwargs[key] == "":
            del kwargs[key]
    params = data.urlencode()
    extra_params = urlencode(kwargs)
    # Because of a bug in infinitescroll, the extra params should always
    # come last
    if extra_params:
        if params:
            params = "%s&amp;%s" % (params, extra_params)
        else:
            params = extra_params
    if params:
        return "?%s" % params
    return "."
