# -*- encoding: utf-8 -*-
import datetime
from django.core.management import BaseCommand
from purchase.models import LineItem
from sem.models import ProductAdWords


class Command(BaseCommand):
    help = "Pulls total sales and puts in into the adwords table"

    def handle(self, *args, **options):
        first_of_may = datetime.datetime(2013, 05, 01)
        adwords = ProductAdWords.objects.all()

        for ad in adwords:
            total_sales = LineItem.objects.filter(product=ad.product, created__gte=first_of_may).count()
            ad.total_sales = total_sales
            ad.save()