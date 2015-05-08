import warnings

from django.core.management.base import NoArgsCommand, make_option
from django.db import transaction

from marketplace.models import Category, Product


class Command(NoArgsCommand):

    """
    ONE OFF command to populate the images for all 2-tier categories with the
    first image they can find.

    This keeps the /discover/ page fresh and full of products which caught 
    someones eye.
    """

    @transaction.commit_on_success
    def handle_noargs(self, **options):
        updated = 0
        for category in Category.objects.exclude(products=None):
            if category.update_image():
                updated += 1
                category.save()
            else:
                warnings.warn("No products found for %s - using default image" % (category.name,))
        self.stdout.write("Updated %d categories.\n" % updated)
