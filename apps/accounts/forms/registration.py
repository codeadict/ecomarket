from django import forms

from django.core.exceptions import MultipleObjectsReturned

from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from spamish.utils import run_validators
from accounts.forms import account
from accounts.models import UserProfile

attrs_dict = {'class': 'required'}


class RegistrationForm(account.AccountForm):

    MIN_PASSWORD_LENGTH = 5

    password = forms.CharField(max_length=128,
        widget=forms.PasswordInput(render_value=False))
    password_confirm = forms.CharField(max_length=128,
        widget=forms.PasswordInput(render_value=False))

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            User.objects.get(email=email)
        except MultipleObjectsReturned:
            pass
        except User.DoesNotExist:
            return email.lower()
        raise forms.ValidationError('A user with this email already exists.')

    def clean_username(self):
        """ Check that the username doesn't already exist. """
        username = self.cleaned_data['username']
        try:
            User.objects.get(username__iexact=username)
        except User.DoesNotExist:
            return run_validators(username)
        raise forms.ValidationError('A user has already taken that username.')

    def clean_password(self):
        """ """
        password = self.cleaned_data.get('password', None)
        if len(password) < self.MIN_PASSWORD_LENGTH:
            raise forms.ValidationError(_("Password must be at least 5 chars."))
        if password == self.cleaned_data.get('username', None):
            raise forms.ValidationError(_("Password and username cannot be the same"))
        return password

    def clean_password_confirm(self):
        password = self.cleaned_data.get("password", "")
        password2 = self.cleaned_data.get("password_confirm")
        if password != password2:
            raise forms.ValidationError("The password fields didn't match.")
        return password2

    def save(self):
        return UserProfile.objects.create_user(**self.cleaned_data)
