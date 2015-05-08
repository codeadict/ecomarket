from __future__ import print_function

import warnings

from django.core.management.base import NoArgsCommand

from django.contrib.auth.models import User

from accounts.models import UserProfile

from mailing_lists.models import MailingListSignup


class Command(NoArgsCommand):

    help = "ONE OFF command to create a MailingListSignup object for each user"

    def handle_noargs(self, **kwargs):
        processed = 0
        for user in User.objects.all():
            mls = MailingListSignup.objects.filter(email_address=user.email)
            if mls.count() == 0:
                try:
                    MailingListSignup.objects.create_from_user(user)
                except UserProfile.DoesNotExist:
                    warnings.warn(
                        "User {} does not have a UserProfile".format(user))
                    continue
            processed += 1
            if processed % 10 == 0:
                print("Processed {} users".format(processed), file=self.stdout)
