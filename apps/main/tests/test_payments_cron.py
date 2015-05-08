import datetime
from django.test import TestCase
from main.management.commands import payments_cron
import mock
from purchase.models import Payment
from tests import factories

class PaymentsCronTestCase(TestCase):

    def setUp(self):
        created = datetime.datetime.now().date() - datetime.timedelta(days=3)
        self.ready_to_pay = factories.create_order(
            5,
            dispatched=True,
            created=created,
            payment_status=Payment.STATUS_PRIMARY_PAID,
        )
        self.overdue_orders = {}
        for day in [3,7,13,14,15]:
            delta = datetime.timedelta(days=day)
            created = datetime.datetime.now().date() - delta
            self.overdue_orders[day] = factories.create_order(
                5,
                dispatched=False,
                created=created,
                payment_status=Payment.STATUS_PRIMARY_PAID,
            )
        self.command = payments_cron.Command()
        self.notify_patcher = mock.patch.object(payments_cron, "notifier", spec=True)
        self.mock_notifier = self.notify_patcher.start()
        self.addCleanup(self.notify_patcher.stop)

        self.payment_patcher = mock.patch("purchase.models.Order.payment")
        self.mock_payment = self.payment_patcher.start()
        self.addCleanup(self.payment_patcher.stop)

        self.refund_patcher = mock.patch("purchase.models.Order.refund")
        self.mock_refund = self.refund_patcher.start()
        self.addCleanup(self.refund_patcher.stop)

    def test_completed_orders_paid(self):
        self.command.handle()
        # not a very thorough test but it will do
        self.mock_payment.execute.assert_called_once_with()

    def test_overdue_by_3_days_sent_reminder(self):
        self.command.handle()
        self.mock_notifier.send_n_day_reminder.assert_any_call(
            self.overdue_orders[3])

    def test_overdue_by_7_days_sent_reminder(self):
        self.command.handle()
        self.mock_notifier.send_n_day_reminder.assert_any_call(
            self.overdue_orders[7])

    def test_overdue_by_13_days_sent_reminder(self):
        self.command.handle()
        self.mock_notifier.send_n_day_reminder.assert_any_call(
            self.overdue_orders[13])

    def test_overdue_by_14_days_sent_reminder(self):
        self.command.handle()
        self.mock_notifier.send_n_day_reminder.assert_any_call(
            self.overdue_orders[14])

    def test_overdue_notification_not_sent_for_15_day(self):
        self.command.handle()
        calls = self.mock_notifier.send_n_day_reminder.call_args_list
        order_ids = [c[0] for c in calls]
        self.assertTrue(self.overdue_orders[15].id not in order_ids)

    def test_order_to_refund_refunded(self):
        self.command.handle()
        self.mock_refund.assert_called_once_with("More than 14 days without dispatching")
