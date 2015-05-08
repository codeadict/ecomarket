from django import forms
from money.contrib.django.forms.widgets import CurrencySelectWidget


class FixedCurrencyWidget(CurrencySelectWidget):
    """ renders the CurrencySelectWidget without the currency dropwdown """

    def __init__(self, choices=None, attrs=None):
        widgets = (
            forms.TextInput(attrs=attrs),
            forms.TextInput(attrs=attrs))

        forms.MultiWidget.__init__(self, widgets, attrs)

    def format_output(self, rendered_widgets):
        return u''.join(rendered_widgets[0])
