from datetime import timedelta

from django.core.urlresolvers import reverse
from django.db.models import Q

from django.utils.datetime_safe import datetime
from django.utils.safestring import mark_safe


def _get_dispatched_warning(request):
    if not request.user.is_authenticated():
        return
    if not request.user.get_profile().is_seller:
        return
    awaiting_shipping = request.user.stall.orders.awaiting_shipping()
    awaiting_shipping_overdue = awaiting_shipping.filter(
        created__lt=datetime.today() + timedelta(days=3))
    warning_msg = (
        'Look out {name}! You have order(s) that have not been '
        'marked as dispatched or refunded and this will be causing problems '
        'for customers or delays in getting you paid. <a href="{url}">Fix '
        'this now</a>, or <a href="{help_url}" target="_blank">get some help on this</a>.'
        if awaiting_shipping_overdue.count() > 0 else
        '{name}, just a reminder that you have orders to mark as dispatched '
        'or refunded. Please <a href="{url}">do so here</a> or '
        '<a href="{help_url}" target="_blank">get some help</a>.'
        if awaiting_shipping.count() > 0 else ""
    )
    return mark_safe(warning_msg.format(
        name=request.user.first_name, url=reverse("sold"),
        help_url="http://help.ecomarket.com/customer/portal/articles/828639"))

def _get_stall_suspended_warning(request):
    if not request.user.is_authenticated():
        return
    if not request.user.get_profile().is_seller:
        return
    stall = request.user.stall
    if not stall.is_suspended:
        return

    warning_msg = (
        'Look out %(name)s! Your stall on Eco Market has been <b>suspended</b> '
        'because you have not updated the stock of your products. You will not '
        'be able to publish any products until you fix this. '
        '<a href="%(url)s">Do a stock check now</a>, or '
        '<a href="%(help_url)s" target="_blank">get help on how to do this.</a>.' %
        dict(
            name=request.user.first_name,
            url=reverse('stockcheck_update'),
            help_url='http://help.ecomarket.com/customer/portal/articles/1342284-what-is-a-stock-check-and-how-do-i-do-them-'
        )
    )
    return mark_safe(warning_msg)

def _get_stall_upcoming_stockcheck_warning(request):
    if not request.user.is_authenticated():
        return
    if not request.user.get_profile().is_seller:
        return
    stall = request.user.stall
    if stall.is_suspended or stall.days_to_next_stockcheck > 5 or stall.products.live().count() < 1:
        return

    warning_msg = (
        'Look out %(name)s! Your stall on Eco Market if due for a stock check '
        'in just %(days)s days. This is mandatory for all stall owners on Eco Market, '
        'and takes only a few minutes. '
        '<a href="%(url)s">Update your stock now</a>, or '
        '<a href="%(help_url)s" target="_blank">get some help on this</a>.' %
        dict(
            name=request.user.first_name,
            days=stall.days_to_next_stockcheck,
            url=reverse('stockcheck_update'),
            help_url='http://help.ecomarket.com/customer/portal/articles/1342284-what-is-a-stock-check-and-how-do-i-do-them-'
        )
    )
    return mark_safe(warning_msg)

def _get_stockcheck_count(request):
    if not request.user.is_authenticated():
        return
    if hasattr(request.user, "stall") and request.user.stall:
        from apps.marketplace.models import Product
        queryset = Product.objects.filter(stall=request.user.stall)
        return queryset.filter(
            Q(status=Product.PUBLISHED_LIVE) | Q(status=Product.PUBLISHED_SUSPENDED)
        ).count()
    else:
        return 0

def _get_days_to_next_stockcheck(request):
    if not request.user.is_authenticated():
        return
    if hasattr(request.user, "stall") and request.user.stall:
        return request.user.stall.days_to_next_stockcheck
    else:
        return 0

def account_messages(request):
    return {
        "dispatched_warning": _get_dispatched_warning(request),
        "stall_suspended_warning": _get_stall_suspended_warning(request),
        "stall_upcoming_stockcheck_warning": _get_stall_upcoming_stockcheck_warning(request),
        'stockcheck_count': _get_stockcheck_count(request),
        'days_to_next_stockcheck': _get_days_to_next_stockcheck(request)
    }
