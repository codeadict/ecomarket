from __future__ import print_function

from datetime import datetime, timedelta

from django.core.management.base import NoArgsCommand, make_option
from django.db import transaction

from marketplace.models import Product
from purchase.models import LineItem


class Command(NoArgsCommand):

    """
    (Re)populate the value of product.number_of_sales or
    product.number_of_recent_sales
    """

    option_list = NoArgsCommand.option_list + (
        make_option("--period", dest="period", default=None, type="int",
                    help="Period of time to get data from, in days (if set, "
                         "this populates number_of_recent_sales, else "
                         "number_of_sales)"),
    )

    @transaction.commit_on_success
    def handle_noargs(self, period=None, **options):
        verbosity = int(options["verbosity"])
        field_name = ("number_of_sales" if period is None
                      else "number_of_recent_sales")
        if verbosity >= 2:
            print("Updating field %s:" % field_name, file=self.stdout)
        updated = 0
        for product in Product.objects.all():
            filters = {"product_id": product.id}
            if period:
                filters["order__created__gt"] = \
                    datetime.now() - timedelta(days=period)
            line_items = LineItem.objects.filter(**filters)
            sales = 0
            for item in line_items:
                sales += item.quantity
            if verbosity >= 2:
                print("Setting to %d for %s" % (sales, product.slug),
                      file=self.stdout)
            # We can't use save() directly without signals being called, so use
            # update() instead
            Product.objects.filter(id=product.id).update(**{field_name: sales})
            updated += 1
            if updated % 10 == 0:
                print("Updated %d products" % updated, file=self.stdout)
        print("Updated %d products" % updated, file=self.stdout)
