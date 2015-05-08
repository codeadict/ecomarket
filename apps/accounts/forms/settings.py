from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

attrs_dict = {'class': 'required'}


class SettingsForm(forms.ModelForm):

    TYPE_ACCOUNT = (
        ('RU', 'Regular User'),
        ('SO', 'Stall Owner'),
        )

    type_account = forms.CharField(widget=forms.Select(choices=TYPE_ACCOUNT, attrs={'class': ''}))

    def clean_email(self):
        """Validate that the supplied email address is unique for the site."""
        email = self.cleaned_data.get('email', '')
        if User.objects.filter(email__iexact=email).exclude(id=self.instance.id):
            raise forms.ValidationError(
                _("This email address is already in use. Please supply a other."))
        return email.lower()

    def clean_username(self):
        """
        Validate that the username is alphanumeric and is not already
        in use.

        """
        try:
            User.objects.exclude(id=self.instance.id).get(
                username__iexact=self.cleaned_data['username'])
        except User.DoesNotExist:
            return self.cleaned_data['username']
        raise forms.ValidationError(_(u'This username is already taken. Please choose another.'))

    def save(self, *args, **kwargs):
        """
        Update the fields on the related User object as well.
        """
        u = self.instance
        u.username = self.cleaned_data['username']
        u.first_name = self.cleaned_data['first_name']
        u.email = self.cleaned_data['email']
        u.save()
        profile = super(SettingsForm, self).save(*args, **kwargs)
        return profile

    class Meta:
        model = User
        fields = ['first_name', 'username', 'email']

