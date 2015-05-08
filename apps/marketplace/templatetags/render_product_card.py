# -*- encoding: utf-8 -*-
from django import template

register = template.Library()


@register.inclusion_tag('marketplace/fragments/product_card.html', takes_context=True)
def render_product_card(context, product, style, show_price=True):
    """
    Render a product to a template.

    usage example:

       {% render_product_card product 'small' %}

    :param context: added automatically by django
    :param product: product instance that needs to be rendered
    :param style: style of the card; choices: 'small', 'medium'
    :param show_price: Does the price needs to be rendered on the card?
    :return:
    """
    request = context['request']
    context["product"] = product
    context["show_price"] = show_price
    context["country"] = request.country
    context["style"] = style
    return context