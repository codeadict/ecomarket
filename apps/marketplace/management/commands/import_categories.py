import csv
from os import path
import re

from django.conf import settings
from django.core.management.base import NoArgsCommand, CommandError

from marketplace.models import Category


class Command(NoArgsCommand):
    help = "Import categories from CSV file"

    def handle_noargs(self, **options):
        file_path = path.join(settings.PROJECT_ROOT, 'apps/marketplace/fixtures/cat.csv')

        for col in range(0, 4):
            infile = open(file_path, 'r')
            reader = csv.reader(infile)
            print col
            for row in reader:
                try:
                    name = row[col].strip()
                except:
                    import traceback; traceback.print_exc()

                if not name:
                    continue

                if col-1 < 0:
                    ancestor = None
                else:
                    # get correct parent
                    ancestor = None
                    for ncol in xrange(0, col):
                        ancestor_name = row[ncol].strip()

                        if not ancestor:
                            try:
                                ancestor = Category.objects.get(name=ancestor_name, parent__isnull=True)
                            except:
                                import ipdb; ipdb.set_trace()

                        else:
                            try:
                                ancestor = ancestor.get_children().get(name=ancestor_name)
                            except:
                                import ipdb; ipdb.set_trace()

                category, created = Category.objects.get_or_create(name=name, parent=ancestor)

            infile.close()


        for cat in Category.objects.all():
            name = cat.name
            name = name.replace("t-shirts", "T-shirts")
            name = name.title()
            name = name.replace("And", "and")
            cat.name = name
            cat.save()

