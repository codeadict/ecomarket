from django.core.urlresolvers import reverse
from django.contrib.auth.forms import PasswordResetForm as AuthPasswordResetForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.models import get_current_site
from django.utils.translation import ugettext_lazy as _
from django.utils.http import int_to_base36
from django.db.models import Q
from django import forms

from notifications import Events
from main.utils import absolute_uri

from accounts.models import User, UserProfile

attrs_dict = {'class': 'required'}

class PasswordResetForm(AuthPasswordResetForm):
    facebook_invalid = False
    email = forms.CharField(max_length=254)

    def clean_email(self):
        email = self.cleaned_data["email"]
        self.users_cache = User.objects.filter(Q(email__iexact=email) | Q(username=email))
        if len(self.users_cache) == 0:
            raise forms.ValidationError(_("That e-mail or surname doesn't have an associated user account. Are you sure you've registered?"))
        for user in self.users_cache:
            profile = UserProfile.objects.get(user=user)
            if profile.social_auth == 'facebook':
                self.facebook_invalid = True
                raise forms.ValidationError(_("Cannot Reset Password"))
        return email

    """
    Form used for 'Forgot your password' feature.
    """
    def save(self, domain_override=None,
             subject_template_name=None,
             email_template_name=None,
             use_https=False, token_generator=default_token_generator,
             from_email=None, request=None):
        """
        Overriding the save function, so we can use our own html email template
        """
        for user in self.users_cache:
            if not domain_override:
                current_site = get_current_site(request)
                site_name = current_site.name
                domain = current_site.domain
            else:
                site_name = domain = domain_override
            
            Events(request).forgot_password(user)
