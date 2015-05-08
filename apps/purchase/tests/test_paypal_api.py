from django.http import urlencode, QueryDict
from unittest import TestCase
import json
import mock
from purchase.api import Client, PaypalAdaptiveApiError, IpnVerificationError
import requests
from tests import factories
from tests.utils import Matcher
from apps.purchase.tests import utils

def compare_json(expected_dict, other):
    other_dict = json.loads(other)
    return other_dict == expected_dict

def match_any(expected, other):
    return True

class ApiTestCase(TestCase):

    def get_expected_body(self, body_data):
        boilerplate = {
            "requestEnvelope": {
                "errorLanguage": "en_US",
                "detailLevel": "ReturnAll",
            }
        }
        boilerplate.update(body_data)
        return boilerplate

    def setUp(self):
        super(ApiTestCase, self).setUp()
        self.user_id = "someid"
        self.password = "apassword"
        self.signature = "somesignature"
        self.application_id = "anappid"
        self.client = Client(self.user_id, self.password, self.signature,
                             self.application_id, sandbox=False)

class RefundOperationTestCase(ApiTestCase):

    def setUp(self):
        super(RefundOperationTestCase, self).setUp()
        self.pay_key = "some-pay-key"
        self.receiver_email = "somemerchant@sellstuff.com"
        self.amount = 10.0
        self.good_response = json.loads(
            utils.load_fixture("refund_response_good.json"))

    @mock.patch('requests.post')
    def test_headers_correct(self, mock_post):
        expected_headers = {
            'X-PAYPAL-SECURITY-USERID': self.user_id,
            'X-PAYPAL-SECURITY-PASSWORD': self.password,
            'X-PAYPAL-SECURITY-SIGNATURE': self.signature,
            'X-PAYPAL-REQUEST-DATA-FORMAT': 'JSON',
            'X-PAYPAL-RESPONSE-DATA-FORMAT': 'JSON',
            'X-PAYPAL-APPLICATION-ID': self.application_id,
        }
        mock_post.return_value.json = json.dumps(self.good_response)
        result = self.client.refund(self.pay_key)
        mock_post.assert_called_with(mock.ANY,
                                     headers=expected_headers,
                                     data=mock.ANY)

    @mock.patch('requests.post')
    def test_body_correct(self, mock_post):
        expected_request = {
            "currencyCode": "GBP",
            "payKey":self.pay_key,
        }
        expected_request = self.get_expected_body(expected_request)
        mock_post.return_value.json = json.dumps(self.good_response)
        result = self.client.refund(self.pay_key)
        mock_post.assert_called_with(mock.ANY,
                                     data=Matcher(compare_json, expected_request),
                                     headers=mock.ANY)

    @mock.patch('requests.post')
    def test_body_when_amount_specified(self, mock_post):
        expected_request = {
            "currencyCode": "GBP",
            "payKey":self.pay_key,
            "receiverList":[{
                "email": self.receiver_email,
                "amount": 10
            }]
        }
        expected_request = self.get_expected_body(expected_request)
        mock_post.return_value.json = json.dumps(self.good_response)
        result = self.client.refund(
            self.pay_key,
            receiver_email=self.receiver_email,
            amount=10
        )
        mock_post.assert_called_with(mock.ANY,
                                     data=Matcher(compare_json, expected_request),
                                     headers=mock.ANY)

    @mock.patch('requests.post')
    def test_error_thrown_when_amount_specified_without_receiver(self, mock_post):
        with self.assertRaises(RuntimeError):
            self.client.refund(self.pay_key, amount=10)

    @mock.patch('requests.post')
    def test_url_correct(self, mock_post):
        expected_url = "https://svcs.paypal.com/AdaptivePayments/Refund"
        mock_post.return_value.json = json.dumps(self.good_response)
        result = self.client.refund(self.pay_key)
        mock_post.assert_called_with(expected_url,
                                     headers=mock.ANY,
                                     data=mock.ANY)

    @mock.patch('requests.post')
    def test_error_response(self, mock_post):
        bad_response = json.loads(utils.load_fixture("refund_response_bad.json"))
        mock_post.return_value.json = bad_response
        with self.assertRaises(PaypalAdaptiveApiError):
            self.client.refund(self.pay_key)


class ExecutePaymentTestCase(ApiTestCase):

    @mock.patch('requests.post')
    def test_correct_url(self, mock_post):
        expected_url = "https://svcs.paypal.com/AdaptivePayments/ExecutePayment"
        self.client.execute_payment("some-pay-key")
        mock_post.assert_called_with(expected_url,
                                     headers=mock.ANY,
                                     data=mock.ANY)

    @mock.patch('requests.post')
    def test_correct_data(self, mock_post):
        expected_data = {
            "payKey": "some-pay-key"
        }
        expected_body = self.get_expected_body(expected_data)
        self.client.execute_payment("some-pay-key")
        mock_post.assert_called_with(mock.ANY,
                                     headers=mock.ANY,
                                     data=Matcher(compare_json, expected_body))


class PaymentDetailsTestCase(ApiTestCase):

    @mock.patch('requests.post')
    def test_correct_url(self, mock_post):
        expected_url = "https://svcs.paypal.com/AdaptivePayments/PaymentDetails"
        self.client.payment_details("some-pay-key")
        mock_post.assert_called_with(expected_url,
                                     headers=mock.ANY,
                                     data=mock.ANY)

    @mock.patch('requests.post')
    def test_correct_data(self, mock_post):
        expected_data = {
            "payKey": "some-pay-key"
        }
        expected_body = self.get_expected_body(expected_data)
        self.client.payment_details("some-pay-key")
        mock_post.assert_called_with(mock.ANY,
                                     headers=mock.ANY,
                                     data=Matcher(compare_json, expected_body))

class IpnVerificationTestCase(ApiTestCase):

     @mock.patch('requests.get')
     def test_valid_response(self, mock_get):
         data = "mc_gross=19.95&protection_eligibility=Eligible&address_status=confirmed&payer_id=LPLWNMTBWMFAY&tax=0.00&address_street=1+Main+St&payment_date=20%3A12%3A59+Jan+13%2C+2009+PST&payment_status=Completed&charset=windows-1252&address_zip=95131&first_name=Test&mc_fee=0.88&address_country_code=US&address_name=Test+User&notify_version=2.6&custom=&payer_status=verified&address_country=United+States&address_city=San+Jose&quantity=1&verify_sign=AtkOfCXbDm2hu0ZELryHFjY-Vb7PAUvS6nMXgysbElEn9v-1XcmSoGtf&payer_email=gpmac_1231902590_per%40paypal.com&txn_id=61E67681CH3238416&payment_type=instant&last_name=User&address_state=CA&receiver_email=gpmac_1231902686_biz%40paypal.com&payment_fee=0.88&receiver_id=S8XGHLYDW9T3S&txn_type=express_checkout&item_name=&mc_currency=USD&item_number=&residence_country=US&test_ipn=1&handling_amount=0.00&transaction_subject=&payment_gross=19.95&shipping=0.00"
         expected_url = "https://www.paypal.com/cgi-bin/webscr?cmd=_notify-validate&{0}".format(data)
         mock_get.return_value.content = "VERIFIED"
         result = self.client.validate_ipn(data)
         mock_get.assert_called_with(expected_url)
         self.assertTrue(result)

     @mock.patch('requests.get')
     def test_invalid_response(self, mock_get):
         mock_get.return_value.content = "INVALID"
         result = self.client.validate_ipn("ignored data")
         self.assertFalse(result)

     @mock.patch('requests.get')
     def test_error_raised(self, mock_get):
         mock_get.return_value.content = "There was an error"
         with self.assertRaises(IpnVerificationError):
             self.client.validate_ipn("ignored data")

class IpnDataParseTestCase(ApiTestCase):

    def setUp(self):
        super(IpnDataParseTestCase, self).setUp()
        data = json.loads(utils.load_fixture("refund_ipn.json"))
        # Use a querydict as that is what the client object will parse
        # and there are some subtleties to them
        self.data = QueryDict(urlencode(data))


    def test_data_parsed_correctly(self):
        parsed = self.client.parse_ipn(self.data)
        self.assertTrue(len(parsed["transactions"]), 2)
        self.assertEqual(parsed["pay_key"], "AP-32A1235987756532A")

    def test_data_parsed_correctly_for_booleans(self):
        parsed = self.client.parse_ipn(self.data)
        self.assertFalse(parsed["log_default_shipping_address_in_transaction"])



