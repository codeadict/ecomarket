import logging

from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView, ListView

from main.utils.decorators import view_dispatch_decorator
from main.utils import OrderableListView, DynamicPaginationMixin

logger = logging.getLogger(__name__)


@view_dispatch_decorator(login_required)
class BoughtBaseView(DynamicPaginationMixin, OrderableListView):
    template_name = "accounts/bought/bought.html"
    context_object_name = "orders"
    paginate_by = 8
    default_order = "created"
    tabs = [{"created":"date"}]

    def get_queryset(self):
        order = self.get_queryset_order()
        return self.request.user.orders.order_by(order).all()


class BoughtView(BoughtBaseView):
    pass


class BoughtAwaitingFeedbackView(BoughtBaseView):
    template_name = "accounts/bought/bought.html"

    def get_queryset(self, **kwargs):
        order = self.get_queryset_order()
        return self.request.user.orders.awaiting_feedback().order_by(order)


class BoughtFeedbackGivenView(BoughtBaseView):
    template_name = "accounts/bought/bought.html"

    def get_queryset(self, **kwargs):
        order = self.get_queryset_order()
        return self.request.user.orders.completed().order_by(order)
