import re

from django import forms
from django.core import validators

from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from accounts.models import EmailNotification, Privacy
from notifications import Events


class AccountForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(AccountForm, self).__init__(*args, **kwargs)
        self.email_changed = False
        if "first_name" in self.fields:
            self.fields["first_name"].required = True
        if "last_name" in self.fields:
            self.fields["last_name"].required = True
        if "username" in self.fields:
            self.fields["username"].validators.append(
                validators.RegexValidator(re.compile('^[\w.@+-]+$'),
                                          message=_('Enter a valid username.'),
                                          code='invalid')
            )

    def clean_email(self):
        if self.instance is not None:                 
            self.old_email = self.instance.email
            self.new_email = self.cleaned_data['email']            
            self.email_changed = self.old_email != self.new_email

        if self.email_changed:
            if User.objects.filter(email__iexact=self.new_email).count() > 0:
                raise forms.ValidationError(_("Another person with this e-mail address already has an Eco Market account"))

        return self.new_email

    def save(self, *args, **kwargs):
        """
        Notify events subsystem when user changes their e-mail
        This handles updating mailing lists etc.
        """
        result = super(AccountForm, self).save(*args, **kwargs)
        if self.email_changed:
            Events(None).user_changed_email(self.instance, self.old_email, self.new_email)
        return result

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email',)


class EmailNotificationForm(forms.ModelForm):
    class Meta:
        model = EmailNotification
        fields = ('stall_owner_tips',
                  'site_updates_features',
                  'blogs_you_might_like',
                  'product_discounts',
                  'follower_notifications',
                  'products_you_might_like',
                  'private_messages',
                  'orders',
                  'customer_reviews',
                  'share_orders_in_activity_feed')

    def __init__(self, *args, **kwargs):
        super(EmailNotificationForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)

        self.fields['private_messages'].widget.attrs['class'] = 'checkbox eco-checkbox'
        self.fields['orders'].widget.attrs['class'] = 'eco-checkbox checkbox'
        self.fields['customer_reviews'].widget.attrs['class'] = 'eco-checkbox checkbox'
        self.fields['site_updates_features'].widget.attrs['class'] = 'eco-checkbox checkbox'
        self.fields['blogs_you_might_like'].widget.attrs['class'] = 'eco-checkbox checkbox'
        self.fields['stall_owner_tips'].widget.attrs['class'] = 'eco-checkbox checkbox'
        self.fields['product_discounts'].widget.attrs['class'] = 'eco-checkbox checkbox'
        self.fields['follower_notifications'].widget.attrs['class'] = 'eco-checkbox checkbox'
        self.fields['products_you_might_like'].widget.attrs['class'] = 'eco-checkbox checkbox'
        self.fields['share_orders_in_activity_feed'].widget.attrs['class'] = 'eco-checkbox checkbox'
        if instance and instance.id:
            self.fields['private_messages'].required = False
            self.fields['private_messages'].widget.attrs['disabled'] = 'disabled'

            self.fields['orders'].required = False
            self.fields['orders'].widget.attrs['disabled'] = 'disabled'

            self.fields['customer_reviews'].required = False
            self.fields['customer_reviews'].widget.attrs['disabled'] = 'disabled'

    def clean_private_messages(self):
        return self.instance.private_messages

    def clean_orders(self):
        return self.instance.orders

    def clean_customer_reviews(self):
        return self.instance.customer_reviews


class PrivacyForm(forms.ModelForm):
    class Meta:
        model = Privacy
        fields = ('share_purchases_in_activity',
                'love_list_public',
                'share_love_list_in_activity',
                'profile_public'
            )

    def __init__(self, *args, **kwargs):
        super(PrivacyForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)

        self.fields['share_purchases_in_activity'].widget.attrs['class'] = 'checkbox eco-checkbox'
        self.fields['love_list_public'].widget.attrs['class'] = 'checkbox eco-checkbox'
        self.fields['share_love_list_in_activity'].widget.attrs['class'] = 'checkbox eco-checkbox'
        self.fields['profile_public'].widget.attrs['class'] = 'checkbox eco-checkbox'

        if instance and instance.id and instance.user.get_profile().is_seller:
            self.fields['profile_public'].widget.required = False
            self.fields['profile_public'].widget.attrs['disabled'] = 'disabled'

    def clean(self):
        cleaned_data = self.cleaned_data
        instance = getattr(self, 'instance', None)
        if instance and instance.id and instance.user.get_profile().is_seller:
            cleaned_data['profile_public'] = True
        return cleaned_data
