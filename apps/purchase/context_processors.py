# -*- encoding: utf-8 -*-
from discounts.models import UTMCode
from marketplace.models import Country
from purchase.models import Payment
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


def has_incomplete_payment_tracking(request):
    """
    Checks if a user has a payment that is not tracked, yet.
    .filter() and [0] are used, because it is possible that a user
    has deactivated JavaScript (and the tracking will not work). If the user
    makes multiple purchases .get() would break.

    :param request:
    :return:
    """
    if request.user.is_authenticated():
        pending_trackings = Payment.objects.filter(
            purchaser=request.user,
            logged_to_google=False
        ).order_by(
            '-created'
        )

        if pending_trackings.count() > 0:
            pending_tracking = pending_trackings[0]
            logger.debug("Found untracked order")
            try:
                utm_code = request.user.campaigns.all()[0].name
            except IndexError:
                utm_code = request.campaign.get("name")

            try:
                utm_code_obj = UTMCode.objects.get(code=utm_code)
            except UTMCode.DoesNotExist:
                curebit_site_id = settings.DEFAULT_CUREBIT_SITE_ID
            else:
                curebit_site_id = utm_code_obj.site.slug

            return {
                'order_to_track': pending_tracking.order,
                'countries': [c.to_json() for c in Country.objects.all()],
                'curebit_site_id': curebit_site_id,
                'base_url': request.build_absolute_uri("/"),
            }
        else:
            logger.debug("No untracked order found")
            return {}
    else:
        return {}
