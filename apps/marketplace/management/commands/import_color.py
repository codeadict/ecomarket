import csv

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError, make_option

from marketplace.models import Product, Color


class Command(BaseCommand):
    help = "Read from a TSV of product/color information and update Products as needed"
    args = "filename"

    def handle(self, *args, **options):
        if len(args) != 1:
            raise CommandError("Usage: <filename>")

        filename, = args

        fh = csv.reader(open(filename, 'rb'), dialect=csv.excel_tab)
        for row in fh:
            try:
                product = Product.objects.get(pk=row[0])
                if not product.colors.count():
                    change = False
                    for col in range(2, (len(row) - 1)):
                        color_text = row[col].strip()
                        if not color_text:
                            continue
                        try:
                            color = Color.objects.get(title=color_text)
                            product.colors.add(color)
                            change = True
                        except Color.DoesNotExist:
                            pass
                    if change:
                        product.save()
                        print product.title
            except Product.DoesNotExist:
                print "Product with ID %s does not exist" % row[0]