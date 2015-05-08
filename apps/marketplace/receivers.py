# -*- encoding: utf-8 -*-
import logging

import django.dispatch
from purchase.signals import order_payed
from django.conf import settings


logger = logging.getLogger(settings.LOGGER_SIGNALS)


@django.dispatch.receiver(order_payed)
def update_categories(sender, **kwargs):
    """
    Sets new images for the "discover" page.

    :param sender:
    :param kwargs:
    :return:
    """
    logger.debug("received order_payed signal")
    order = kwargs.get("order")

    for line_item in order.line_items.all():
        category = line_item.product.primary_category
        category.update_image(line_item.product)
        category.save()

    logger.debug("Updated categories.")