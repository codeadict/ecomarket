from django.db import models
from django.db.models.query import QuerySet


class StallManager(models.Manager):
    """Custom manager for the Stall model. """


class ProductMixin(object):

    def live(self):
        return self.filter(status=self.model.PUBLISHED_LIVE)

    def unpublished(self):
#        return self.filter(status=self.model.PUBLISHED_UNPUBLISHED)
#        Have to return published_draft for backwards compatibility
        return self.filter(status__in=[
            self.model.PUBLISHED_DRAFT,
            self.model.PUBLISHED_UNPUBLISHED])

    def active(self):
        return self.exclude(status=self.model.PUBLISHED_DELETED)

    def deleted(self):
        return self.filter(status=self.model.PUBLISHED_DELETED)

    def sold_out(self):
        return self.filter(
            status=self.model.PUBLISHED_LIVE,
            stock=0)

    def suspended(self):
        return self.filter(status=self.model.PUBLISHED_SUSPENDED)


class ProductQuerySet(QuerySet, ProductMixin):
    """
    Django 1.6 patch:
    https://github.com/django/django/commit/de9942a667
    """
    def in_bulk(self, id_list):        
        """
        Returns a dictionary mapping each of the given IDs to the object with
        that ID.
        """
        assert self.query.can_filter(), \
                "Cannot use 'limit' or 'offset' with in_bulk"
        if not id_list:
            return {}
        qs = self._clone()
        qs.query.add_filter(('pk__in', id_list))
        qs.query.clear_ordering(force_empty=True)
        return dict([(obj._get_pk_val(), obj) for obj in qs])


class ProductManager(models.Manager, ProductMixin):
    """Custom manager for the Product model. """

    def get_query_set(self):
        return ProductQuerySet(self.model, using=self._db)


class CategoryManager(models.Manager):

    def get_toplevel(self):
        return self.filter(parent__isnull=True)

