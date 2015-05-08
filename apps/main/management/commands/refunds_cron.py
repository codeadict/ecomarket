from django.core.management.base import BaseCommand, CommandError
from purchase.models import Order
from notifications import Events

class Command(BaseCommand):
    args = ''
    help = "Finds all overdue orders and takes action"

    def handle(self, *args, **kwargs):
        # handle orders which have not been dispatched after 14 days
        self.stdout.write("Processing overdue orders\n")
        for order in Order.objects.dispatch_overdue(14).all():
            self.stdout.write("overdue order number {0}\n".format(order.id))
            # if email not sent then  send email to seller asking them
            # to mark dispatched. Also, this will send a reminder every
            # day, we may want to control that a bit.
            Events(none).order_reminder(order)

        self.stdout.write("Refunding orders overdue by 30 days\n")
        for order in Order.objects.dispatch_overdue(30).all():
            self.stdout.write("Refunding order number {0}\n".format(order.id))
            # refund order and notify merchant and user
            order.refund()
            Events(none).order_refunded(order)

        self.stdout.write("Executing payments\n")
        for order in Order.objects.ready_to_pay(30).all():
            self.stdout.write("Executing payment for order number {0}\n".format(order.id))
            order.payment.execute()

