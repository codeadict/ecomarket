# -*- encoding: utf-8 -*-
from analytics.models import AggregateData
from monitoring.lib.nagios_command import NagiosCommand
import datetime
from django.utils.timezone import utc


class Command(NagiosCommand):
    help = ""

    def handle(self, *args, **options):
        last_24 = datetime.datetime.utcnow().replace(tzinfo=utc) - datetime.timedelta(hours=24)
        change_counter = AggregateData.objects.filter(created_at__gte=last_24).count()

        if change_counter > 0:
            self.log_exit(0, "Everything is fine!")
        else:
            self.log_exit(2, "No AggregateData was updated in the last 24hours")