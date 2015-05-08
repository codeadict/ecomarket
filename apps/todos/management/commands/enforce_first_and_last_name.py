from __future__ import print_function

from django.core.management.base import NoArgsCommand
from django.db.models import Q

from django.contrib.auth.models import User


class Command(NoArgsCommand):

    help = ("ONE OFF command to force sellers without first or last names to "
            "add them.")

    def handle_noargs(self, **options):
        verbose = (options["verbosity"] >= 2)
        users = User.objects.filter(Q(first_name="") | Q(last_name="") |
                                    Q(first_name=None) | Q(last_name=None))
        view_name = "add_full_name"
        for user in users:
            if verbose:
                msg = "Adding todo '{}' for {}".format(view_name, user)
                print(msg, file=self.stdout)
            user.todos.create(view_name=view_name)
