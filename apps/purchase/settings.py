from django.conf import settings
from money.Money import CURRENCY


PAYPAL_SANDBOX = getattr(settings, "PAYPAL_SANDBOX", True)

if PAYPAL_SANDBOX:
    PAYPAL_ENDPOINT = 'https://svcs.sandbox.paypal.com/AdaptivePayments/'
    PAYPAL_PAYMENT_HOST = 'https://www.sandbox.paypal.com/au/cgi-bin/webscr'
    PAYPAL_PREAPPROVAL_HOST = 'https://www.sandbox.paypal.com/webscr'
    EMBEDDED_ENDPOINT = 'https://www.sandbox.paypal.com/webapps/adaptivepayment/flow/pay'
    PAYPAL_APPLICATION_ID = 'APP-80W284485P519543T'  # sandbox only
else:
    PAYPAL_ENDPOINT = 'https://svcs.paypal.com/AdaptivePayments/'  # production
    PAYPAL_PAYMENT_HOST = 'https://www.paypal.com/webscr'  # production
    EMBEDDED_ENDPOINT = 'https://paypal.com/webapps/adaptivepayment/flow/pay'
    PAYPAL_APPLICATION_ID = settings.PAYPAL_APPLICATION_ID

 # These settings are required
PAYPAL_USERID = settings.PAYPAL_USERID
PAYPAL_PASSWORD = settings.PAYPAL_PASSWORD
PAYPAL_SIGNATURE = settings.PAYPAL_SIGNATURE
PAYPAL_EMAIL = settings.PAYPAL_EMAIL

USE_IPN = getattr(settings, 'PAYPAL_USE_IPN', False)
SHIPPING = getattr(settings, 'PAYPAL_USE_SHIPPING', False)

PAYPAL_COMMISION = getattr(settings, 'PAYPAL_COMMISION', 0)  # in percentage
DEFAULT_CURRENCY_CODE = getattr(settings, 'DEFAULT_CURRENCY_CODE', 'GBP')
DEFAULT_CURRENCY = CURRENCY[DEFAULT_CURRENCY_CODE]
