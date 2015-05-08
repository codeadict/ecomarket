from django import forms

from marketplace.models import Stall

from spamish.utils import run_validators


class AppearanceForm(forms.ModelForm):
    class Meta:
        model = Stall
        fields = ('title', 'description_short', 'description_full',)

    field_requirements = {
        'description_short': True,
        'description_full': True,
    }

    def __init__(self, *args, **kwargs):
        super(AppearanceForm, self).__init__(*args, **kwargs)

        for k, v in self.field_requirements.items():
            self.fields[k].required = v

    # Commenting out as part of https://sprint.ly/product/3047/#!/item/750
    # def clean_title(self):
    #     return run_validators(self.cleaned_data['title'])

    # def clean_description_short(self):
    #     return run_validators(self.cleaned_data['description_short'])

    # def clean_description_full(self):
    #     return run_validators(self.cleaned_data['description_full'])


class PaymentForm(forms.ModelForm):
    def clean_paypal_email(self):
        data = self.cleaned_data['paypal_email']
        if len(self.instance.paypal_email) > 0 and len(data) < 1:
            raise forms.ValidationError("Cannot Remove Paypal E-mail")
        return data

    class Meta:
        model = Stall
        fields = ('paypal_email', )


class PolicyTemplateForm(forms.ModelForm):
    class Meta:
        model = Stall
        fields = (
            'message_after_purchasing',
            'refunds_policy', 'returns_policy',)


class OptionsForm(forms.ModelForm):
    class Meta:
        model = Stall
        fields = ('holiday_mode', 'holiday_message', )
