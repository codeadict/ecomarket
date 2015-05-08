from django.core.urlresolvers import reverse
from django.test import TestCase
from tests import factories

class InvoiceViewTestCase(TestCase):

    def test_context_contains_order(self):
        order = factories.create_order(5)
        view_url = reverse('invoice', kwargs={"order_id": order.id})
        r = self.client.get(view_url)
        self.assertEqual(r.context["order"].id, order.id)
