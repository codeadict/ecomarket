import logging
from operator import contains
import re
from urllib import urlencode
import json

from notifications import Events

from django.views.generic.edit import CreateView
from django.core.urlresolvers import reverse
from django.db import transaction
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.shortcuts import redirect, render

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages

from accounts.models import UserProfile, EmailNotification
from accounts.views import REGISTER_SUCCESS_MESSAGE

from mailing_lists.forms import (EmailSignupForm, QuickRegistrationForm,
                                 MailingListSignupExists)
from mailing_lists.integrations.sailthru import Sailthru, SailthruError

logger = logging.getLogger(__name__)


def sailthru_sync(request):
    """
    This page is used as the 'redirect action' for the SailThru unsubscribe
    page. We then pull the notification settings from SailThru and save them
    to our DB.
    """
    redirect_url = request.META.get('HTTP_REFERER')
    if redirect_url is None or 'link.ecomarket.com' not in redirect_url:
        redirect_url = 'http://www.ecomarket.com/'

    sailthru_id = request.GET.get('id', None)
    if sailthru_id is not None:
        try:
            sailthru_data = Sailthru(request).get_user_data(
                sailthru_id=sailthru_id)
        except SailthruError, e:
            logger.error(e, exc_info=True)
            raise  # TODO remove
        else:
            try:
                user = User.objects.get(email=sailthru_data['keys']['email'])
            except User.DoesNotExist:
                pass
            else:
                # The following variables are forced to enabled:
                #  - customer_reviews (notifications_customer_reviews)
                #  - orders (notifications_orders)
                #  - private_messages (notifications_private_messages)
                lists = sailthru_data.get('lists', {})
                user_notify = EmailNotification.objects.get(user=user)
                user_notify.blogs_you_might_like = contains(
                    lists, 'blogs_you_might_like')
                user_notify.follower_notifications = contains(
                    lists, 'follower_notifications')
                user_notify.product_discounts = contains(
                    lists, 'product_discounts')
                user_notify.products_you_might_like = contains(
                    lists, 'products_you_might_like')
                user_notify.site_updates_features = contains(
                    lists, 'site_updates_features')
                user_notify.stall_owner_tips = contains(
                    lists, 'stall_owner_tips')
                user_notify.save()
    return redirect(redirect_url)


class CreateSignup(CreateView):

    template_name = "mailing_lists/fragments/capture_modals_inner.html"
    form_class = EmailSignupForm

    def form_valid(self, form):
        # discard if notifications are unwanted
        marketing_optin = form.cleaned_data.get('marketing_optin', True)
        form.instance.set_ip_address(self.request)
        mls = form.save()
        # This is used in Campaign Tracking
        self.request.session['email_lead'] = mls.id
        Events(self.request).newsletter_signup(email=mls.email_address)

        url_data = urlencode({
            "marketing_optin": "true" if marketing_optin else "false",
            "email": form.cleaned_data["email_address"],
        })
        return HttpResponseRedirect(reverse("quick_register") + "?" + url_data)

    def post(self, *args, **kwargs):
        try:
            ret = super(CreateSignup, self).post(*args, **kwargs)
            return ret
        except MailingListSignupExists:
            # We're happy, the user's happy, everyone's happy.
            return render(self.request,
                          "mailing_lists/fragments/capture_complete.html")


class BlogSignup(CreateSignup):
    def post(self, *args, **kwargs):
        try:
            super(BlogSignup, self).post(*args, **kwargs)
            data = dict(
                status = 'OK'
            )
            return HttpResponse(json.dumps(data), mimetype="application/json")
        except MailingListSignupExists:
            data = dict(
                status = 'OK'
            )
            return HttpResponse(json.dumps(data), mimetype="application/json")


class QuickRegisterView(CreateView):

    template_name = "mailing_lists/fragments/quick_register.html"
    form_class = QuickRegistrationForm

    def get_initial(self):
        return {
            "email": self.request.GET.get("email", ""),
            "marketing_optin": self.request.GET.get("marketing_optin", True),
        }

    @transaction.commit_on_success
    def form_valid(self, form):
        user = form.save()
        if user.user_profile is None:
            profile = UserProfile(user=user)
        else:
            profile = user.user_profile
        gender = form.cleaned_data.get('gender')
        if gender is not None and not 'x' in gender:
            profile.gender = gender
        profile.send_newsletters = form.cleaned_data.get('marketing_optin') != 'false'
        profile.activation_key = profile.generate_activation_key()
        profile.detected_country = self.request.country
        profile.preferred_currency = self.request.session.get('preferred_currency', '')
        profile.save()

        Events(self.request).user_signup(user)

        # login user
        password = form.cleaned_data.get('password')
        user = authenticate(username=user.username, password=password)
        login(self.request, user)
        messages.success(self.request, REGISTER_SUCCESS_MESSAGE)
        return render(self.request,
                      "mailing_lists/fragments/capture_complete.html")


class BlogQuickRegisterView(QuickRegisterView):
    def post(self, *args, **kwargs):
        try:
            super(BlogQuickRegisterView, self).post(*args, **kwargs)
            data = dict(
                status = 'OK'
            )
            return HttpResponse(json.dumps(data), mimetype="application/json")
        except:
            data = dict(
                status = 'ERROR',
                error = list(
                    'SIGNEDUP'
                )
            )
            return HttpResponse(json.dumps(data), mimetype="application/json")
