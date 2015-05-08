"""This is not an admin module, it's completely custom"""
from django import forms
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.utils.decorators import method_decorator
from django.views.generic import DetailView
from purchase.models import Order
from main.utils import OrderableListView

class FilterMixin(object):

    def get_queryset_filters(self):
        filters = {}
        for item in self.allowed_filters:
            if item in self.request.GET:
                 filters[self.allowed_filters[item]] = self.request.GET[item]
        return filters

    def get_queryset(self):
        return super(FilterMixin, self).get_queryset()\
              .filter(**self.get_queryset_filters())


class AdminOnlyViewMixin(object):

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        request = args[0]
        if not request.user.is_staff:
            return HttpResponseForbidden("You need to be an admin to see that screen")
        return super(AdminOnlyViewMixin, self).dispatch(*args, **kwargs)


class AdminOrderViewFilterForm(forms.Form):
    user_id = forms.IntegerField(label="User id", required=False)
    username = forms.CharField(label="Username", required=False)
    order_id = forms.IntegerField(required=False)
    created_before = forms.DateField(label="Order placed after",
                                     required=False,
                                     widget=forms.DateInput(attrs={"class":"date-picker"}))
    created_after = forms.DateField(label="order placed before",
                                    required=False,
                                    widget=forms.DateInput(attrs={"class":"date-picker"}))
    stall_id = forms.IntegerField(label="Stall ID", required=False)
    stall_name = forms.CharField(label="Stall name", required=False)
    stall_email = forms.CharField(label="Stall email", required=False)
    stall_username = forms.CharField(label="Stall user username", required=False)


class AdminOrderView(AdminOnlyViewMixin, FilterMixin, OrderableListView):
    template_name = "purchase/admin/orders.html"
    model = Order
    context_object_name = "orders"
    default_order = "created"
    tabs = ["created"]
    allowed_filters = {
        "created_after": "created__lt",
        "created_before": "created__gt",
        "user_id": "user__id",
        "username": "user__username",
        "stall_id": "stall__id",
        "stall_name": "stall__title",
        "stall_email": "stall__user__email",
        "stall_username": "stall__user__username",
    }
    paginate_by=10

    def get_context_data(self, *args, **kwargs):
        context = super(AdminOrderView, self).get_context_data(*args, **kwargs)
        context.update({
            "filter_form": AdminOrderViewFilterForm(self.request.REQUEST)
        })
        return context

class AdminOrderDetailView(AdminOnlyViewMixin, DetailView):
    model = Order
    context_object_name = "order"
    template_name = "purchase/admin/order.html"
    pk_url_kwarg = "order_id"
