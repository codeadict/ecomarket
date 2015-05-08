from django.test import TestCase, RequestFactory
from tests import factories

from main.utils.mixpanel_tracking import get_request_properties

class ReservedPropertyTestCase(TestCase):

    def setUp(self):
        self.user = factories.UserFactory()
        self.factory = RequestFactory()
        self.request = self.factory.get("/ignored")

    def test_user_id_populated(self):
        self.request.user = self.user
        props = get_request_properties(self.request)
        self.assertEqual(props["distinct_id"], self.user.id)

    def test_x_forwarded_for_used_as_ip_if_present(self):
        """Should use leftmost non private IP address"""
        request = self.factory.get("/ignored", X_FORWARDED_FOR="192.168.0.1, 72.5.3.1, 127.0.0.1")
        props = get_request_properties(request)
        self.assertEqual(props["ip"], "72.5.3.1")

    def test_remote_ip_used_if_x_forwarded_for_not_present(self):
        request = self.factory.get("/ignored", REMOTE_ADDR="234.6.7.8")
        props = get_request_properties(request)
        self.assertEqual(props["ip"], "234.6.7.8")



