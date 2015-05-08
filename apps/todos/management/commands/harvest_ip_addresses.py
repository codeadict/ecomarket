from __future__ import print_function

from django.core.management.base import NoArgsCommand

from django.contrib.auth.models import User


class Command(NoArgsCommand):

    help = ("ONE OFF command to schedule all users without their IP addresses "
            "logged to get them logged next time they log in.")

    def handle_noargs(self, **kwargs):
        # Sellers all have a country set, which is more reliable information
        # than an IP address.
        users = User.objects.filter(stall=None)
        count = users.count()
        for user in users:
            user.todos.create(view_name="get_ip_address")
        print("Updated {} users".format(count), file=self.stdout)
