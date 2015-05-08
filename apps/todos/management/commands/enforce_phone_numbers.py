from __future__ import print_function

from django.core.management.base import NoArgsCommand
from django.db.models import Q

from marketplace.models import Stall


class Command(NoArgsCommand):

    help = ("ONE OFF command to force users without adequate phone numbers to "
            "enter new ones.")

    def handle_noargs(self, **options):
        verbose = (options["verbosity"] >= 2)
        for stall in Stall.objects.filter(
                Q(phone_landline=None) | Q(phone_mobile=None)):
            view_name = "add_phone_numbers"
            if verbose:
                msg = "Adding todo '{}' for {}".format(view_name, stall.user)
                print(msg, file=self.stdout)
            stall.user.todos.create(view_name=view_name)
