import csv
from os import path
import re

from django.conf import settings
from django.core.management.base import NoArgsCommand, CommandError

from product_tmp.models import OldCategory


class Command(NoArgsCommand):
    help = "Import categories from CSV file"

    def handle_noargs(self, **options):
        file_path = path.join(settings.PROJECT_ROOT, 'apps/product_tmp/fixtures/oldcategories.csv')

        #import ipdb; ipdb.set_trace()
        reader = csv.reader(open(file_path, 'rb'), delimiter=',', quotechar='"')
        headerline = reader.next()
        for row in reader:
            id_ = row[0]
            parent_id = int(row[1])
            name = row[2].strip()
            print id_, name, parent_id

            if parent_id==0:
                parent = None
            else:
                try:
                    parent = OldCategory.objects.get(id=parent_id)
                except:
                    print parent_id, "-----------"
                    raise Exception

            category, created = OldCategory.objects.get_or_create(id=id_, name=name, parent=parent)
