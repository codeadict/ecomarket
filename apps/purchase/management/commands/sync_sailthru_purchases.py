import warnings

from django.core.management.base import NoArgsCommand, make_option
from django.db import transaction
from django.db.models import Q

from django.contrib.auth.models import User
from mailing_lists.integrations.sailthru import Sailthru

class FakeRequest(object):
    COOKIES = {}
    def build_absolute_uri(self, url):
        return 'http://www.ecomarket.com' + url

class Command(NoArgsCommand):

    """
    ONE OFF command to synchronize all users purchases with SailThru.
    """

    @transaction.commit_on_success
    def handle_noargs(self, **options):
        st = Sailthru(FakeRequest())
        for user in User.objects.exclude(orders=None):
            response = st.api.api_get('user', {'key':'email',
                                               'id':user.email,
                                               'fields':{'purchases':1}})
            try:
                data = st.check_response(response)
            except:
                continue

            if data['purchases'] is None:
                st_order_ids = []
            else:
                st_order_ids = []
                for purchase in data['purchases']:
                    for item in purchase['items']:
                        if 'vars' in item:
                            st_order_ids.append(item['vars']['order_id'])
            orders = (user.orders
                      .filter(Q(is_joomla_order=True) | ~Q(payment=None))
                      .exclude(id__in=st_order_ids))
            for order in orders:
                st.order_purchased(order)
