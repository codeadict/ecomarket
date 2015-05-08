from __future__ import print_function

import datetime
import time

from django.core.management.base import (
    CommandError, NoArgsCommand, make_option
)
from django.utils import timezone

from lovelists.models import PromotionScheduler


class Command(NoArgsCommand):

    DATE_FORMAT = "%Y-%m-%d"

    help = ("Find any love lists scheduled to be promoted on the specified "
            "date (default: today) and promote them.")

    option_list = NoArgsCommand.option_list + (
        make_option("--date", dest="date",
                    help="Scheduled date (eg. 2013-01-01)"),
    )

    def _handle(self, date=None, **options):
        if date is None:
            date = datetime.date.today()
        else:
            date = datetime.date.utcfromtimestamp(
                time.mktime(time.strptime(date, self.DATE_FORMAT)))
        schedulers = PromotionScheduler.objects.filter(actioned=False)
        try:
            scheduler = schedulers.get(start_date=date)
        except PromotionScheduler.DoesNotExist:
            raise CommandError("No scheduler with start date %s." % date)
        except PromotionScheduler.MultipleObjectsReturned:
            obs = schedulers.filter(start_date=date)
            raise CommandError("Not sure which of [%s] to promote"
                               % ", ".join(str(ob.love_list) for ob in obs))
        love_list = scheduler.love_list
        love_list.promoted = timezone.now()
        love_list.save()
        scheduler.actioned = True
        scheduler.save()

    def _cleanup(self):
        today = datetime.date.today()
        unactioned = PromotionScheduler.objects.filter(actioned=False,
                                                       start_date__lte=today)
        if unactioned.count() == 0:
            return
        print("Warning: The following PromotionScheduler objects are still "
              "not actioned:", file=self.stderr)
        for schedule in unactioned:
            print("\t%s" % schedule, file=self.stderr)

    def handle_noargs(self, **options):
        try:
            self._handle(**options)
        finally:
            self._cleanup()
