# -*- encoding: utf-8 -*-
from django.core.management import BaseCommand
import csv
from django.utils.datetime_safe import datetime
from sem.adwords_api_helper import get_adgroup_data
from sem.models import ProductAdWords


class Command(BaseCommand):
    """
    This command takes a csv file and adds some data from Google AdWords into it.
    It is basically a one-off command.
    """

    def handle(self, *args, **options):
        first_of_may = datetime(year=2013, month=5, day=1)
        new_pla_start = datetime(year=2013, month=9, day=20)
        date_end = datetime(year=2013, month=9, day=23)
        ad_group_list = []
        data = {}

        from purchase.models import LineItem
        from analytics.models import CampaignTrack

        for row in self._get_entries():
            try:
                ad = ProductAdWords.objects.get(product__slug=row["slug"])
            except Exception:
                continue

            ad_group_list.append(ad.ad_group_id)
            data[ad.ad_group_id] = row

            row['orders_since_start'] = LineItem.objects.filter(
                product=ad.product,
                created__gte=first_of_may,
            ).count()

            orders_since_new_pla = LineItem.objects.filter(
                product=ad.product,
                created__gte=new_pla_start,
            )

            for line_item in orders_since_new_pla:
                user = line_item.order.user
                pla_count = CampaignTrack.objects.filter(
                    user=user,
                    created_at__year=line_item.created.year,
                    created_at__month=line_item.created.month,
                    created_at__day=line_item.created.day,
                    name__contains="PLA",
                ).count()
                if pla_count > 0:
                    row['orders_since_new_pla'] += 1

            row['status'] = ad.status

        for ad_group in get_adgroup_data(ad_group_list, first_of_may, date_end):
            data[ad_group['id']]['google_cost'] = ad_group['stats']['cost']['microAmount']
            data[ad_group['id']]['total_cost_since_start'] = float(ad_group['stats']['cost']['microAmount']) / float(1000000)

        for ad_group in get_adgroup_data(ad_group_list, new_pla_start, date_end):
            data[ad_group['id']]['total_cost_since_new_pla'] = float(ad_group['stats']['cost']['microAmount']) / float(1000000)

        with open("profitable_adwords_new_data.csv", "wb") as csvfile:
            writer = csv.writer(csvfile, delimiter=";", quotechar='"', quoting=csv.QUOTE_ALL)
            for row in data.itervalues():
                row['revenue_since_new_pla'] = row['orders_since_new_pla'] * row['total_price'] * 0.2
                row['total_profit_since_new_pla'] = row['revenue_since_new_pla'] - row['total_cost_since_new_pla']

                writer.writerow((
                    row['slug'],
                    row['url'],
                    row['price'],
                    row['shipping_price'],
                    row['total_price'],
                    row['google_cost'],
                    row['total_cost_since_start'],
                    row['total_cost_since_new_pla'],
                    row['orders_since_start'],
                    row['orders_since_new_pla'],
                    row['revenue_since_new_pla'],
                    row['total_profit_since_new_pla'],
                    row['status']
                ))

        csvfile.close()

    def _get_entries(self):
        with open("profitable_adwords_2013_09_19.csv","rb") as csvfile:
            reader = csv.reader(csvfile, delimiter=";", quotechar='"')
            for row in reader:
                yield {
                    'name': row[0],
                    'slug': row[1],
                    'url': row[2],
                    'price': row[3],
                    'shipping_price': float(row[4]),
                    'total_price': float(row[5]),
                    'google_cost': 0,
                    'total_cost_since_start': 0,
                    'total_cost_since_new_pla': 0,
                    'orders_since_start': 0,
                    'orders_since_new_pla': 0,
                    'revenue_since_new_pla': 0,
                    'total_profit_since_new_pla': 0
                }

        csvfile.close()