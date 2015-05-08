# -*- coding: utf-8 -*-

from django import template
from django.conf import settings

register = template.Library()

@register.filter
def getitem ( item, string ):
  return item.get(string,'')