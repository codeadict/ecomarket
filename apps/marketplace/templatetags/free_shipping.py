# -*- coding: utf-8 -*-

from django import template
from marketplace.models import Country

register = template.Library()

country_cache = {}


def get_country(country_code):
    """
    Creates a country instance and stores it. Reason:
    The session only holds the customer's country code, not an instance of Country
    that is needed to check if there is free shipping.
    It would be a big waste of ressources to query the database for one country
    over and over again

    :param country_code:
    :return: Country instance
    """
    if not country_code in country_cache:
        country_cache[country_code] = Country.objects.get(code=country_code)

    return country_cache[country_code]


@register.filter
def has_free_shipping(product, country_code):
    """
    checks if a product has free shipping

    :param product: Product instance
    :param country_code: country code (usually request.country)
    :return:
    """
    country = get_country(country_code)
    if product.has_free_shipping(country):
        return True
    else:
        return False
