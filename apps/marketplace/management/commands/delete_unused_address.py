# coding=utf-8
from django.core.management.base import NoArgsCommand
from django.contrib.auth.models import User

from accounts.models import ShippingAddress
from purchase.models import Order


class Command(NoArgsCommand):
    """
    Delete unused address for all users.
    What is kept back - addresses used in orders.
    If there are no orders for a user, then the last added address is kept back.
    All other addresses are deleted for a user.
    """
    help = "Delete unused addresses for all users"
    
    def handle_noargs(self, **options):
        all_users = User.objects.all()
        
        for user in all_users:
            all_addresses = set([a.pk for a in user.addresses.all()])
            if all_addresses:
                orders = Order.objects.filter(user=user)
                if orders:
                    order_addresses = set([o.address.pk for o in orders])
                    addresses_to_delete = all_addresses - order_addresses 
                else:
                    addresses_to_delete = all_addresses
                if addresses_to_delete:
                    print "User %s (%s) - %s" % (user, user.pk, len(addresses_to_delete))
                    ShippingAddress.objects.filter(user=user, pk__in=addresses_to_delete).delete()