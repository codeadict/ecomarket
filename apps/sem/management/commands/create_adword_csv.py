# -*- encoding: utf-8 -*-
from django.core.management import BaseCommand
import csv
from django.utils.datetime_safe import datetime
from marketplace.models import Country
from sem.adwords_api_helper import get_adgroup_data
from sem.models import ProductAdWords
from purchase.models import LineItem
from analytics.models import CampaignTrack


class Command(BaseCommand):
    """
    This command takes a csv file and adds some data from Google AdWords into it.
    It is basically a one-off command.
    """

    def handle(self, *args, **options):
        dates_end = self._parse_dates(*args)

        first_of_may = datetime(year=2013, month=5, day=1)
        new_pla_start = datetime(year=2013, month=9, day=20)
        ad_group_list = []
        data = {}
        country = Country.objects.get(code="GB")
        counter = 0

        for date_end in dates_end:
            csvfilename = 'all_adwords_' + date_end.strftime('%Y_%m_%d.csv')

            for ad in ProductAdWords.objects.all():
                counter += 1
                if counter % 100 == 0:
                    print "processed %d products" % counter

                order_count_since_start = LineItem.objects.filter(
                    product=ad.product,
                    created__gte=first_of_may,
                ).count()

                orders_since_new_pla = LineItem.objects.filter(
                    product=ad.product,
                    created__gte=new_pla_start,
                    created__lt=date_end,
                )

                order_count_since_new_pla = 0
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
                        order_count_since_new_pla += line_item.quantity

                total_orders_ever = LineItem.objects.filter(product=ad.product).count()

                shipping_price, shipping_price_extra = ad.product.get_shipping_prices(country)

                if shipping_price is None:
                    continue

                data[ad.ad_group_id] = {
                    'slug': ad.product.slug,
                    'url': ad.product.get_absolute_url(),
                    'price': float(ad.product.price.amount.amount),
                    'shipping_price': float(shipping_price.amount),
                    'total_price': float(ad.product.price.amount.amount + shipping_price.amount),
                    'order_count_since_start': order_count_since_start,
                    'order_count_since_new_pla': order_count_since_new_pla,
                    'total_orders_ever': total_orders_ever,
                    'status': ad.status,
                }

                ad_group_list.append(ad.ad_group_id)

            counter = 0
            for ad_group in get_adgroup_data(ad_group_list, first_of_may, date_end):
                counter += 1
                if counter % 100 == 0:
                    print "processed %d old cost entries" % counter

                data[ad_group['id']]['google_cost'] = ad_group['stats']['cost']['microAmount']
                data[ad_group['id']]['total_cost_since_start'] = float(ad_group['stats']['cost']['microAmount']) / float(1000000)

            counter = 0
            for ad_group in get_adgroup_data(ad_group_list, new_pla_start, date_end):
                counter += 1
                if counter % 100 == 0:
                    print "processed %d new cost entries" % counter

                data[ad_group['id']]['total_cost_since_new_pla'] = float(ad_group['stats']['cost']['microAmount']) / float(1000000)

            with open(csvfilename, "wb") as csvfile:
                writer = csv.writer(csvfile, delimiter=";", quotechar='"', quoting=csv.QUOTE_ALL)

                writer.writerow((
                    'slug',
                    'url',
                    'price',
                    'shipping price',
                    'total price',
                    'all time ad cost',
                    'ad cost since May 1st',
                    'ad cost since new PLA',
                    'order count since May 1st',
                    'order count since new PLA',
                    'total orders ever',
                    'revenue since new PLA',
                    'total profit since new PLA',
                    'current status',
                ))

                for row in data.itervalues():
                    row['revenue_since_new_pla'] = row['order_count_since_new_pla'] * row['total_price'] * 0.2
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
                        row['order_count_since_start'],
                        row['order_count_since_new_pla'],
                        row['total_orders_ever'],
                        row['revenue_since_new_pla'],
                        row['total_profit_since_new_pla'],
                        row['status']
                    ))

            csvfile.close()

    @classmethod
    def _parse_dates(cls, *args):
        output = []
        try:
            dates = args[0].split(",")
        except IndexError:
            dates = None
        if not dates:
            today = datetime.today()
            year, month, day = today.year, today.month, today.day
            output.append(datetime(year=int(year), month=int(month), day=int(day)))
        else:
            for date in dates:
                year, month, day = date.split("-")
                output.append(datetime(year=int(year), month=int(month), day=int(day)))
        return output