import re
import sys
import inspect
import socket

from django import forms
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _

from .models import BannedWord


class BaseValidator(object):
    """
    This class defines the validator structure for validator classes. It is
    pretty much the same as Django validators.

    Implement the __call__ method in your validator (placed in this module)
    and it will be picked up by the messaging validation code and used for
    validating user messages.

    Make sure you subclass BaseValidator as this is how the validators are
    detected.
    """

    def __call__(self, value):
        """
        Return True/False.
        """
        raise NotImplemented


class UKTelephoneValidator(BaseValidator):
    """
    Rejects message that contains UK telephone numbers.
    """
    default_error = _(u"Please do not include a telephone number in your message.")

    pattern = r'(?:(?:\(?(?:0(?:0|11)\)?[\s-]?\(?|\+)44\)?[\s-]?(?:\(?0\)?[\s-]?)?)|(?:\(?0))(?:(?:\d{5}\)?[\s-]?\d{4,5})|(?:\d{4}\)?[\s-]?(?:\d{5}|\d{3}[\s-]?\d{3}))|(?:\d{3}\)?[\s-]?\d{3}[\s-]?\d{3,4})|(?:\d{2}\)?[\s-]?\d{4}[\s-]?\d{4}))(?:[\s-]?(?:x|ext\.?|\#)\d{3,4})?'
    regex = re.compile(pattern, re.IGNORECASE)

    def __call__(self, value):
        if value and self.regex.search(value):
            raise forms.ValidationError(self.default_error)


class WebsiteValidator(BaseValidator):
    """
    Reject messages that contain website URLs not in the allowed_list.
    """
    default_error = _(u"Sorry but you can't use website links or email addresses "
        "here.")
    allowed_domains = ['ecomarket.com', 'ethicalcommunity.com']

    regex = re.compile(r'([A-Z]+\.)+[A-Z]{2,8}', re.IGNORECASE)

    def _is_active_domain(self, domain):
        """
        Returns True if domain exists; False otherwise.
        """
        try:
            socket.gethostbyname(domain.lower())
            return True
        except socket.gaierror:
            return False

    def __call__(self, value):
        if value:
            # Loop through all domains in value. If at least one isn't in the
            # allowed domains list then value is invalid.
            for m in self.regex.finditer(value):
                url = m.group(0)
                url_valid = False
                for allowed_domain in self.allowed_domains:
                    if allowed_domain.lower() in url.lower():
                        url_valid = True
                        break

                # If statement avoids setting allowed domains to invalid.
                if not url_valid:
                    url_valid = not self._is_active_domain(url)

                if not url_valid:
                    raise forms.ValidationError(self.default_error)


class BannedWordValidator(BaseValidator):
    """
    Rejects if the message contains a word from the banned word list.
    """
    CONTACT_URL = 'http://help.ecomarket.com/'
    default_error = _(mark_safe(u"Whoops, looks like you used a word here that isn't "
                       "allowed. If you think this might have been a mistake "
                       "feel free to <a href='%s'>contact us</a>" % CONTACT_URL))

    def __call__(self, value):
        if not value:
            return
        banned_words = BannedWord.objects.active().values_list('word', flat=True)
        if not banned_words:
            return
        escaped_banned_words = [re.escape(b) for b in banned_words]
        pattern = r'\b(' + r'|'.join(escaped_banned_words) + r')\b'
        regex = re.compile(pattern, re.IGNORECASE)
        m = regex.search(value)
        if m:
            raise forms.ValidationError(self.default_error)
