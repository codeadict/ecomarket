from __future__ import print_function

from django.core.management.base import NoArgsCommand
from django.db.models import Q

from accounts.models import EmailNotification


class Command(NoArgsCommand):

    help = "ONE OFF command to enable all email notifications for all users"

    def handle_noargs(self, **kwargs):
        notifications = EmailNotification.objects.filter(
                Q(site_updates_features=False) |
                Q(stall_owner_tips=False) |
                Q(follower_notifications=False) |
                Q(products_you_might_like=False) |
                Q(private_messages=False))
        count = notifications.count()
        notifications.update(
            site_updates_features=True,
            stall_owner_tips=True,
            follower_notifications=True,
            products_you_might_like=True,
            private_messages=True,
        )
        print("Updated {} email notifications".format(count), file=self.stdout)
