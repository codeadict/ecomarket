from __future__ import print_function

from django.core.management.base import NoArgsCommand

from accounts.models import UserProfile


class Command(NoArgsCommand):

    help = ("ONE OFF command to force sellers without email validation to "
            "get validated.")

    def handle_noargs(self, **options):
        verbose = (options["verbosity"] >= 2)
        profiles = UserProfile.objects.exclude(user__stall=None).exclude(
            activation_key=UserProfile.ACTIVATED)
        view_name = "validate_email"
        for profile in profiles:
            if profile.has_facebook_auth:
                # Consider Facebook auth equal to email validation
                continue
            try:
                profile.user
            except:
                continue
            if verbose:
                msg = "Adding todo '{}' for {}".format(view_name, profile.user)
                print(msg, file=self.stdout)
            profile.user.todos.create(view_name=view_name)
