from django.core.urlresolvers import reverse
from django.test import TestCase
from tests import factories

class PurchaseAdminViewTestCase(TestCase):

    def setUp(self):
        self.view_url = reverse('orders_admin')

    def test_view_inaccessible_if_not_admin(self):
        user = factories.UserFactory()
        self.assertFalse(user.is_staff)
        logged_in = self.client.login(username=user.username, password="password")
        self.assertTrue(logged_in)
        response = self.client.get(self.view_url)
        self.assertEqual(response.status_code, 403)
