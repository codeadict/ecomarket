# -*- coding: utf-8 -*-

from django import template
from django.conf import settings

register = template.Library()


@register.simple_tag
def display_rating(rating):
    review_str = ''
    # cut off integer
    rating = int(rating)
    for i in range(0, rating):
        review_str +="<b>★</b>"
    for i in range(rating, 5):
        review_str +="<i>★</i>"
    return review_str
