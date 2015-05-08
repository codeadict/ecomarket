from django.test import TestCase
from tests import factories

class UserProfileTestCase(TestCase):

    def test_total_gmv_is_sum_of_order_totals(self):
        order = factories.OrderFactory()
        user = order.user
        order2 = factories.OrderFactory(user=order.user)
        total = order.total() + order2.total()
        self.assertEqual(user.get_profile().total_gmv, total)
