from datetime import datetime
from decimal import Decimal

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext_lazy as _

from categories.models import CategoryBase
from marketplace.models import Category, Recipient


class OldCategory(CategoryBase):
    """
    Contains hierarchial product categories
    """
    class Meta:
        verbose_name_plural = 'categories'


class TempProduct(models.Model):
    title = models.CharField(_('title'), blank=False, max_length=200)
    slug = models.TextField(blank=True, default='', null=False)
    description = models.TextField(blank=True, default='', null=False)
    colors = models.TextField(blank=True, default='', null=False)
    keywords = models.TextField(blank=True, default='', null=False)
    old_category = models.ForeignKey(OldCategory, verbose_name="old category", null=True, blank=True)
    primary_category = models.ForeignKey(Category, verbose_name="main category", null=True, blank=True)
    secondary_category = models.ForeignKey(Category, verbose_name="secondary category", related_name='tmp_products_sec', null=True, blank=True)

    #recipient = models.ManyToManyField(Recipient, blank=True, null=True, related_name='tmp_products')
    recipients = models.TextField(default="", blank=True)

    last_updated_by = models.ForeignKey(User, blank=True, default=None, null=True)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True, default=datetime.now)

