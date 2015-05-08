from marketplace.models import Country
import money
import purchase
from purchase import api
from purchase.models import *
import datetime
from django.test import TestCase
from tests import factories
from money import Money
import mock
import unittest

class LineItemTestCase(TestCase):

    def setUp(self):
        super(LineItemTestCase, self).setUp()
        self.line_item = factories.LineItemFactory.build(price=30)
        self.product = self.line_item.product
        self.price = self.line_item.price

    def test_line_item_total_is_calculated_correctly(self):
        line_item = LineItem(product=self.product, price=self.price,
                             quantity=10)
        self.assertEqual(line_item.total().amount, 300)


class OrderTestCase(TestCase):

    def setUp(self):
        super(OrderTestCase, self).setUp()
        self.stall = factories.StallFactory()
        self.order = factories.OrderFactory(stall=self.stall)

        self.product1 = factories.ProductFactory(stall=self.stall)
        self.product2 = factories.ProductFactory(stall=self.stall)

        self.line_item2 = factories.LineItemFactory(
            product=self.product1,
            quantity=10,
            order=self.order,
            price=10
        )
        self.line_item2 = factories.LineItemFactory(
            product=self.product2,
            quantity=10,
            order=self.order,
            price=20
        )
        self.order.delivery_charge = Money(10)
        self.order.save()

    def test_order_subtotal_calculation(self):
        self.assertEqual(self.order.subtotal().amount, 10 *10 + 20 * 10)

    def test_order_total_calculation(self):
        self.assertEqual(self.order.total().amount, 10 * 10 + 20 * 10 + 10)


@mock.patch.object(purchase.models, 'client')
class OrderRefundTestCase(TestCase):

    def setUp(self):
        super(OrderRefundTestCase, self).setUp()
        self.order = factories.create_order(5)
        self.notifier_patcher = mock.patch("apps.purchase.models.notifier")
        self.notifier_patcher.start()
        self.addCleanup(self.notifier_patcher.stop)

    def test_refund_subset_line_items_creates_refunds(self, mock_api):
        line_item = self.order.line_items.all()[:1].get()
        self.order.refund("out of stock", line_items=[line_item])
        line_item = LineItem.objects.get(id=line_item.id)
        self.assertEqual(line_item.refund.reason, "out of stock")

        #check that no other line items have been refunded
        other_line_items = self.order.line_items.filter(refund__isnull=False).all()
        self.assertEqual([i.id for i in other_line_items], [line_item.id])

    def test_refund_no_line_item_refunds_all(self, mock_api):
        self.order.refund("out of stock")
        refunded_line_items = self.order.line_items.filter(
            refund__isnull=False).all()
        self.assertEqual(len(refunded_line_items), 5)
        self.assertEqual(set([l.id for l in refunded_line_items]),
                         set([l.id for l in self.order.line_items.all()]))

    def test_refund_does_not_allow_line_items_from_other_orders(self, mock_api):
        other_line_item = factories.LineItemFactory()
        with self.assertRaises(RuntimeError):
            self.order.refund("evil", [other_line_item])
        refunds = Refund.objects.filter(order=self.order).all()
        self.assertEqual(len(refunds), 0)

    def test_refund_sends_to_paypal(self, mock_api):
        line_item = self.order.line_items.all()[:1].get()
        self.order.refund("sold out",[ line_item])
        mock_api.refund.assert_called_with(
            self.order.payment.pay_key,
            amount=line_item.price.amount,
            receiver_email=self.order.stall.paypal_email
        )

    def test_no_amount_when_no_line_items(self, mock_api):
        self.order.refund("sold out")
        mock_api.refund.assert_called_with(self.order.payment.pay_key)

    def test_order_is_refunded(self, mock_client):
        self.assertFalse(self.order.is_refunded())
        self.order.refund("hatred")
        self.assertTrue(self.order.is_refunded())

    def test_refund_marks_payment_as_refunded(self, mock_api):
        self.order.refund("sold out")
        self.assertEqual(self.order.payment.status, Payment.STATUS_REFUNDED)



class OrderDispatchTestCase(TestCase):

    def test_mark_dispatched_marks_all_line_items(self):
        order = factories.create_order(5)
        order.mark_dispatched()
        for line_item in order.line_items.all():
            self.assertTrue(line_item.dispatched)

    def test_mark_dispatched_doesnt_mark_refunded_line_items(self):
        order = factories.create_order(5)
        refunded_line_item = order.line_items.all()[0]
        refund = factories.RefundFactory(order=order)
        refunded_line_item.refund = refund
        refunded_line_item.save()
        order.mark_dispatched()
        for line_item in order.line_items.all():
            if line_item.id == refunded_line_item.id:
                self.assertFalse(line_item.dispatched, "refunded item should "
                                 "not be dispatched")
            else:
                self.assertTrue(line_item.dispatched, "unrefunded items should "
                                "be dispatched")

    def test_is_dispatched(self):
        order = factories.create_order(5, dispatched=True)
        self.assertTrue(order.is_dispatched())

    def test_is_dispatched_with_refunded_items(self):
        order = factories.create_order(2, dispatched=True)
        ref_line_item = order.line_items.all()[0]
        refund = factories.RefundFactory(order=order)
        ref_line_item.refund = refund
        ref_line_item.dispatched = False
        ref_line_item.save()

        self.assertTrue(order.is_dispatched())

    def test_is_dispatched_on_non_dispatched_order(self):
        order = factories.create_order(2)
        self.assertFalse(order.is_dispatched())


class OrderManagerTestCase(TestCase):

    def setUp(self):
        super(OrderManagerTestCase, self).setUp()

    def make_order_days_old(self, order, days):
        created = datetime.datetime.now() - datetime.timedelta(days=days)
        order.created = created
        order.save()

    def test_dispatch_overdue_if_subset_line_items_not_dispatched(self):
        order = factories.create_order(5)
        line_item = order.line_items.all()[0]
        line_item.dispatched = True
        line_item.save()
        self.make_order_days_old(order, 3)

        non_overdue_orders = factories.create_order(3)

        result = Order.objects.dispatch_overdue(2).all()
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].id, order.id)

    def test_dispatch_not_overdue_if_all_line_items_dispatched(self):
        dispatched_order = factories.create_order(4, dispatched=True)
        self.make_order_days_old(dispatched_order, 50)
        result = Order.objects.dispatch_overdue(10).all()
        self.assertEqual(len(result), 0)

    def test_dispatch_overdue_doesnt_include_joomla_orders(self):
        order = factories.create_order(5, is_joomla_order=False)
        self.make_order_days_old(order, 2)
        joomla_order = factories.create_order(5, is_joomla_order=True)
        self.make_order_days_old(joomla_order, 2)
        result = Order.objects.dispatch_overdue(1)
        self.assertEqual([o.id for o in result], [order.id])


    def test_dispatch_not_overdue_if_undispatched_item_refunded(self):
        order = factories.create_order(4, dispatched=True)
        self.make_order_days_old(order, 10)
        line_item = order.line_items.all()[0]
        refund = factories.RefundFactory(order=order)
        line_item.refund = refund
        line_item.dispatched=False
        line_item.save()
        result = Order.objects.dispatch_overdue(14)
        self.assertEqual(len(result), 0)

    def test_dispatched_orders_not_paid(self):
        ready_to_pay = factories.create_order(
            5,
            dispatched=True,
            payment_status=Payment.STATUS_PRIMARY_PAID
        )
        self.make_order_days_old(ready_to_pay, 15)

        not_ready_to_pay = factories.create_order(5, dispatched=False)

        already_paid = factories.create_order(5, dispatched=True,
                                              payment_status=Payment.STATUS_COMPLETED)
        payment = already_paid.payment
        self.make_order_days_old(already_paid, 15)

        to_pay = Order.objects.ready_to_pay(14).all()
        self.assertEqual(len(to_pay), 1)
        self.assertEqual(to_pay[0].id, ready_to_pay.id)

    def test_ready_to_pay_doesnt_include_joomla_orders(self):
        ready_to_pay = factories.create_order(
            5,
            dispatched=True,
            payment_status=Payment.STATUS_PRIMARY_PAID
        )
        self.make_order_days_old(ready_to_pay, 15)
        joomla = factories.create_order(
            3,
            dispatched=True,
            payment_status=Payment.STATUS_PRIMARY_PAID,
            is_joomla_order=True,
        )
        self.make_order_days_old(joomla, 15)
        to_pay = list(Order.objects.ready_to_pay(0).all())
        self.assertEqual(to_pay, [ready_to_pay])

    def test_awaiting_feedback(self):
        order1 = factories.create_order(3)
        order2 = factories.create_order(4)
        feedback = factories.FeedbackFactory(order=order1)

        awaiting = Order.objects.awaiting_feedback().all()
        self.assertEqual(len(awaiting), 1)
        self.assertEqual(awaiting[0].id, order2.id)

    def test_feedback_given(self):
        order1 = factories.create_order(3)
        order2 = factories.create_order(3)
        feedback = factories.FeedbackFactory(order=order1)

        given = Order.objects.feedback_given().all()
        self.assertEqual(len(given), 1)
        self.assertEqual(given[0].id, order1.id)

    def test_dispatched(self):
        order1 = factories.create_order(3)
        order2 = factories.create_order(5, dispatched=True)
        dispatched = Order.objects.dispatched().all()
        self.assertEqual(len(dispatched), 1)
        self.assertEqual(dispatched[0].id, order2.id)

    def test_old_orders_are_dispatched(self):
        order = factories.create_order(4, is_joomla_order=True)
        dispatched = Order.objects.dispatched()
        self.assertEqual([order.id], [o.id for o in dispatched])

    def test_completed(self):
        order1 = factories.create_order(3)
        order2 = factories.create_order(5, dispatched=True)

        completed = Order.objects.completed().all()
        self.assertEqual(len(completed), 1)
        self.assertEqual(completed[0].id, order2.id)

    def test_old_orders_are_complete(self):
        order = factories.create_order(3, is_joomla_order=True)
        completed = Order.objects.completed().all()
        self.assertEqual([order.id], [c.id for c in completed])

    def test_awaiting_shipping(self):
        order1 = factories.create_order(3)
        order2 = factories.create_order(4)
        order2.mark_dispatched()

        to_ship = Order.objects.awaiting_shipping().all()
        self.assertEqual(len(to_ship), 1)
        self.assertEqual(to_ship[0].id, order1.id)


@mock.patch.object(purchase.models.CartStall, 'delivery_total')
class CartStallTestCase(TestCase):

    def setUp(self):
        super(CartStallTestCase, self).setUp()
        self.cart_stall = factories.create_cart_stall(num_products=3, price=10)

    def test_cart_stall_order_contains_all_products(self, mock_delivery):
        mock_delivery.return_value = money.Money(10, "GBP")
        order = self.cart_stall.create_order()
        self.assertEqual(len(order.line_items.all()),
                         len(self.cart_stall.cart_products.all()))
        for cart_product in self.cart_stall.cart_products.all():
            line_item = [l for l in order.line_items.all()
                         if l.product.id == cart_product.product.id][0]
            self.assertEqual(line_item.price, cart_product.unit_price)
            self.assertEqual(line_item.quantity, cart_product.quantity)

    def test_create_order_sets_delivery_charge(self, mock_delivery):
        mock_delivery.return_value =  money.Money(10, "GBP")
        order = self.cart_stall.create_order()
        self.assertEqual(order.delivery_charge.amount, 10)

    def test_create_order_sets_notes(self, mock_delivery):
        mock_delivery.return_value =  money.Money(10, "GBP")
        self.cart_stall.note = "test notes"
        order = self.cart_stall.create_order()
        self.assertEqual(order.note, "test notes")

    def test_to_json(self, mock_delivery):
        mock_delivery.return_value =  money.Money(10, "GBP")
        json = self.cart_stall.to_json()
        self.assertEqual(len(json["cart_products"]), 3)



class CartStallShippingCalculationTestCase(TestCase):


    def setUp(self):
        super(CartStallShippingCalculationTestCase, self).setUp()
        user = factories.UserFactory()
        self.country = Country.objects.get(code="GB")
        self.user = user
        address = factories.ShippingAddressFactory(
            user=user,
            country=self.country
        )
        self.cart_stall = factories.create_cart_stall(
            num_products=0,
            address=address,
            user=user
        )
        self.prod_1 = self.create_product_with_profile(10, 5)
        self.prod_2 = self.create_product_with_profile(20, 5)
        self.profile = self.prod_1.shipping_profile

    def create_product_with_profile(self, price, price_extra):
        ship_prof = factories.ShippingProfileFactory(
            stall=self.cart_stall.stall,
            others_price=None,
            others_price_extra=None,
        )
        rule = factories.ShippingRuleFactory(
            profile=ship_prof,
            rule_price=price,
            rule_price_extra=price_extra,
        )
        rule.countries.add(self.country)
        return factories.ProductFactory(
            stall=self.cart_stall.stall,
            shipping_profile=ship_prof
        )

    def add_to_cartstall(self, product, quantity):
        self.cart_stall.cart_products.create(
            product=product,
            quantity=quantity,
            unit_price=10
        )

    def test_largest_of_initial_payments_taken(self):
        self.add_to_cartstall(self.prod_1, 1)
        self.add_to_cartstall(self.prod_2, 1)
        self.assertEqual(self.cart_stall.delivery_total().amount, 25)

    def test_quantity_respected(self):
        self.add_to_cartstall(self.prod_1, 5)
        self.add_to_cartstall(self.prod_2, 10)
        self.assertEqual(self.cart_stall.delivery_total().amount, 90)

    def test_rules_from_other_countries_not_used(self):
        rule = factories.ShippingRuleFactory(
            profile=self.prod_1.shipping_profile,
            rule_price=100,
            rule_price_extra=1000
        )
        rule.countries.add(factories.CountryFactory(code="USA"))
        self.add_to_cartstall(self.prod_1, 3)
        self.assertEqual(self.cart_stall.delivery_total().amount, 20)

    def test_speculative_country_used_if_exists(self):
        country2 = factories.CountryFactory(code="ES")
        rule2 = factories.ShippingRuleFactory(
            profile=self.prod_1.shipping_profile,
            rule_price=30,
            rule_price_extra=10
        )
        rule2.countries.add(country2)
        rule2.save()
        self.cart_stall.address = None
        self.cart_stall.speculative_country = country2
        self.cart_stall.save()
        self.add_to_cartstall(self.prod_1, 1)
        delivery = self.cart_stall.delivery_total()
        self.assertEqual(delivery.amount, 30)

    @unittest.skip("pending")
    def test_address_used_even_if_speculative_country_defined(self):
        pass

    @mock.patch.object(purchase.models.CartStall, 'delivery_total')
    def test_create_order_sets_delivery_charge(self, mock_delivery):
        mock_delivery.return_value =  money.Money(10, "GBP")
        order = self.cart_stall.create_order()
        self.assertEqual(order.delivery_charge.amount, 10)

    def test_cart_stall_throws_error_on_set_invalid_shipping_address(self):
        country3 = factories.CountryFactory(code="FI")
        address = factories.ShippingAddressFactory(country=country3,
                                                   user=self.user)
        self.add_to_cartstall(self.prod_1, 4)
        with self.assertRaises(purchase.models.UnavailableShippingCountryError):
            self.cart_stall.set_address(address)

    def test_no_error_thrown_on_invalid_address_ships_to_rest_of_world(self):
        country3 = factories.CountryFactory(code="FI")
        product = self.create_product_with_profile(10, 3)
        self.profile.others_price = 10
        self.profile.save()
        self.add_to_cartstall(self.prod_1, 4)
        address = factories.ShippingAddressFactory(country=country3,
                                                   user=self.user)
        self.cart_stall.set_address(address)
        self.assertEqual(self.cart_stall.address.id, address.id)

    def test_get_countries_returns_only_countries_allowed_by_shipping_rules(self):
        #Make sure there is another country, otherwise this is a bogus test
        country2 = factories.CountryFactory(code="NL")
        self.add_to_cartstall(self.prod_1, 4)
        countries = self.cart_stall.get_countries()
        self.assertEqual([self.country.id], [c.id for c in countries])

    def test_rest_of_world_used_if_not_none(self):
        profile = self.prod_1.shipping_profile
        profile.others_price = 50
        profile.others_price_extra = 20
        profile.save()
        country2 = factories.CountryFactory(code="DE")
        self.cart_stall.address.country = country2
        self.cart_stall.address.save()
        self.add_to_cartstall(self.prod_1, 4)
        self.assertEqual(self.cart_stall.delivery_total().amount, 110)

    @unittest.skip("Needs implementing")
    def test_throws_unavailable_shipping_country_if_invalid_shipping(self):
        country2 = factories.CountryFactory(code="DE")
        self.cart_stall.address.country = country2
        self.cart_stall.address.save()
        self.add_to_cartstall(self.prod_1, 3)
        with self.assertRaises(purchase.models.UnavailableShippingCountryError):
            self.cart_stall.delivery_total()

    def test_throws_mismatching_country_if_address_speuclative_country_differ(self):
        country2 = factories.CountryFactory(code="DE")
        address = factories.ShippingAddressFactory(country=country2, user=self.user)
        self.cart_stall.speculative_country = self.country
        with self.assertRaises(purchase.models.MismatchingCountryError):
            self.cart_stall.set_address(address)

    def test_get_country_returns_uk_if_no_speculative_country_set(self):
        self.assertEqual(self.cart_stall.get_country(),
                         Country.objects.get(code="GB"))

    def test_get_country_returns_first_allowed_country_if_UK_invalid(self):
        profile = self.prod_1.shipping_profile
        rule = profile.shipping_rules.all()[0]
        country2 = factories.CountryFactory()
        rule.countries = [country2]
        rule.save()
        self.add_to_cartstall(self.prod_1, 3)
        self.assertEqual(self.cart_stall.get_country(), country2)



class PaymentTestCase(TestCase):

    def setUp(self):
        super(PaymentTestCase, self).setUp()
        self.mock_client = mock.Mock()
        self.old_client = purchase.models.client
        purchase.models.client = self.mock_client

    def tearDown(self):
        super(PaymentTestCase, self).tearDown()
        purchase.models.client = self.old_client

    def test_execute_payment(self):
        self.mock_client.execute_payment.return_value = {
            "paymentExecStatus": "complete"
        }
        payment = factories.PaymentFactory()
        payment.execute()
        p = Payment.objects.get(id=payment.id)
        self.assertEqual(p.status, "complete")


class CartProductTestCase(TestCase):

    def setUp(self):
        self.cart_stall = factories.create_cart_stall(1)
        self.cart_product = self.cart_stall.cart_products.all()[0]

    def test_to_json(self):
        result = self.cart_product.to_json()
        self.assertEqual(result["product"]["id"], self.cart_product.product.id)
        self.assertEqual(result["quantity"], 1)


