# -*- encoding: utf-8 -*-
import logging

from analytics.models import CampaignTrack
import django.dispatch
from django.template import loader, Context
from djipchat.lib import send_to_hipchat
from purchase.models import Order
from purchase.signals import order_payed
from django.conf import settings


logger = logging.getLogger(settings.LOGGER_SIGNALS)


@django.dispatch.receiver(order_payed)
def handle_order_payed(sender, **kwargs):
    order = kwargs.get("order")
    request = kwargs.get("request")

    user = order.user
    profile = user.get_profile()
    em_data = CampaignTrack.objects.filter(user=user).order_by('id')
    try:
        first_em_data, last_em_data = em_data[0], em_data.reverse()[0]
    except IndexError:
        first_em_data = None
        last_em_data = None

    total_orders = Order.objects.filter(user=user).count()

    context = Context({
        'request': request,
        'order': order,
        'first_em_data': first_em_data,
        'last_em_data': last_em_data,
        'total_orders': total_orders,
        'profile': profile,
    })
    template = loader.get_template("purchase/fragments/hipchat_order_notification.html")
    output = template.render(context)
    send_to_hipchat(output)

    logger.debug("Sent order information to hipchat")