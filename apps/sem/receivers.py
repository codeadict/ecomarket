# -*- encoding: utf-8 -*-
import logging

import django.dispatch
from purchase.signals import order_payed
from django.conf import settings
from models import ProductAdWords


logger = logging.getLogger(settings.LOGGER_SIGNALS)


@django.dispatch.receiver(order_payed)
def update_total_sales(sender, **kwargs):
    """
    Updates the number of total sales for SEM table.

    :param sender:
    :param kwargs:
    :return:
    """
    logger.debug("received order_payed signal")
    order = kwargs.get("order")

    for li in order.line_items.all():
        try:
            ad = ProductAdWords.objects.get(product=li.product)
            ad.total_sales = ad.total_sales + li.quantity
            ad.save()
        except Exception:
            pass

    logger.debug("Updated adwords sale data.")