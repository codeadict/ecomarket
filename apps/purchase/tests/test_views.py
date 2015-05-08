from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.http import urlencode
from django.utils import unittest
from django.test import TestCase
from apps.accounts.models import UserProfile
from apps.marketplace.models import Stall, Country
from apps.purchase.models import Cart, CartStall, ShippingAddress, Order, \
        Payment, PaymentAttempt
from purchase.api import PayError
from apps.purchase import views
from tests import factories
from purchase.tests import utils

import json
import mock
import money
import purchase.models
import purchase.views


class ShippingViewTestCase(TestCase):

    def setUp(self):
        self.merchant = User.objects.create_user("merchantname",
                                                 password="apassword")
        self.merchant_profile = UserProfile.objects.create(user=self.merchant)

        self.user = User.objects.create_user("ausername", password="apassword")
        self.user_profile = UserProfile.objects.create(user=self.user)
        self.country = Country.objects.get(code="GB")
        self.shipping_address = ShippingAddress.objects.create(
            line1="address line 1",
            line2="address line 2",
            city="London",
            state="London",
            postal_code="e11uy",
            user=self.user,
            country=self.country,
        )

        self.cart = self.user.cart
        self.stall = Stall.objects.create(user=self.merchant)
        self.cart_stall = CartStall.objects.create(cart=self.cart,
                                                   stall=self.stall)

        self.view_url = reverse("checkout_shipping_stall",
                                kwargs={"stall_id": self.cart_stall.stall_id})

    def login(self):
        self.client.login(username="ausername", password="apassword")

    def do_logged_in_get(self):
        self.login()
        response = self.client.get(self.view_url)
        return response

    def test_with_create_form_creates_shipping_address(self):
        self.client.login(username="ausername", password="apassword")
        response = self.client.post(
            self.view_url,
            data={"shipping_address_id": self.shipping_address.id}
        )
        cart_stall = CartStall.objects.get(id=self.cart_stall.id)
        self.assertEqual(cart_stall.address, self.shipping_address)

    def test_get_returns_existing_shipping_addresses(self):
        response = self.do_logged_in_get()
        self.assertEqual(len(response.context["shipping_addresses"]), 1)
        self.assertEqual(response.context["shipping_addresses"][0].id,
                         self.shipping_address.id)

    def test_get_returns_shipping_address_form(self):
        response = self.do_logged_in_get()
        self.assertIsNotNone(response.context["address_form"])

    def test_with_new_address_creates_new_address(self):
        country = Country.objects.get(code="GB")
        data = {
            "name": "home",
            "line1": "A Place Somewhere",
            "line2": "Probably a village",
            "city": "Dorchester",
            "state": "Dorset",
            "postal_code": "DT1178T",
            "country": country.id
        }
        self.login()
        response = self.client.post(self.view_url, data=data)
        shipping_addresses = self.user.addresses.all()
        self.assertEqual(len(shipping_addresses), 2)
        new_address = self.user.addresses.get(line1=data["line1"])
        cart_stall = CartStall.objects.get(id=self.cart_stall.id)
        self.assertEqual(cart_stall.address, new_address)

    def test_new_address_invalid_data_returns_to_shipping_with_errors(self):
        data = {"line1": "the only bit of data"}
        self.login()
        response = self.client.post(self.view_url, data=data)
        self.assertTemplateUsed(response, "purchase/checkout_shipping.html")
        self.assertTrue(len(response.context["address_form"].errors) > 0)

    def test_shipping_address_with_invalid_country_returns_to_shipping(self):
        country2 = factories.CountryFactory(code="NL")
        data = {
            "name": "home",
            "line1": "A Place Somewhere",
            "line2": "Probably a village",
            "city": "Dorchester",
            "state": "Dorset",
            "postal_code": "DT1178T",
            "country": country2.id
        }
        product = factories.ProductFactory()
        self.cart.add(product)
        self.login()
        with mock.patch.object(purchase.models.CartStall, 'set_address') as mock_set_country:
            mock_set_country.side_effect = purchase.models.UnavailableShippingCountryError
            response = self.client.post(self.view_url, data=data)
            self.assertTemplateUsed('purchase/checkout_shipping.html')
            cart_stall = CartStall.objects.get(stall=product.stall, cart=self.cart)
            # Check that the address has not been updated
            self.assertIsNone(cart_stall.address)
            self.assertEqual(len(response.context['messages']), 1)

    def test_shipping_address_with_mismatching_country_returns_to_shipping(self):
        address = factories.ShippingAddressFactory(user=self.user)
        product = factories.ProductFactory()
        self.cart.add(product)
        self.cart_stall.speculative_country = Country.objects.get(code="GB")
        self.cart_stall.save()
        self.login()
        with mock.patch.object(purchase.models.CartStall, 'set_address') as mock_set_country:
            mock_set_country.side_effect = purchase.models.MismatchingCountryError
            data = {"shipping_address_id": address.id}
            response = self.client.post(self.view_url, data=data)
            self.assertTemplateUsed('purchase/checkout_shipping.html')
            self.assertTrue(len(response.context['messages']), 1)



@mock.patch('purchase.models.notifier.send_merchant_order_complete')
@mock.patch('purchase.models.notifier.send_customer_order_complete')
class PaymentReturnTestCase(TestCase):
    # This is a smoke test, needs a lot more work
    # TODO write exhaustive test cases for payment scenarios


    def setUp(self):
        super(PaymentReturnTestCase, self).setUp()
        self.cart_stall = factories.create_cart_stall()
        self.cart_stall.delivery_total = mock.MagicMock()
        self.cart_stall.delivery_total.return_value = money.Money(10, "GBP")
        self.user = self.cart_stall.cart.user
        self.payment = factories.PaymentFactory(
            purchaser=self.user
        )
        self.payment_attempt = factories.PaymentAttemptFactory(
            payment=self.payment,
            cart_stall=self.cart_stall,
        )
        self.client.login(username=self.user.username, password="password")
        self.view_url = reverse("paypal_adaptive_return",
                           kwargs={
                               "payment_id": self.payment.id,
                               "payment_secret_uuid": self.payment.secret_uuid
                           })

    def test_cart_stall_deleted(self, mock_notifier_customer,
            mock_notifier_merchant):
        response = self.client.get(self.view_url)
        cart_stalls = CartStall.objects.filter(id=self.cart_stall.id)
        self.assertEqual(len(cart_stalls), 0)

    def test_payment_marked_as_created(self, mock_notifieri_customer,
            mock_notifier_merchant):
        response = self.client.get(self.view_url)
        payment = Payment.objects.get(id=self.payment.id)
        self.assertEqual(payment.status, Payment.STATUS_CREATED)

    def test_payment_attempt_not_deleted(self, mock_notifier_customer,
                                         mock_notifier_merchant):
        response = self.client.get(self.view_url)
        #check for DoesNotExist
        payment_attempt = PaymentAttempt.objects.get(id=self.payment_attempt.id)

    def test_payment_return_on_already_complete_payment(self, mock_customer_notifier,
            mock_merchant_notifier):
        # Payment return can end up being called twice if paypal starts a
        # redirect, then the user hits the 'return' button so the first
        # request is cancelled and another begins.
        self.payment_attempt.complete()
        response = self.client.get(self.view_url)
        self.assertRedirects(response, reverse('payment_track',
                                               kwargs={"payment_id":self.payment_attempt.payment.id}))

    def test_payment_return_with_remaining_cart_stalls(self, mock_customer_notifier,
                                                       mock_merchant_notifier):
        # Smoke test to make sure that this path doesn't throw any errors
        cs_two = factories.create_cart_stall(user=self.user, num_products=2)
        response = self.client.get(self.view_url)


@mock.patch('purchase.models.client')
class RefundViewTestCase(TestCase):

    def setUp(self):
        super(RefundViewTestCase, self).setUp()
        self.order = factories.create_order(5)
        self.user = self.order.stall.user
        self.client.login(username=self.user.username, password="password")

        self.patcher = mock.patch('apps.purchase.models.notifier')
        self.patcher.start()
        self.addCleanup(self.patcher.stop)

    def test_post_creates_refund(self, mock_client):
        self.view_url = reverse("refund", kwargs={"order_id":self.order.id})
        data = {
            "entire_order": True,
            "reason": "There's always a reason"
        }
        response = self.client.post(self.view_url, data=data)
        order = Order.objects.get(id=self.order.id)
        self.assertEqual(len(order.refunds.all()), 1)
        refunded_line_item_ids = [l.id for l in
                                  order.refunds.all()[0].line_items.all()]
        expected_line_item_ids = [l.id for l in order.line_items.all()]
        self.assertEqual(len(refunded_line_item_ids),
                         len(expected_line_item_ids))
        self.assertEqual(set(refunded_line_item_ids),
                         set(expected_line_item_ids))

    def test_view_not_accessible_if_user_does_not_own_order_stall(self, mock_client):
        user = factories.UserFactory()
        self.client.login(username=user.username, password="password")
        view_url = reverse("refund", kwargs={"order_id":self.order.id})
        response = self.client.post(view_url, data={})
        self.assertEqual(response.status_code, 403)

    def test_refund_individual_line_items(self, mock_client):
        view_url = reverse("refund", kwargs={"order_id": self.order.id})
        line_item = self.order.line_items.all()[0]
        data = {
            "line_items": [line_item.id],
            "reason": "There's always a reason"
        }
        self.client.post(view_url, data=data)
        order = Order.objects.get(id=self.order.id)
        refunds = order.refunds.all()
        self.assertEqual(len(refunds), 1)
        refund_line_items = refunds[0].line_items.all()
        self.assertEqual(len(refund_line_items), 1)
        self.assertEqual(refund_line_items[0].id, line_item.id)

@mock.patch.object(purchase.views.client, 'validate_ipn')
class IpnHandlerViewTestCase(TestCase):

    def setUp(self):
        super(IpnHandlerViewTestCase, self).setUp()
        self.view_url = reverse('ipn_handler')
        self.order = factories.create_order(5)

        ipn_data = json.loads(utils.load_fixture("refund_ipn.json"))
        ipn_data["pay_key"] = self.order.payment.pay_key
        self.ipn_data = urlencode(ipn_data)

        self.notifier_patcher = mock.patch('apps.purchase.models.notifier')
        self.notifier_patcher.start()
        self.addCleanup(self.notifier_patcher.stop)

    def tearDown(self):
        super(IpnHandlerViewTestCase, self).tearDown()

    def do_post(self, data):
        return self.client.post(
            self.view_url,
            data=data,
            content_type="application/x-www-form-urlencoded"
        )

    def test_valid_response(self, mock_validate):
        mock_validate.return_value = True
        response = self.do_post(urlencode({"pay_key": "someignoredvalue"}))
        self.assertEqual(response.status_code, 200)

    def test_refund_not_in_system_creates_new_refund(self, mock_validate):
        mock_validate.return_value = True
        response = self.do_post(self.ipn_data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.order.is_refunded())

    def test_existing_refund_not_created(self, mock_validate):
        mock_validate.return_value = True
        self.order.refund("ignored reason", send_to_paypal=False)
        response = self.do_post(self.ipn_data)
        self.assertEqual(len(self.order.refunds.all()), 1)

    @mock.patch('purchase.views.Payment.objects.get')
    def test_refund_does_not_refund_already_refunded_orders(self, mock_get, mock_validate):
        mock_validate.return_value = True
        mock_payment = mock.Mock()
        mock_order = mock.Mock()
        mock_get.return_value = mock_payment
        mock_payment.order.return_value.is_refunded.return_value = True
        response = self.do_post(self.ipn_data)
        self.assertEqual(mock_get.return_value.refund.call_count, 0)


@mock.patch.object(purchase.views.client, 'validate_ipn')
class IpnPayPrimaryTestCase(TestCase):

    def setUp(self):
        super(IpnPayPrimaryTestCase, self).setUp()
        self.view_url = reverse('ipn_handler')
        self.order = factories.create_order(5)

        self.ipn_data = json.loads(utils.load_fixture("pay_primary_ipn.json"))
        self.ipn_data["pay_key"] = self.order.payment.pay_key

    def test_payment_marked_as_primary_paid(self, mock_validate):
        mock_validate.return_value = True
        response = self.client.post(self.view_url, data=self.ipn_data)
        payment = Payment.objects.get(id=self.order.payment.id)
        self.assertEqual(payment.status, Payment.STATUS_PRIMARY_PAID)


@mock.patch.object(purchase.views.client, 'validate_ipn')
class IpnPaymentCompleteTestCase(TestCase):

    def setUp(self):
        super(IpnPaymentCompleteTestCase, self).setUp()
        self.view_url = reverse('ipn_handler')
        self.order = factories.create_order(5)

        self.ipn_data = json.loads(utils.load_fixture("payment_complete_ipn.json"))
        self.ipn_data["pay_key"] = self.order.payment.pay_key

    def test_payment_marked_as_complete(self, mock_validated):
        mock_validated.return_value = True
        response = self.client.post(self.view_url, data=self.ipn_data)
        payment = Payment.objects.get(id=self.order.payment.id)
        self.assertEqual(payment.status, Payment.STATUS_COMPLETED)



@mock.patch.object(purchase.views, 'notifier')
class MarkDispatchedTestCase(TestCase):

    def setUp(self):
        super(MarkDispatchedTestCase, self).setUp()
        self.order = factories.create_order(4)
        self.view_url = reverse('mark_dispatched',
                                kwargs={'order_id': self.order.id})

    def test_order_is_dispatched(self, mock_notifier):
        self.client.login(username=self.order.stall.user.username,
                          password="password")
        response = self.client.post(self.view_url,
                                    data={"redirect_url":"http://test.com"})
        self.assertTrue(self.order.is_dispatched())
        self.assertRedirects(response, 'http://test.com')

    def test_forbidden_id_user_is_not_owning_merchant(self, mock_notifier):
        user = factories.UserFactory()
        result = self.client.login(username=user.username, password="password")
        self.assertTrue(result)
        response = self.client.post(self.view_url)
        self.assertEqual(response.status_code, 403)
        self.assertFalse(self.order.is_dispatched())


class PaypalCancelViewTestCase(TestCase):

    def setUp(self):
        super(PaypalCancelViewTestCase, self).setUp()
        self.payment = factories.PaymentFactory()
        self.user = self.payment.purchaser
        self.view_url = reverse('paypal_adaptive_cancel', kwargs={
            "payment_id": self.payment.id,
            "payment_secret_uuid": self.payment.secret_uuid
        })
        self.client.login(username=self.user.username, password="password")

    def test_cancel_sets_payment_status(self):
        self.client.get(self.view_url)
        payment = Payment.objects.get(id=self.payment.id)
        self.assertEqual(payment.status, "cancelled")

    def test_cancel_view_fails_if_wrong_user(self):
        user2 = factories.UserFactory()
        self.client.login(username=user2.username, password="password")
        response = self.client.get(self.view_url)
        self.assertEqual(response.status_code, 403)


class CartStallViewTestCase(TestCase):

    def setUp(self):
        super(CartStallViewTestCase, self).setUp()
        self.cart_stall = factories.create_cart_stall(1)
        self.view_url = reverse('cart_stalls',
                                kwargs={"cart_stall_id":self.cart_stall.id})
        self.user = self.cart_stall.cart.user
        self.client.login(username=self.user.username, password="password")
        self.patcher = mock.patch.object(purchase.models.CartStall,
                                         'get_countries')
        self.mock_get_countries = self.patcher.start()
        self.addCleanup(self.patcher.stop)

    def test_delete_cart_stall(self):
        response = self.client.delete(self.view_url)
        cart_stalls = CartStall.objects.filter(id=self.cart_stall.id)
        self.assertEqual(len(cart_stalls.all()), 0)

    def test_403_for_unauthorised_user(self):
        user = factories.UserFactory()
        self.client.login(username=user.username, password="password")
        response = self.client.delete(self.view_url)
        self.assertEqual(response.status_code, 403)

    def test_put_updates_country(self):
        country = factories.CountryFactory(code="ES", title="Spain")
        self.mock_get_countries.return_value = [country]
        data = country.to_json()
        response = self.client.put(self.view_url,
                                   data=json.dumps({"country": data}),
                                   content_type="application/json")
        cs = CartStall.objects.get(id=self.cart_stall.id)
        self.assertEqual(cs.speculative_country, country)

    def test_put_updates_note(self):
        data = {"note": "A test note"}
        country = factories.CountryFactory(code="ES", title="Spain")
        self.mock_get_countries.return_value = [country]
        response = self.client.put(self.view_url,
                                   data=json.dumps(data),
                                   content_type='application/json'
                                   )
        cs = CartStall.objects.get(id=self.cart_stall.id)
        self.assertEqual(cs.note, "A test note")

    def test_put_returns_cart_stall_summary(self):
        country = factories.CountryFactory(code="ES", title="Spain")
        self.mock_get_countries.return_value = [country]
        response = self.client.put(self.view_url,
                                   data=json.dumps({"country_id": country.id}),
                                   content_type="application/json")
        cs = CartStall.objects.get(id=self.cart_stall.id)
        self.assertEqual(json.loads(response.content), cs.to_json())

    def test_get_returns_all_cart_stalls(self):
        country = factories.CountryFactory(code="ES", title="Spain")
        self.mock_get_countries.return_value = [country]
        view_url = reverse('cart_stalls')
        response = self.client.get(view_url)
        data = json.loads(response.content)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0], self.cart_stall.to_json())



class CartAddTestCase(TestCase):

    def setUp(self):
        super(CartAddTestCase, self).setUp()
        self.product = factories.ProductFactory()
        self.view_url = reverse('checkout_add',
                                kwargs={"slug": self.product.slug})

    def test_redirects_to_login_if_not_authenticated(self):
        response = self.client.post(self.view_url)
        expected = "{0}?next={1}".format(
            reverse('login'),
            reverse('checkout_cart')
        )
        self.assertRedirects(response, expected)

    def test_redirect_populates_session_variable(self):
        response = self.client.post(self.view_url)
        self.assertEqual(self.client.session["product_to_add_id"],
                         self.product.id)

    def test_returns_error_message_if_out_of_stock_error(self):
        self.product.stock = 0
        self.product.save()
        self.user = factories.UserFactory()
        self.client.login(username=self.user.username, password="password")
        # Basically a smoke test checking that an exception is not thrown
        response = self.client.post(self.view_url)



class CheckoutPayStallTestCase(TestCase):
    #TODO refactor setup common logic in this test case

    def test_checkout_paystall_creates_payment_attempt(self):
        self.cart_stall = factories.create_cart_stall(5)
        self.user = self.cart_stall.cart.user
        self.client.login(username=self.user.username,
                password="password")
        view_url = reverse('checkout_pay_stall', kwargs={
            "cart_stall_id": self.cart_stall.id
            })
        response = self.client.post(view_url)
        cs = CartStall.objects.get(id=self.cart_stall.id)
        self.assertEqual(len(cs.payment_attempts.all()), 1)
        payment_attempt = cs.payment_attempts.all()[0]
        self.assertIsNotNone(payment_attempt.payment)
        self.assertIsNotNone(payment_attempt.cart_stall)

    @mock.patch('purchase.notifier.mandrill_send_template')
    @mock.patch('purchase.api')
    def test_checkout_paystall_for_unverified_account_sends_email(self, api, mock_send_tempalte):
        api.ChainedPayment.side_effect = PayError("PayError: Account someemail@gmail.com isn't confirmed by PayPal",
                                                  error_id="569042")
        self.cart_stall = factories.create_cart_stall(5)
        self.user = self.cart_stall.cart.user
        self.client.login(username=self.user.username,
                password="password")
        view_url = reverse('checkout_pay_stall', kwargs={
            "cart_stall_id": self.cart_stall.id
            })
        response = self.client.post(view_url, follow=True)
        expected_url = reverse("checkout_cart")
        self.assertRedirects(response, "http://testserver{0}".format(expected_url))
        self.assertEqual(len(response.context["messages"]), 1)

    @mock.patch('purchase.api')
    def test_checkout_paystall_for_some_paypal_error(self, api):
        api.ChainedPayment.side_effect = PayError("PayError: some paypal error",
                                                  error_id="569002")
        self.cart_stall = factories.create_cart_stall(5)
        self.user = self.cart_stall.cart.user
        self.client.login(username=self.user.username,
                password="password")
        view_url = reverse('checkout_pay_stall', kwargs={
            "cart_stall_id": self.cart_stall.id
            })
        response = self.client.post(view_url, follow=True)
        expected_url = reverse("checkout_cart")
        self.assertRedirects(response, "http://testserver{0}".format(expected_url))
        self.assertEqual(len(response.context["messages"]), 1)


class CheckoutCartStallViewTestCase(TestCase):

   def setUp(self):
       self.cart_stall = factories.create_cart_stall(3)
       self.user = self.cart_stall.cart.user
       self.client.login(username=self.user.username,
                         password="password")
       self.view_url = reverse('cart_stalls', kwargs={"cart_stall_id":
                                                      self.cart_stall.id})

   def test_checkout_cart_stall(self):
       response = self.client.get(self.view_url)
       self.assertEqual(json.loads(response.content), self.cart_stall.to_json())

