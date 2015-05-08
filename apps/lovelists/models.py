from __future__ import division

from itertools import chain
import math

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models
from django.contrib.contenttypes.models import ContentType

from django_extensions.db.fields import AutoSlugField

from main.utils import generate_identifier


class LoveList(models.Model):

    user = models.ForeignKey(User, related_name="love_lists")

    primary_category = models.ForeignKey(
        'marketplace.Category', related_name="love_lists", verbose_name="main category")
    secondary_category = models.ForeignKey(
        'marketplace.Category', related_name="+2", blank=True, null=True)
    tertiary_category = models.ForeignKey(
        'marketplace.Category', related_name="+3", blank=True, null=True)

    title = models.CharField(max_length=155)
    description = models.TextField(blank=True, null=True)
    slug = AutoSlugField(populate_from="title", allow_duplicates=True,
                         overwrite=True)
    is_public = models.BooleanField()
    identifier = models.IntegerField(max_length=8, default=0, unique=True)
    products = models.ManyToManyField('marketplace.Product', through="LoveListProduct",
                                      related_name="love_lists")

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    promoted = models.DateTimeField(default=None, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.identifier == 0:
            self.identifier = generate_identifier(LoveList)
        super(LoveList, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("lovelist:view", kwargs={
            "category": self.primary_category.slug,
            "slug": self.slug,
            "identifier": self.identifier,
        })

    def get_first_product(self):
        all_products = self.products.order_by('-pk')
        if all_products:
            return all_products[0]
        return None

    class Meta:
        ordering = ("-updated", )

    def __unicode__(self):
        return unicode(self.title)

    @property
    def hot_products(self):
        return (self.products.live()
                             .order_by('-number_of_recent_sales')
                             .select_related('stall__identifier')
                             .prefetch_related('prices'))
        
    @property
    def categories(self):
        return [c.name for c in self.category_objs()]

    def category_objs(self):
        def _split_categories(cat):
            while cat:
                yield cat
                cat = cat.parent
        categories = [self.primary_category,
                      self.secondary_category,
                      self.tertiary_category]
        return chain(*[reversed(list(_split_categories(cat)))
                       for cat in categories if cat is not None])


class LoveListProduct(models.Model):

    love_list = models.ForeignKey(LoveList,
                                  related_name="product_relationships")
    product = models.ForeignKey('marketplace.Product')
    weight = models.IntegerField(blank=True, null=False)

    def __getattr__(self, name):
        try:
            return super(LoveListProduct, self).__getattr__(name)
        except AttributeError:
            if name.startswith("_") and "cache" in name:
                # Avoid confusing Django's internals
                raise
            return getattr(self.product, name)

    def save(self, *args, **kwargs):
        if self.weight is None:
            siblings = self.love_list.product_relationships.all()\
                .order_by("-weight")
            if self.pk:
                siblings = siblings.exclude(pk=self.pk)
            if siblings.count() == 0:
                self.weight = 0
            else:
                # Floor the max weight to the nearest 100, then add 100
                # For instance, if the max weight is 158, return 200
                max_weight = siblings[0].weight
                max_weight_floored = int(math.floor(max_weight / 100)) * 100
                self.weight = max_weight_floored + 100
        return super(LoveListProduct, self).save(*args, **kwargs)

    class Meta:
        ordering = ("weight", )
        unique_together = ("love_list", "product")

    def __unicode__(self):
        return u"%s in %s" % (unicode(self.product), unicode(self.love_list))


class PromotionScheduler(models.Model):

    start_date = models.DateField()
    love_list = models.ForeignKey(LoveList)
    actioned = models.BooleanField(default=False)

    def __unicode__(self):
        data = u"Promote {list} on {date}".format(list=self.love_list,
                                                  date=self.start_date)
        if self.actioned:
            data = u"(%s)" % data
        return data

    class Meta:
        ordering = ("-start_date", )
