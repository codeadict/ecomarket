from django.shortcuts import get_object_or_404
from django.views.generic.base import TemplateView, RedirectView
from django.core.exceptions import PermissionDenied
from main.utils.decorators import view_dispatch_decorator
from django.contrib.auth.decorators import login_required

from purchase.models import Order

@view_dispatch_decorator(login_required)
class InvoiceView(TemplateView):
    template_name = "accounts/invoice.html"

    def get_context_data(self, **kwargs):
        context = super (InvoiceView, self).get_context_data(**kwargs)
        order_id = kwargs["order_id"]
        order = get_object_or_404(Order, id=order_id)
        user_is_merchant = order.stall.user == self.request.user
        if not user_is_merchant and order.user != self.request.user:
            raise PermissionDenied()
        context.update({
            "order": order,
            "user_is_merchant": user_is_merchant,
        })
        return context


