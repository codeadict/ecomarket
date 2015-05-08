# coding=utf-8
from django.core.management.base import BaseCommand, CommandError
from notifications import Events
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    args = ''
    help = "Finds all overdue orders and takes action"

    def handle(self, *args, **kwargs):
        exceptions = []
        from purchase.models import Order
        for order in Order.objects.ready_to_pay(0):
            try:
                order.payment.execute()
            except Exception as ex:
                logger.error(
                    "Error processing payment for order {0}".format(order.id),
                    exc_info=True)

        for overdue_days in [3,7,13,14]:
            for order in Order.objects.dispatch_overdue_by(overdue_days):
                print("Sending {0} day overdue reminder for order id "
                      "{1}".format(overdue_days, order.id))
                Events(None).order_reminder(order)

        #for order_to_refund in Order.objects.dispatch_overdue(30):
            #print("refunding order id {0} as it is over 30 days since "
                  #"required dispatch date".format(order_to_refund.id))
            #order_to_refund.refund("More than 14 days without dispatching")





