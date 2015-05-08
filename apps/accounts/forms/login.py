from django import forms
from django.contrib.auth.forms import AuthenticationForm

attrs_dict = {'class': 'required'}


class LoginForm(AuthenticationForm):

    username = forms.CharField(max_length=75,required=True)

    password = forms.CharField(max_length=128,
        widget=forms.PasswordInput(render_value=False,
            attrs={'class': 'input-small'}))
    remember_me = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={}),
                             label=u'remember me for 1 month', initial=True)

    def clean_username(self):
        """Convert emails to lowercase to reduce user complaints"""
        value = self.cleaned_data.get('username', '')
        if value and '@' in value:
            value = value.lower()
        return value

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = 'Username or email'
