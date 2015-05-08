from django import forms
from django.core.exceptions import MultipleObjectsReturned
from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe

from accounts.models import User

from mailing_lists.constants import LeadSources
from mailing_lists.models import MailingListSignup


class MailingListSignupExists(Exception):

    pass


class EmailSignupForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(EmailSignupForm, self).__init__(*args, **kwargs)
        self.fields["email_address"].widget.attrs["placeholder"] = \
            "Type in your email address here..."
        self.fields["email_address"].error_messages = {
            'required': 'Please enter an email address.',
            'invalid': 'A valid email address is required.',
        }
        self.fields["source"].widget = forms.HiddenInput()
        self.fields["source"].initial = LeadSources.GATE_MODAL
        self.fields["marketing_optin"].widget.attrs["class"] = "pull-left"

    class Meta:
        model = MailingListSignup
        fields = ('email_address', 'source', 'marketing_optin')

    def clean_email_address(self):
        err = mark_safe('This email is already registered, would you like to '
                        '<a href="#" data-toggle="modal" data-target="#login"'
                        'data-dismiss="modal">'
                        'login</a>?')
        email = self.cleaned_data.get('email_address')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(err)
        if MailingListSignup.objects.filter(email_address=email).exists():
            raise MailingListSignupExists()
        return email


def generate_username(user_obj, i):
    username = '%s-%s%s' % (user_obj.first_name, user_obj.last_name, i)
    if User.objects.filter(username=username).exists():
        return generate_username(user_obj, i + 1)
    else:
        return username


class QuickRegistrationForm(forms.ModelForm):
    """ This is a quick form for use on the capture modal.
        auto generates a username
    """
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

    MIN_PASSWORD_LENGTH = 5

    GENDER_MALE = 'm'
    GENDER_FEMALE = 'f'
    GENDER_UNKNOWN = 'x'
    GENDER_CHOICES = (
        (GENDER_UNKNOWN, "I'd rather not say"),
        (GENDER_MALE, "Male"),
        (GENDER_FEMALE, "Female"),
    )

    password = forms.CharField(max_length=128,
        widget=forms.PasswordInput(render_value=False))
    email = forms.EmailField(widget=forms.HiddenInput())
    marketing_optin = forms.CharField(widget=forms.HiddenInput())
    gender = forms.ChoiceField(choices=GENDER_CHOICES)
    first_name = forms.CharField(required=True, error_messages={
            'reduired': 'Please enter you first name.'
        })
    last_name = forms.CharField(required=True, error_messages={
            'reduired': 'Please enter you last name.'
        })

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            User.objects.get(email=email)
        except MultipleObjectsReturned:
            pass
        except User.DoesNotExist:
            return email.lower()
        raise forms.ValidationError('A user with this email already exists.')

    def clean_password(self):
        """ """
        password = self.cleaned_data.get('password', None)
        if len(password) < self.MIN_PASSWORD_LENGTH:
            raise forms.ValidationError(
                _("Password must be at least 5 chars."))
        if password == self.cleaned_data.get('username', None):
            raise forms.ValidationError(
                _("Password and username cannot be the same"))
        return password

    def save(self, force_insert=False, force_update=False, commit=True):
        user = super(QuickRegistrationForm, self).save(commit=False)
        user.username = generate_username(user, 0)
        user.set_password(self.cleaned_data.get('password'))
        if commit:
            user.save()
        return user


class BulkUpdateForm(forms.Form):

    csv_file = forms.FileField(label="CSV File")

    def clean_csv_file(self):
        data = self.cleaned_data["csv_file"]
        csv_content_types = ["text/csv", "text/comma-separated-values"]
        if data.content_type not in csv_content_types:
            raise forms.ValidationError(
                "This file does not look like a CSV file")
        return data
