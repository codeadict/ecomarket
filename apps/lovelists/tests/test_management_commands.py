from cStringIO import StringIO
from datetime import date, timedelta

from django.core.management.base import CommandError
from django.test import TestCase

from tests.factories import LoveListFactory

from lovelists.management.commands import promote_scheduled_love_lists
from lovelists.models import LoveList, PromotionScheduler


class PromoteScheduledLoveListsTest(TestCase):

    DATE_FORMAT = promote_scheduled_love_lists.Command.DATE_FORMAT

    def setUp(self):
        self.list1 = LoveListFactory(title="My first list")
        self.list2 = LoveListFactory(title="My second list")
        self._stderr = StringIO()

    def schedule(self, love_list, start_date):
        return PromotionScheduler.objects.create(
            love_list=love_list, start_date=start_date)

    def call_command(self):
        command = promote_scheduled_love_lists.Command()
        # If we call command.execute it will mask all errors behind sys.exit
        # so we must set these manually instead
        command.stderr = self._stderr
        command.handle()

    def get_errors(self):
        self._stderr.seek(0)
        return self._stderr.read()

    def test_working(self):
        self.schedule(self.list1, date.today())
        self.call_command()
        schedule = PromotionScheduler.objects.get()

        self.assertTrue(schedule.actioned)
        promoted_list = \
            LoveList.objects.exclude(promoted=None).order_by("-promoted")[0]
        self.assertEqual(promoted_list, self.list1)
        self.assertEqual(self.get_errors(), "")

    def test_no_scheduler_today(self):
        today = date.today()
        today_str = today.strftime(self.DATE_FORMAT)

        # Schedule for tomorrow
        self.schedule(self.list1, today + timedelta(days=1))
        with self.assertRaises(CommandError) as ex:
            self.call_command()
        expected = "No scheduler with start date %s." % today_str
        self.assertEqual(ex.exception.args, (expected, ))

        # Schedule for yesterday
        yesterday = today - timedelta(days=1)
        self.schedule(self.list1, yesterday)
        with self.assertRaises(CommandError) as ex:
            self.call_command()
        expected = "No scheduler with start date %s." % today_str
        self.assertEqual(ex.exception.args, (expected, ))

        self.assertEqual(self.get_errors(), (
            "Warning: The following PromotionScheduler objects are still not "
            "actioned:\n\tPromote My first list on %s\n" %\
                    yesterday.strftime(self.DATE_FORMAT)))

    def test_multiple_schedulers_today(self):
        today = date.today()
        today_str = today.strftime(self.DATE_FORMAT)

        self.schedule(self.list1, today)
        self.schedule(self.list2, today)
        with self.assertRaises(CommandError) as ex:
            self.call_command()
        self.assertEqual(ex.exception.args, (
            "Not sure which of [My first list, My second list] to promote", ))

        self.assertEqual(self.get_errors(), (
            "Warning: The following PromotionScheduler objects are still not "
            "actioned:\n\tPromote My first list on {today}\n\tPromote My "
            "second list on {today}\n".format(today=today_str)))
