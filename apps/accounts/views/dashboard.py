import logging

from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.views.generic.base import TemplateView, RedirectView

from main.utils.decorators import view_dispatch_decorator
from marketplace.models import Stall

logger = logging.getLogger(__name__)


@view_dispatch_decorator(login_required)
class DashboardRedirectView(RedirectView):
    permanent = False
    query_string = True

    def get_redirect_url(self):
        try:
            if self.request.user.stall:
                    # Disabled dashboard_awaiting_delivery tab for 2.0 launch.
                    # If you enable this also enable the tab in accounts/fragments/tabs.html
                    # return reverse('dashboard_awaiting_delivery')
                    return reverse('sold')
        except Stall.DoesNotExist:
            return reverse('bought')


@view_dispatch_decorator(login_required)
class DashboardBaseView(TemplateView):

    def get_context_data(self, **kwargs):
        context = super(DashboardBaseView, self).get_context_data(**kwargs)
        context['base'] = 'Params of base'
        return context


class DashboardAwaitingDeliveryView(DashboardBaseView):
    template_name = "accounts/dashboard/items.html"


class DashboardWaitingFeedbackView(DashboardBaseView):
    template_name = "accounts/dashboard/items.html"


class DashboardUnresolvedQuestionsView(DashboardBaseView):
    template_name = "accounts/dashboard/items.html"
