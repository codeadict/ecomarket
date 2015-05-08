import datetime
from django.core.urlresolvers import reverse
from django.test import TestCase
from ecomarket.tests import factories

class BoughtViewTestCase(TestCase):

    def setUp(self):
        super(BoughtViewTestCase, self).setUp()
        self.user = factories.UserFactory(password="apassword")
        self.stall = factories.StallFactory()
        self.product1 = factories.ProductFactory(stall=self.stall)
        self.product2 = factories.ProductFactory(stall=self.stall)

        self.order1 = factories.OrderFactory(stall=self.stall, user=self.user)
        self.order1.created = first_date = datetime.datetime.strptime(
            "2012-06-07", "%Y-%m-%d")
        self.order1.save()

        self.order2 = factories.OrderFactory(stall=self.stall, user=self.user)
        self.order2.created = datetime.datetime.strptime(
            "2012-06-08", "%Y-%m-%d")
        self.order2.save()

        self.order3 = factories.OrderFactory(stall=self.stall, user=self.user)
        self.order3.created = datetime.datetime.strptime(
            "2012-06-09", "%Y-%m-%d")
        self.order3.save()
        factories.FeedbackFactory(order=self.order3)

        self.line_item1 = factories.LineItemFactory(product=self.product1,
                                                    order=self.order1)

        self.line_item2 = factories.LineItemFactory(product=self.product2,
                                                    order=self.order2)
        self.order2 = self.line_item2.order

        self.client.login(username=self.user.username, password="apassword")


    def test_bought_displays_all_orders(self):
        view_url = reverse("bought")
        response = self.client.get(view_url)
        orders = response.context["orders"]
        # order is important here, should be in reverse chronological order
        expected_ids = [order.id for order in [self.order3, self.order2,
                                               self.order1,]]
        actual_ids = [order.id for order in orders]
        self.assertEqual(expected_ids, actual_ids)

    def test_awaiting_feedback_displays_orders_without_feedback(self):
        view_url = reverse("bought_awaiting_feedback")
        response = self.client.get(view_url)
        orders = response.context["orders"]
        self.assertEqual(len(orders), 2)
        order_ids = [o.id for o in orders]
        expected = [o.id for o in [self.order2, self.order1]]
        self.assertEqual(order_ids, expected)
