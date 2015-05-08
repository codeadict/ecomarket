import logging

from django.shortcuts import redirect

from django.core.urlresolvers import reverse
from django.views.generic.base import RedirectView
from django.views.generic.edit import UpdateView
from django.contrib.auth.decorators import login_required
from django.utils.http import urlquote

from accounts.forms.stall import \
    AppearanceForm, PaymentForm, PolicyTemplateForm, OptionsForm
from marketplace.models import Stall, ShippingProfile
from marketplace.forms import StallOwnerProfileForm

from main.utils.decorators import view_dispatch_decorator

from accounts.models import UserProfile

logger = logging.getLogger(__name__)


@view_dispatch_decorator(login_required)
class AccountStallBaseView(UpdateView):
    model = Stall

    def get_object(self, queryset=None):
        try:
            return self.request.user.stall
        except Stall.DoesNotExist:
            return None

    def get_success_url(self):
        return self.request.path

    def get_context_data(self, **kwargs):
        context = super(AccountStallBaseView, self).get_context_data(**kwargs)
        context['base'] = 'Params of base'
        return context

    def render_to_response(self, request, *args, **kwargs):
        if not self.get_object():
            return redirect('create_stall')

        return super(
            AccountStallBaseView,
            self).render_to_response(request, *args, **kwargs)


class AccountStallTabRedirectView(RedirectView):
    permanent = False
    query_string = True

    def get_redirect_url(self):
        return reverse('stall_appearance')


class AccountStallShippingView(AccountStallBaseView):
    template_name = "accounts/stall/shipping.html"

    def get_context_data(self, **kwa):
        profiles = ShippingProfile.objects.filter(
            stall=self.request.user.stall)
        return {
            'profiles': profiles}


class AccountStallAppearanceView(AccountStallBaseView):
    form_class = AppearanceForm
    template_name = "accounts/stall/appearance.html"


class AccountStallAddressView(AccountStallBaseView):
    model = UserProfile
    form_class = StallOwnerProfileForm
    template_name = "accounts/stall/stall_form.html"

    def get_object(self, queryset=None):
        try:
            return self.request.user.user_profile
        except Stall.DoesNotExist:
            return None


class AccountStallPaymentView(AccountStallBaseView):
    form_class = PaymentForm
    template_name = "accounts/stall/payment.html"

    def get_context_data(self, **kwargs):
        context = super(AccountStallPaymentView, self).get_context_data(**kwargs)
        context['hold_fire'] = self.request.GET.get('add-product') is not None
        return context


class AccountStallPoliciesView(AccountStallBaseView):
    form_class = PolicyTemplateForm
    template_name = "accounts/stall/policies.html"


class AccountStallFaqView(AccountStallBaseView):
    template_name = "accounts/stall/faq.html"


class AccountStallOptionsView(AccountStallBaseView):
    form_class = OptionsForm
    template_name = "accounts/stall/options.html"
