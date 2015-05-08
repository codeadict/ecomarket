from django.core.urlresolvers import reverse
from django.test import TestCase
from tests import factories


class SoldViewTestCase(TestCase):

    def setUp(self):
        self.needs_shipping = factories.create_order(5, dispatched=False)
        self.shipped = factories.create_order(5, dispatched=True,
                                              stall=self.needs_shipping.stall)
        self.stall = self.shipped.stall
        self.user = self.stall.user
        self.client.login(username=self.user.username, password="password")

    def test_sold_awaiting_shipping(self):
        view_url = reverse('sold_awaiting_shipping')
        response = self.client.get(view_url)
        orders = response.context["orders"]
        self.assertEqual(len(orders), 1)
        self.assertEqual(orders[0].id, self.needs_shipping.id)

    def test_sold_completed(self):
        view_url = reverse('sold_completed')
        response = self.client.get(view_url)
        orders = response.context["orders"]
        self.assertEqual(len(orders), 1)
        self.assertEqual(orders[0].id, self.shipped.id)

    def test_sold_all(self):
        view_url = reverse('sold_all')
        response = self.client.get(view_url)
        orders = response.context["orders"]
        self.assertEqual(len(orders), 2)
        self.assertEqual(set(orders), set([self.needs_shipping, self.shipped]))
