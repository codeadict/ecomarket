import logging

from django.core.urlresolvers import reverse
from django.utils.decorators import method_decorator
from django.views.generic.base import TemplateView, RedirectView
from django.views.generic.list import ListView

from main.utils import DynamicPaginationMixin

from accounts.utils import seller_account_required
from purchase.models import Order


logger = logging.getLogger(__name__)


class SoldRedirectView(RedirectView):
    permanent = False
    query_string = True

    def get_redirect_url(self):
        return reverse('sold_awaiting_shipping')


class SoldBaseView(DynamicPaginationMixin, ListView):
    template_name = "accounts/sold.html"
    context_object_name = "orders"
    paginate_by = 8

    def get_context_data(self, *args, **kwargs):
        context = super(SoldBaseView, self).get_context_data(*args, **kwargs)
        if "order_by" in self.request.REQUEST:
            context["order_by"] = self.request.REQUEST["order_by"]
        else:
            context["order_by"] = "date-asc"

        context['refund_reasons'] = Order.refund_reasons

        return context

    def get_queryset(self):
        order_by = self.get_queryset_order()
        return self._get_unordered_queryset().order_by(order_by).all()

    def _get_unordered_queryset(self):
        return self.request.user.stall.orders

    def get_queryset_order(self):
        if "order_by" not in self.request.REQUEST:
            return "-created"
        order_by = self.request.REQUEST["order_by"]
        if order_by == "date-asc":
            return "-created"
        elif order_by == "date-desc":
            return "created"

    @method_decorator(seller_account_required)
    def dispatch(self, *args, **kwargs):
        return super(SoldBaseView, self).dispatch(*args, **kwargs)


class SoldAwaitingShippingView(SoldBaseView):

    def _get_unordered_queryset(self):
        return self.request.user.stall.orders.awaiting_shipping()


class SoldAwaitingFeedbackView(SoldBaseView):

    def _get_unordered_queryset(self):
        return self.request.user.stall.orders.awaiting_feedback()


class SoldCompletedView(SoldBaseView):

    def _get_unordered_queryset(self):
        return self.request.user.stall.orders.dispatched()


class SoldAllView(SoldBaseView):
    pass


class SoldOrderDetailView(TemplateView):
    template_name = "accounts/sold/detail.html"
