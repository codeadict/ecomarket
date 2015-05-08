# coding=utf-8
import datetime
import logging
import pytz

from django.core.management.base import BaseCommand

from apps.marketplace.models import Stall, Product, StallStatusLog
from apps.notifications.events import Events


logger = logging.getLogger(__name__)


class Command(BaseCommand):
    def handle(self, *args, **options):
        now = datetime.datetime.now(tz=pytz.utc)

        for stall in Stall.objects.filter(is_suspended=False).iterator():
            qualified_products_count = stall.products.filter(status=Product.PUBLISHED_LIVE).count()

            if qualified_products_count == 0:
                stall.last_stock_checked_at = now
                stall.save()
            elif stall.days_to_next_stockcheck == -1:
                ###
                # Suspend this Stall, and Suspend all products of this Stall
                ###
                stall.is_suspended = True
                stall.reason_for_suspension = 2 # Seller is not updating Stock
                stall.save()
                stall.products.filter(status=Product.PUBLISHED_LIVE).update(status=Product.PUBLISHED_SUSPENDED, updated=now)
                status = StallStatusLog()
                status.stall = stall
                status.renewal_tier = stall.renewal_tier
                status.is_suspended = stall.is_suspended
                status.reason_for_suspension = stall.reason_for_suspension
                status.updated_at = now
                status.save()

                try:
                    Events(None).stall_suspended(stall)
                except Exception as e:
                    print "Stall id %s had error in processing - %s" % (stall.id, e)
            elif stall.days_to_next_stockcheck == 5:
                ###
                # Send notification to Seller asking them to so Stock Check
                ###
                try:
                    Events(None).stall_stockcheck(stall)
                except Exception as e:
                    print "Stall id %s had error in processing - %s" % (stall.id, e)
            elif stall.days_to_next_stockcheck == 1:
                try:
                    Events(None).stall_stockcheck_urgent(stall)
                except Exception as e:
                    print "Stall id %s had error in processing - %s" % (stall.id, e)

        filename = "/tmp/%s.txt" % __name__
        result_file = open(filename, "w")
        now = datetime.datetime.now()
        result_file.write(now.isoformat())