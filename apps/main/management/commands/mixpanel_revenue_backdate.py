from django.core.management.base import BaseCommand, CommandError
from purchase.models import Order
from django.conf import settings
from django.contrib.auth.models import User
from main.utils import mixpanel_engage
from money.Money import Money
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    args = ''
    help = "Backdates all Revenue Data to MixPanel"
    def handle(self, *args, **kwargs):
        for user in User.objects.all():
            try:
                user_profile = user.get_profile()
            except:
                continue
            total_gmv = user_profile.total_gmv
            if total_gmv is None or total_gmv <= 0:
                # Don't backdate valueless users
                continue         
            transactions = []
            for order in user.orders.completed():                
                transactions.append({
                    '$time': order.created.isoformat(),
                    '$amount': str(order.total().amount),
                    "Order ID": order.id,
                })
            if len(transactions) == 0:
                print "User has no transactions!"
                continue

            try:
                has_stall = user.stall is not None
            except:
                has_stall = False
            if has_stall:
                member_type = 'Regular'
            else:
                member_type = 'Stall Owner'
            user_properties = {       
                '$set': {                
                    '$email': user.email,
                    '$username': user.username,
                    '$created': user.date_joined.isoformat(),
                    "$last_seen": user.last_login.isoformat(),
                    '$first_name': user.first_name,
                    '$last_name': user.last_name,
                    '$ignore_time': True,
                    '$transactions': transactions,
                    'gender': user_profile.get_gender_display(),
                    'mp_name_tag': user.get_full_name(),
                    'Orders': user.orders.completed().count(),
                    'Total GMV to Date': str(total_gmv.amount),
                    'Member Type': member_type,
                },
                '$ip': 0,
                '$ignore_time': True,
                '$distinct_id': user.id,    
            }
            print user_properties
            mixpanel_engage(None, user_properties, user.id)


