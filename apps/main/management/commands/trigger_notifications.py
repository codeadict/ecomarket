import datetime
from django.core.management.base import BaseCommand, CommandError
from purchase.models import Order
from purchase import notifier
from tests import factories

def trigger_order_notifications(order):
    for day in [3,7,13,14]:
        print("Sending {0} day dispatch reminder".format(day))
        delta = datetime.timedelta(days=day)
        order.created = datetime.datetime.now().date() - delta
        notifier.send_n_day_reminder(order)

    print("Sending merchant order complete")
    notifier.send_merchant_order_complete(order)

    print("sending customer order complete")
    notifier.send_customer_order_complete(order)

    print("sending customer order dispatched")
    notifier.send_customer_dispatched(order)

    print("sending merchant manual refund")
    notifier.send_merchant_manual_refund(order)

    print("sending customer manual refund")
    notifier.send_customer_manual_refund(order)

    print("sending customer automated refund")
    notifier.send_customer_automated_refund(order)

    print("sending merchant automated refund")
    notifier.send_merchant_automated_refund(order)

    print("sending erroneous patpal account")
    payment_attempt = factories.PaymentAttemptFactory.build(cart_stall__stall=order.stall,
                                                      cart_stall__user=order.user)
    payment_attempt.cart_stall.stall = order.stall
    notifier.send_erroneous_paypal_account(payment_attempt)


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        order_id = args[0]
        order = Order.objects.get(id=order_id)
        trigger_order_notifications(order)

