import logging
import json

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, redirect
from django.views.generic.base import RedirectView, TemplateResponseMixin, View
from django.views.generic.edit import UpdateView
from django.http import HttpResponse
from django.template import Context, Template

from accounts.forms.account import (AccountForm, EmailNotificationForm,
                                    PrivacyForm)
from main.utils.decorators import view_dispatch_decorator

from accounts.forms.shipping_address import ShippingAddressForm
from accounts.models import EmailNotification, Privacy, ShippingAddress

logger = logging.getLogger(__name__)


@view_dispatch_decorator(login_required)
class AccountTabBaseView(UpdateView):
    model = User

    def get_object(self, queryset=None):
        user = self.request.user
        return user

    def get_context_data(self, **kwargs):
        context = super(AccountTabBaseView, self).get_context_data(**kwargs)
        context['base'] = 'Params of base'
        return context

    def get_success_url(self):
        return self.request.path


class AccountTabAccountRedirectView(RedirectView):
    permanent = False
    query_string = True

    def get_redirect_url(self):
        return reverse('account_account')


# TODO: update sailthru e-mail address
class AccountTabAccountView(AccountTabBaseView):
    form_class = AccountForm
    template_name = "accounts/account/account.html"


class AccountTabDeliveryAddressesView(View, TemplateResponseMixin):
    template_name = "accounts/account/delivery_addresses.html"

    def get(self, request, address_id=None):
        addresses = request.user.addresses.all()
        address_form = ShippingAddressForm()
        context = {
                "addresses": addresses,
                "address_form": address_form,
                }
        logger.debug("Addresses is {0}".format(addresses))
        return self.render_to_response(context)

    def post(self, request, address_id=None):
        if address_id is None:
            form = ShippingAddressForm(request.POST)
        else:
            address = get_object_or_404(ShippingAddress, id=address_id)
            form = ShippingAddressForm(request.POST, instance=address)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            address.save()
            return redirect('account_delivery_addresses')
        else:
            print(form.errors)
            form = ShippingAddressForm()
        context = {
                "address_form": form
                }
        return self.render_to_response(context)


class AccountDeliveryAddressUpdateView(UpdateView):
    """
    This function is used by other views to allow editing address using AJAX
    The template does not inherit from base.html
    """
    template_name = "accounts/account/delivery_update.html"
    form_class = ShippingAddressForm
    model = ShippingAddress
    
    def get_context_data(self, **kwargs):
        context = super(AccountDeliveryAddressUpdateView, self).get_context_data(**kwargs)
        context['address'] = get_object_or_404(ShippingAddress, pk=self.kwargs.get('pk'), user=self.request.user)
        return context
    
    def form_valid(self, form):
        form.save()
        data = {
            "success": True,
            "address": self.object.id,
            "tmpl": Template('{{ address.name }}<br>{{ address.line1 }}<br>' + \
                    '{% if address.line2 %}{{ address.line2 }}<br>{% endif %}' + \
                    '{{ address.city }}, {{ address.postal_code }}<br>' + \
                    '{{ address.state }}, <b>{{ address.country }}</b>').render(Context({"address": self.object}))
        }
        return HttpResponse(
            json.dumps(data),
            mimetype="application/json"
        )


def account_delivery_address_delete(request, pk):
    address = get_object_or_404(ShippingAddress, pk=pk, user=request.user)
    address.delete()
    return HttpResponse('{"success": true, "address": %s}' % pk, mimetype="application/json")


class AccountTabConnectedAccountsView(AccountTabBaseView):
    template_name = "accounts/account/connected_accounts.html"


class AccountTabEmailNotificationsView(AccountTabBaseView):
    model = EmailNotification
    form_class = EmailNotificationForm
    template_name = "accounts/account/email_notifications.html"

    def get_object(self, queryset=None):
        user = self.request.user
        email_notification = user.email_notification
        return email_notification


class AccountTabPrivacyView(AccountTabBaseView):
    model = Privacy
    form_class = PrivacyForm
    template_name = "accounts/account/privacy.html"

    def get_object(self, queryset=None):
        user = self.request.user
        privacy = user.privacy
        return privacy
