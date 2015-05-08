# -*- encoding: utf-8 -*-
from django import template

register = template.Library()


@register.inclusion_tag('main/fragments/top_nav_dropdown.html', takes_context=True)
def top_nav_dropdown(context):
    """

    :param context: added automatically by django
    :return:
    """
    request = context['request']
    return context