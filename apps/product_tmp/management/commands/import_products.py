from datetime import datetime

from django.conf import settings
from django.core.management.base import NoArgsCommand, CommandError
from django.db import connections

from product_tmp.models import OldCategory, TempProduct


class Command(NoArgsCommand):
    def handle_noargs(self, **options):
        cursor = connections['ecom'].cursor()
        cursor.execute('select * from jos_ethmp_products order by product_id;')
        results = cursor.fetchall()
        for result in results:
            id_ = result[0]
            title = result[1]
            print title

            description = result[5]
            colors = result[8]
            keywords = result[15]
            category_id = result[10]
            try:
                old_category = OldCategory.objects.get(id=category_id)
            except:
                old_category = None

            product = TempProduct(
                id=id_,
                title=title,
                description=description,
                colors=colors,
                keywords=keywords,
                old_category=old_category,
                created = datetime.now(),
                updated = datetime.now(),
                )
            product.save()
