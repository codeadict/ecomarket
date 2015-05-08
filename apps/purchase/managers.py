from django.db import models
from django.db.models import Q, get_model
import datetime
import re

class CartStallManager(models.Manager):

    def remaining_stalls(self):
        """
        Returns stalls that haven't been checked out yet via payment provider.
        """
        return self.get_query_set().filter(checked_out=False)


class OrderManager(models.Manager):
    """Implements a dispatch_overdue method for orders"""

    def _dispatch_overdue(self, days):
        """Returns orders which have not been dispatched bu which are
        older than days
        """
        delta = datetime.timedelta(days=days - 1)
        max_created = datetime.datetime.now() - delta
        return self.filter(
            line_items__refund__isnull=True,
            line_items__dispatched=False,
            created__lt=max_created,
            is_joomla_order=False,
        )

    def dispatch_overdue(self, days):
        """Returns all orders which are older than deadline and which have
        at least one line_item which is not marked as dispatched and has
        not been refunded

        :param days: An integer representing the number of days before an
                     order is considered overdue.
        """
        return self._dispatch_overdue(days).distinct()

    def dispatch_overdue_by(self, days):
        """Returns all orders which are overdue by exactly days"""
        delta = datetime.timedelta(days=days)
        min_created = datetime.datetime.now() - delta
        return self._dispatch_overdue(days).filter(
            created__gte=min_created
        ).distinct()


    def ready_to_pay(self, days):
        """Returns all orders which are older than day and have all line items
        marked as either dispatched or refunded and whose payment status is
        CREATED

        :param days: An integer number of days at which point the payment should
                     be taken for an order.
        """
        # Little hack to avoid circular import problems.
        from purchase.models import Payment
        max_created = datetime.datetime.now() - datetime.timedelta(days=days)
        return self.exclude(
            line_items__refund__isnull=True,
            line_items__dispatched=False
        ) & self.filter(
            created__lt=max_created,
            payment__status=Payment.STATUS_PRIMARY_PAID,
            is_joomla_order=False,
        )

    def awaiting_feedback(self):
        return self.filter(feedback__isnull=True)

    def feedback_given(self):
        return self.filter(feedback__isnull=False)

    def _dispatched(self):
        return (self.filter(
            line_items__refund__isnull=False,
            line_items__dispatched=False
        ) | self.filter(
            line_items__dispatched=True
        ) | self.filter(
            is_joomla_order=True
        ))

    def dispatched(self):
        return self._dispatched().distinct()

    def completed(self):
        # For now, consider any order which is dispatched or
        # is from the old joomla system to be completed, later we will
        # want to consider feedback.
        #return (self._dispatched() & self.feedback_given()).distinct()
        return (self._dispatched().distinct())

    def awaiting_shipping(self):
        return self.filter(
            line_items__refund__isnull=True,
            line_items__dispatched=False,
            is_joomla_order=False,
        ).distinct()


