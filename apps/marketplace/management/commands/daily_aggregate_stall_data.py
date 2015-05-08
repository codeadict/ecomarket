# coding=utf-8
import datetime, pytz

from django.core.management.base import NoArgsCommand

from apps.marketplace.models import Stall, StallStatusLog, Product
from apps.messaging.models import Message


class Command(NoArgsCommand):
    """
    Delete unused address for all users.
    What is kept back - addresses used in orders.
    If there are no orders for a user, then the last added address is kept back.
    All other addresses are deleted for a user.
    """
    help = "Delete unused addresses for all users"
    
    def handle_noargs(self, **options):
        last_month = datetime.datetime.now(tz=pytz.utc) - datetime.timedelta(days=30)

        for stall in Stall.objects.all():
            stall.total_gmv_till_yesterday = float(stall.total_gmv)
            stall.total_orders_till_yesterday = (stall.orders.exclude(payment=None).count()
                + stall.orders.filter(is_joomla_order=True).count())
            stall.is_active = True if (stall.user.last_login > last_month) else False
            stall.total_suspensions_till_yesterday = StallStatusLog.objects.filter(stall=stall, is_suspended=True).count()

            stall.total_products_till_yesterday = stall.products.all().count()
            stall.total_live_products_till_yesterday = stall.products.filter(status=Product.PUBLISHED_LIVE).count()
            stall.total_messages_received_till_yesterday = Message.objects.filter(recipient=stall.user).count()
            stall.days_to_next_stockcheck_till_yesterday = stall.days_to_next_stockcheck

            stall.save()

        filename = "/tmp/%s.txt" % __name__
        result_file = open(filename, "w")
        now = datetime.datetime.now()
        result_file.write(now.isoformat())