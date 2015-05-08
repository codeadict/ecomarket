from django import forms

from accounts.models import ShippingAddress


class ShippingAddressForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ShippingAddressForm, self).__init__(*args, **kwargs)
        self.fields['country'].widget.attrs.update({'class': 'select'})

    class Meta:
        model = ShippingAddress
        fields = ('name', 'line1', 'line2', 'city', 'state', 'country', 'postal_code')