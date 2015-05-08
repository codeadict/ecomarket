"""
Classes and helper functions that implement (a portion of) the
Paypal Adaptive API.
"""
import logging
import re
import urllib2

from django.utils import simplejson as json
from pytz import timezone
import requests

from purchase import settings as purchase_settings

logger = logging.getLogger(__name__)


"""
IPN constants
"""
IPN_TYPE_PAYMENT = 'Adaptive Payment PAY'
IPN_TYPE_ADJUSTMENT = 'Adjustment'
IPN_TYPE_PREAPPROVAL = 'Adaptive Payment Preapproval'

IPN_STATUS_CREATED = 'CREATED'
IPN_STATUS_COMPLETED = 'COMPLETED'
IPN_STATUS_INCOMPLETE = 'INCOMPLETE'
IPN_STATUS_ERROR = 'ERROR'
IPN_STATUS_REVERSALERROR = 'REVERSALERROR'
IPN_STATUS_PROCESSING = 'PROCESSING'
IPN_STATUS_PENDING = 'PENDING'

IPN_ACTION_TYPE_PAY = 'PAY'
IPN_ACTION_TYPE_CREATE = 'CREATE'

IPN_TXN_STATUS_COMPLETED = 'Completed'
IPN_TXN_STATUS_PENDING = 'Pending'
IPN_TXN_STATUS_REFUNDED = 'Refunded'

IPN_TXN_SENDER_STATUS_SUCCESS = 'SUCCESS'
IPN_TXN_SENDER_STATUS_PENDING = 'PENDING'
IPN_TXN_SENDER_STATUS_CREATED = 'CREATED'
IPN_TXN_SENDER_STATUS_PARTIALLY_REFUNDED = 'PARTIALLY_REFUNDED'
IPN_TXN_SENDER_STATUS_DENIED = 'DENIED'
IPN_TXN_SENDER_STATUS_PROCESSING = 'PROCESSING'
IPN_TXN_SENDER_STATUS_REVERSED = 'REVERSED'
IPN_TXN_SENDER_STATUS_REFUNDED = 'REFUNDED'
IPN_TXN_SENDER_STATUS_FAILED = 'FAILED'

IPN_FEES_PAYER_SENDER = 'SENDER'
IPN_FEES_PAYER_PRIMARYRECEIVER = 'PRIMARYRECEIVER'
IPN_FEES_PAYER_EACHRECEIVER = 'EACHRECEIVER'
IPN_FEES_PAYER_SECONDARYONLY = 'SECONDARYONLY'

IPN_REASON_CODE_CHARGEBACK = 'Chargeback'
IPN_REASON_CODE_SETTLEMENT = 'Settlement'
IPN_REASON_CODE_ADMIN_REVERSAL = 'Admin reversal'
IPN_REASON_CODE_REFUND = 'Refund'

IPN_PAYMENT_PERIOD_NO_PERIOD_SPECIFIED = 'NO_PERIOD_SPECIFIED'
IPN_PAYMENT_PERIOD_DAILY = 'DAILY'
IPN_PAYMENT_PERIOD_WEEKLY = 'WEEKLY'
IPN_PAYMENT_PERIOD_BIWEEKLY = 'BIWEEKLY'
IPN_PAYMENT_PERIOD_SEMIMONTHLY = 'SEMIMONTHLY'
IPN_PAYMENT_PERIOD_MONTHLY = 'MONTHLY'
IPN_PAYMENT_PERIOD_ANNUALLY = 'ANNUALLY'

IPN_PIN_TYPE_NOT_REQUIRED = 'NOT_REQUIRED'
IPN_PIN_TYPE_REQUIRED = 'REQUIRED'

IPN_TIMEZONES = {'PDT': timezone('US/Pacific'),  # TODO: Change timezone?
                 'PST': timezone('US/Pacific')}

SANDBOX_ENDPOINTS = {
    "PAYPAL_ENDPOINT": 'https://svcs.sandbox.paypal.com/AdaptivePayments/',
    "PAYPAL_PAYMENT_HOST": 'https://www.sandbox.paypal.com/cgi-bin/webscr',
    "PAYPAL_PREAPPROVAL_HOST": 'https://www.sandbox.paypal.com/webscr',
    "EMBEDDED_ENDPOINT": 'https://www.sandbox.paypal.com/webapps/adaptivepayment/flow/pay',
}

PRODUCTION_ENDPOINTS = {
    "PAYPAL_ENDPOINT": 'https://svcs.paypal.com/AdaptivePayments/',  # production
    "PAYPAL_PAYMENT_HOST": 'https://www.paypal.com/cgi-bin/webscr',  # production
    "EMBEDDED_ENDPOINT": 'https://paypal.com/webapps/adaptivepayment/flow/pay',
}


class Pay(object):
    pass


class ChainedPayment(Pay):
    #TODO Get rid of this monstrosity and move the interaction with
    #     the paypal API onto the Client class.
    """Models the chained payment method."""

    def __init__(self, receiver_email, amount, discount_amount, remote_address,
                 return_url, cancel_url, ipn_url=None):
        """Wrapper for Pay(PAY_PRIMARY) API operation and pays the
        primary receiver.

        Handle the secondary receiver payments separately.

        Required Arguments:
        receiver_email : The email of the seller/stall owner.
          Eg. 'seller1@gmail.com',
        amount : Total price of products + delivery. Eg. Money("5", currency)

        Note:
        * Ecomarket paypal email(in settings.py) is set as the default primary
          receiver.
        * The amount to primary receiver is the main amount that is passed to
          this method.
        * To calculate the actual amount sent to secondary receiver, the
          commission is deducated automatically. Do not pre-deduct it from the
          amount param.

        """
        headers = _build_headers(remote_address)
        params = {
            'actionType': 'PAY_PRIMARY',
            'currencyCode': purchase_settings.DEFAULT_CURRENCY_CODE,
            'returnUrl': return_url,
            'cancelUrl': cancel_url,
            'feesPayer': "PRIMARYRECEIVER",
            'ipnNotificationUrl': ipn_url,
            'requestEnvelope': {
                # It appears no other  lanuages are
                # supported
                'errorLanguage': 'en_US',
                'detailLevel': 'ReturnAll'
            },
            'receiverList': {'receiver': []}  # Start with empty receiver list
        }

        receiver_param_list = []

        # Add primary receiver
        receiver_param_list.append(
            {
                'email': purchase_settings.PAYPAL_EMAIL,
                'amount': unicode(amount.amount),
                'primary': 'true'
            }
        )

        # Calculate undiscounted amount
        total_amount = amount + discount_amount

        # Add secondary receiver
        # We don't necessarily receive all of this commission (some of it may
        # have already disappeared due to discount)
        commission = round(
            total_amount * (purchase_settings.PAYPAL_COMMISION / 100.0), 2)
        secondary_amount = total_amount - commission
        logger.debug("Commision is {0}".format(commission))
        logger.debug("secondary amount is {0}".format(secondary_amount))
        receiver_param_list.append(
            {
                'email': receiver_email,
                'amount': unicode(secondary_amount.amount),
                'primary': 'false'
            }
        )

        params['receiverList']['receiver'] = receiver_param_list

        self.raw_request = json.dumps(params)
        url = "{0}{1}".format(purchase_settings.PAYPAL_ENDPOINT, 'Pay')
        logger.debug("Making request to paypal PAY operation. "
                     "url is: {0}, data is {1} and headers are {2}".format(
                         url, self.raw_request, headers))
        self.raw_response = url_request(
            url,
            data=self.raw_request,
            headers=headers
        ).content
        self.response = json.loads(self.raw_response)

        logger.debug('headers are: %s' % headers)
        logger.debug('request is: %s' % self.raw_request)
        logger.debug('response is: %s' % self.raw_response)

        if 'responseEnvelope' not in self.response \
            or 'ack' not in self.response['responseEnvelope'] \
            or (self.response['responseEnvelope']['ack'] not
                in ['Success', 'SuccessWithWarning']):

            error_message = 'unknown'
            error_id = None
            try:
                error_message = self.response['error'][0]['message']
                error_id = self.response['error'][0]['errorId']
            except Exception:
                pass

            raise PayError(error_message, error_id=error_id)

    @property
    def status(self):
        return self.response.get('paymentExecStatus', None)

    @property
    def paykey(self):
        return self.response.get('payKey', None)


class ShippingAddress(object):
    def __init__(self, paykey, remote_address):
        headers = _build_headers(remote_address)
        data = {'key': paykey,
                'requestEnvelope': {'errorLanguage': 'en_US'}}

        self.raw_request = json.dumps(data)
        url = "{0}{1}".format(
            purchase_settings.PAYPAL_ENDPOINT,
            'GetShippingAddresses'
        )
        self.raw_response = url_request(
            url,
            data=self.raw_request,
            headers=headers
        ).content
        logging.debug('response was: %s' % self.raw_response)
        self.response = json.loads(self.raw_response)


#  Error classes
class PaypalAdaptiveApiError(RuntimeError):
    def __init__(self, message, error_id=None):
        super(PaypalAdaptiveApiError, self).__init__(message)
        self.error_id = error_id


class IpnVerificationError(RuntimeError):
    pass


class PayError(PaypalAdaptiveApiError):
    pass


class IpnError(PaypalAdaptiveApiError):
    pass


# Helpers
def _build_headers(remote_address=None):
    headers = {
        'X-PAYPAL-SECURITY-USERID': purchase_settings.PAYPAL_USERID,
        'X-PAYPAL-SECURITY-PASSWORD': purchase_settings.PAYPAL_PASSWORD,
        'X-PAYPAL-SECURITY-SIGNATURE': purchase_settings.PAYPAL_SIGNATURE,
        'X-PAYPAL-REQUEST-DATA-FORMAT': 'JSON',
        'X-PAYPAL-RESPONSE-DATA-FORMAT': 'JSON',
        'X-PAYPAL-APPLICATION-ID': purchase_settings.PAYPAL_APPLICATION_ID,
        #'X-PAYPAL-SERVICE-VERSION': '1.8.1',
    }
    if remote_address:
        headers['X-PAYPAL-DEVICE-IPADDRESS'] = remote_address

    return headers


class url_request(object):
    """
    Wrapper for urllib2
    """
    def __init__(self, url, data=None, headers={}):
        # urllib - not validated
        request = urllib2.Request(url, data=data, headers=headers)

        try:
            self._response = urllib2.urlopen(request).read()
            self._code = 200
        except urllib2.URLError, e:
            self._response = e.read()
            self._code = e.code

    @property
    def content(self):
        return self._response

    @property
    def code(self):
        return self._code


class Client(object):
    """Interface to the paypal API"""

    def __init__(self, user_id, password, signature, app_id, sandbox=True):
        self.user_id = user_id
        self.password = password
        self.signature = signature
        self.app_id = app_id
        self.sandbox = sandbox

    def _get_endpoint(self):
        if self.sandbox:
            return SANDBOX_ENDPOINTS["PAYPAL_ENDPOINT"]
        else:
            return PRODUCTION_ENDPOINTS["PAYPAL_ENDPOINT"]

    def _get_payment_host(self):
        if self.sandbox:
            return SANDBOX_ENDPOINTS["PAYPAL_PAYMENT_HOST"]
        else:
            return PRODUCTION_ENDPOINTS["PAYPAL_PAYMENT_HOST"]

    def _build_headers(self, remote_address=None):
        headers = {
            'X-PAYPAL-SECURITY-USERID': self.user_id,
            'X-PAYPAL-SECURITY-PASSWORD': self.password,
            'X-PAYPAL-SECURITY-SIGNATURE': self.signature,
            'X-PAYPAL-REQUEST-DATA-FORMAT': 'JSON',
            'X-PAYPAL-RESPONSE-DATA-FORMAT': 'JSON',
            'X-PAYPAL-APPLICATION-ID': self.app_id,
        }
        if remote_address:
            headers['X-PAYPAL-DEVICE-IPADDRESS'] = remote_address
        return headers

    def _do_call(self, url, data):
        data["requestEnvelope"] = {
            "detailLevel": "ReturnAll",
            "errorLanguage": "en_US",
        }
        headers = self._build_headers()
        response = requests.post(url, data=json.dumps(data),
                                 headers=headers)
        if "error" in response.json:
            error_id = response.json["error"][0]["errorId"]
            error_message = response.json["error"][0]["message"]
            raise PaypalAdaptiveApiError("Error calling paypal api, message was"
                                      " {0}. errorId was {1}".format(
                                          error_message,
                                          error_id),
                                          error_id=error_id)
        return response

    def refund(self, pay_key, amount=None, receiver_email=None,
               currency_code="GBP"):
        """Performs a refund, raises an error if paypal retunrs one
        but otherwise returns the parsed data response.

        If amount is not specified then the entire payment is refunded

        :param pay_key: The payKey of the payment to be refunded.
        :param amount: float of the amount to refund.
        :param receiver_email: The paypal email address of the receiver to refund.

        """
        data = {
            "currencyCode": currency_code,
            "payKey": pay_key,
            "requestEnvelope": {
                "detailLevel": "ReturnAll",
                "errorLanguage": "en_US",
            }
        }
        if amount:
            if receiver_email is None:
                raise RuntimeError("You must specify a receiver email when "
                                   "specifying an amount to refund")
            data["receiverList"] = [{
                "email": receiver_email,
                "amount": amount
            }]
        endpoint = "{0}Refund".format(self._get_endpoint())
        response = self._do_call(endpoint, data)
        return response.json

    def execute_payment(self, pay_key):
        data = {
            "payKey": pay_key
        }
        endpoint = "{0}ExecutePayment".format(self._get_endpoint())
        response = self._do_call(endpoint, data)
        return response.json

    def payment_details(self, pay_key):
        """Get the payment details for a payment

        :param pay_key: The pay key of the payment
        """
        data = {
            "payKey": pay_key
        }
        endpoint = "{0}PaymentDetails".format(self._get_endpoint())
        response = self._do_call(endpoint, data)
        return response.json

    def validate_ipn(self, raw_data):
        """Validates ipn data returns true if valid, false otherwise

        :param raw_data: should be the data that was
        posted to the handler exactly as it was posted. i.e do not
        parse it, keys have to be in the same order as they were posted.
        """
        url = self._get_payment_host()
        url += "?cmd=_notify-validate&{0}".format(raw_data)
        r = requests.get(url)
        if r.content == "VERIFIED":
            return True
        elif r.content == "INVALID":
            return False
        else:
            raise IpnVerificationError("Error sending verification request to "
                                       "IPN url, response content was {0}"
                                       .format(r.content))

    def parse_ipn(self, data):
        """Parse the dictionary of form data passed to an IPN handler into
        a nested dictionary. This is necessary because paypal represents transactions
        as keys like 'transaction[0].status' when we want to deal with a dictionary
        of transaction dictionaries.
        """
        # This would be much better done with a proper parse, but hey.
        result = {}
        transactions = {}
        id_reg = re.compile("\[(\d+)\]")
        for key, value in data.items():
            if key.startswith("transaction"):
                match = id_reg.search(key)
                if match:
                    index = id_reg.search(key).groups()[0]
                    if index not in transactions:
                        transactions[index] = {}
                    trans_key = key.split(".")[1]
                    trans_value = self._parse_value(value)
                    transactions[index][trans_key] = trans_value
                else:
                    result[key] = self._parse_value(value)
            else:
                result[key] = self._parse_value(value)
        result["transactions"] = []
        for key, value in transactions.items():
            result["transactions"].append(value)
        return result

    def _parse_value(self, value):
        if value == 'false':
            return False
        if value == 'true':
            return True
        return value
