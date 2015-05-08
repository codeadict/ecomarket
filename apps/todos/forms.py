import django.forms as forms

from django.core.exceptions import ValidationError

from django.contrib.auth.models import User

from accounts.forms.account import AccountForm
from accounts.models import UserProfile
from marketplace.forms import PhoneValidatorMixin
from marketplace.models import Stall


class CountryForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(CountryForm, self).__init__(*args, **kwargs)
        self.fields["country"].widget.attrs["class"] = "select"

    class Meta:
        model = UserProfile
        fields = ["country"]


class AddPhoneNumbersForm(PhoneValidatorMixin, forms.ModelForm):

    class Meta:
        model = Stall
        fields = ["phone_landline", "phone_mobile"]


class FullNameForm(AccountForm):

    class Meta(AccountForm.Meta):
        fields = ["first_name", "last_name"]


class ChangeEmailAddressForm(forms.ModelForm):

    email = forms.EmailField(label="E-mail address")

    class Meta:
        model = User
        fields = ["email"]

    def clean_email(self):
        value = self.cleaned_data["email"].lower()
        if self.instance and self.instance.pk:
            users = User.objects.exclude(pk=self.instance.pk)
        else:
            users = User.objects
        if users.filter(email=value):
            raise ValidationError("A user with this email already exists")
        return value
