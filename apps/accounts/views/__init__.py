import datetime
import logging
from operator import truth
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import password_reset_confirm
from django.core.urlresolvers import reverse
from django.utils import simplejson
from django.contrib import messages

from notifications import Events

from django.db import transaction

from django.shortcuts import render, redirect
from django.views.generic.base import TemplateView

from django.contrib import messages
from django.contrib.auth import (login as auth_login, logout as auth_logout,
                                 authenticate)
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect

from notifications import Events
from mailing_lists.models import MailingListSignup
from todos.decorators import ignore_todos

from accounts.forms import RegistrationForm, UserProfileForm, LoginForm
from accounts.models import UserProfile

from marketplace import CURRENCY_CHOICES

logger = logging.getLogger(__name__)

SESSION_EXPIRY = 30 * 24 * 60 * 60  # One month
REGISTER_SUCCESS_MESSAGE = (
    'Thanks! We have sent you an email to verify your account, when you get a '
    'moment in the next few days if you could click the link in this email then your '
    'account will be activated. In the mean time you can carry on using the site as '
    'per normal.')


def login(request, template_name='accounts/login.html'):
    """
    Allow a user to log in with either username/email and password.

    """
    next_url = request.REQUEST.get('next')
    context = {
        'next': next_url,
        'social_login_error': int(request.GET.get('social-login-error', 0)),
    }

    data = request.POST or None
    login_form = LoginForm(data=data)

    redirect_to = next_url or '/'
    if request.user.is_authenticated():
        return redirect(redirect_to)

    if login_form.is_valid():
        username = login_form.cleaned_data.get('username', None)
        password = login_form.cleaned_data.get('password', None)

        user = authenticate(username=username, password=password)
        login_success = user and not user.is_anonymous()
        if login_success:
            auth_login(request, user)            
            Events(request).logged_in(user)
            if not request.POST.get('remember_me', None):
                expiry = 0
            else:
                expiry = SESSION_EXPIRY

            request.session.set_expiry(expiry)
            return redirect(redirect_to)

    context.update({'login_form': login_form})
    return render(request, template_name, context)


@ignore_todos
@login_required
def logout(request):
    """Logs the user out."""
    next_url = request.REQUEST.get('next', 'home')
    auth_logout(request)
    return redirect(next_url)


def register(request, template_name='accounts/register.html'):
    """
    Allow a user to register an account.

    :returns:
        A :py:class:`!django.http.HttpResponse` on GET, which renders a
        registration form.
        A :py:class:`!django.http.HttpResponseRedirect on successful POST,
        which redirects to the 'success' view.
    """
    context = {}
    post_signup_url = request.REQUEST.get('next') or 'register_success'
    if "post_signup_url" in request.session:
        post_signup_url = request.session["post_signup_url"]

    reg_form = RegistrationForm(request.POST or None)
    profile_form = UserProfileForm(request.POST or None)
    if reg_form.is_valid() and profile_form.is_valid():
        user = reg_form.save()
        if user.user_profile is not None:
            # Re-make the profile form against the auto-created user profile
            profile_form = UserProfileForm(request.POST,
                                           instance=user.user_profile)

        user_profile = profile_form.save(commit=False)
        user_profile.user = user
        user_profile.activation_key = user_profile.generate_activation_key()
        user_profile.detected_country = request.country
        user_profile.preferred_currency = request.session.get('preferred_currency', '')
        user_profile.save()
        Events(request).user_signup(user)
        
        # logging him in
        user.backend = 'django.contrib.auth.backends.ModelBackend'
        auth_login(request, user)

        request.session['new_user'] = True
        messages.success(request, REGISTER_SUCCESS_MESSAGE)
        return redirect(post_signup_url)

    context.update({'reg_form': reg_form, 'profile_form': profile_form})
    return render(request, template_name, context)


def quick_signup_login(request, next_url=None):
    if "next_url" in request.REQUEST:
        next_url = request.REQUEST["next_url"]
        request.session["post_signup_url"] = next_url
    return redirect('login')


@ignore_todos
@transaction.commit_on_success
def verify(request, token):
    """
    Verifies a user's account.
    """
    logger.info('Attempting verification for {0}'.format(token))
    user = UserProfile.objects.activate_user(token)
    if user:
        logger.info('User has been verified with token {0}'.format(token))
        # Hack, so we can manually log the user in on verification
        # without requiring them to type their password in.
        user.backend = 'django.contrib.auth.backends.ModelBackend'
        auth_login(request, user)
        user.todos.filter(view_name='validate_email').delete()
        return redirect('verify_success')
    else:
        logger.info('User could not be verified with token {0}'.format(token))
        # insert a verification failed page.
        return redirect('verify_failure')


# Accounts tabs
class AccountPromotionBaseView(TemplateView):
    def get_context_data(self, **kw):
        context = super(AccountPromotionBaseView, self).get_context_data(**kw)
        context['base'] = 'Params of base'
        return context


class AccountPromotionDiscountsView(AccountPromotionBaseView):
    template_name = "accounts/fragments/promotion/discounts.html"

    def get_context_data(self, **kwargs):
        superclass = super(AccountPromotionDiscountsView, self)
        context = superclass.get_context_data(**kwargs)
        context['no_base'] = 'Params of no_base'
        return context


class AccountPromotionStallStoryView(AccountPromotionBaseView):
    template_name = "accounts/fragments/promotion/stall_story.html"

    def get_context_data(self, **kwargs):
        superclass = super(AccountPromotionStallStoryView, self)
        context = superclass.get_context_data(**kwargs)
        context['no_base'] = 'Params of no_base'
        return context


class AccountPromotionWelcomeVideoView(AccountPromotionBaseView):
    template_name = "accounts/fragments/promotion/welcome_video.html"

    def get_context_data(self, **kwargs):
        superclass = super(AccountPromotionWelcomeVideoView, self)
        context = superclass.get_context_data(**kwargs)
        context['no_base'] = 'Params of no_base'
        return context


def save_currency_preference(request):
    currency = request.GET.get('currency', None)
    status = dict()
    if currency in [cur_choice[0] for cur_choice in CURRENCY_CHOICES]:
        status['valid_request'] = True
        request.session['preferred_currency'] = currency
        if request.user.is_authenticated():
            status['user'] = True
            user_profile = request.user.get_profile()
            user_profile.preferred_currency = currency
            user_profile.save()
    return HttpResponse(simplejson.dumps(status), mimetype='application/json')


def custom_password_reset_confirm(request, **kwargs):
    """
    The default django password_reset_confirm only returns an empty form when
    the token is invalid. This custom method calls the default one, checks if the form
    is empty and sends the user back to the password reset page.

    :param request:
    :param kwargs: default kwargs for password_reset_confirm
    :return:
    """
    output = password_reset_confirm(request, **kwargs)
    try:
        if not output.context_data['form']:
            messages.error(request, "Sorry something went wrong here and we couldn't carry out "
                                    "this password reset. It's likely that the link you clicked "
                                    "was too old and had expired. You can try again on this page.")
            return HttpResponseRedirect(
                reverse('password_reset')
            )
    except AttributeError:
        pass

    return output
