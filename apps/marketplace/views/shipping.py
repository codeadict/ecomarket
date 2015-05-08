from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext as _
from django.shortcuts import redirect
from django.views.generic import UpdateView
from django.utils.datastructures import MultiValueDictKeyError

from marketplace.forms import ShippingProfileForm, \
    ShippingRuleForm, ShippingRulesFormset

from marketplace.models import Stall, Country, ShippingProfile, ShippingRule


class MarketplaceStallBaseView(UpdateView):
    model = Stall

    def get_object(self, queryset=None):
        stall = self.request.user.stall
        return stall

    def get_success_url(self):
        return self.request.path

    def get_context_data(self, **kwargs):
        context = super(
            MarketplaceStallBaseView,
            self).get_context_data(**kwargs)
        context['base'] = 'Params of base'
        return context


class ShippingProfileAjaxView(MarketplaceStallBaseView):
    template_name = "marketplace/shipping/profile.html"

    def get_context_data(self, *la, **kwa):
        profile = None
        try:
            profile_id = self.request.GET['profile']
            profile = ShippingProfile.objects.get(
                id=profile_id, stall=self.request.user.stall)
            shipping_form = ShippingProfileForm(
                instance=profile, prefix='ship_profile')
            rules_formset = ShippingRulesFormset(
                prefix="ship_rules",
                instance=profile)
        except:
            rules_formset = ShippingRulesFormset(
                prefix="ship_rules")
            shipping_form = ShippingProfileForm(
                prefix='ship_profile')

        return {
            'form': shipping_form,
            'rules_formset': rules_formset}


class ShippingProfileJSONView(MarketplaceStallBaseView):
    template_name = "marketplace/shipping/profile.html"
    # adding/deleting


class ShippingProfileRuleAjaxView(MarketplaceStallBaseView):
    template_name = "marketplace/shipping/profile-rule.html"
    model = ShippingRule

    def get_context_data(self, *la, **kwa):
        i = self.request.GET.get('i')
        return {
            'form': ShippingRuleForm(prefix='ship_rule_add_%s' % i or 0)}


def _create_shipping_profile(request):
    # TODO: move this...
    message = ''
    try:
        shipping_profile_name = request.POST['shipping_profile_name']
        shipping_origin = request.POST['shipping_origin']
        success = True
    except MultiValueDictKeyError:
        success = False
        message = _(
            'You must specify a shipping origin and profile name '
            + 'when creating a new profile')

    if success:
        try:
            profile = ShippingProfile.objects.get(
                title=shipping_profile_name,
                stall=request.user.stall)
        except:
            profile = None

        if not profile:
            profile = ShippingProfile(
                stall=request.user.stall,
                title=shipping_profile_name,
                shipping_from=Country.objects.get(code=shipping_origin))
            profile.save()
        else:
            # update the profile
            pass

        # set the profile rules

    context = {
        'success': success,
        'message': message}
    return context


@login_required
def add_shipping_profile(request, *la, **kwa):
    """
    Handles the creation of a shipping profile
    """
    try:
        stall = request.user.stall
    except:
        return redirect('create_stall')

    params = None
    if request.POST:
        params = request.POST.copy()

    form = ShippingProfileForm(
        params, request.FILES or None,
        request=request, stall=stall)

    if request.method == "POST" and form.is_valid():
        form.save()
        form.save_m2m()

    # TODO: add JSON response


@login_required
def delete_shipping_profile(request, *la, **kwa):
    """
    Handles the creation of a shipping profile
    """
