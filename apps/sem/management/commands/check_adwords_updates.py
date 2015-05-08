# -*- encoding: utf-8 -*-
from monitoring.lib.nagios_command import NagiosCommand
from sem.models import ProductAdWords
import datetime
from django.utils.timezone import utc


class Command(NagiosCommand):
    help = ""

    def handle(self, *args, **options):
        last_24 = datetime.datetime.utcnow().replace(tzinfo=utc) - datetime.timedelta(hours=24)
        change_counter = ProductAdWords.objects.filter(datetime_updated__gte=last_24).count()

        if change_counter > 0:
            self.log_exit(0, "Everything is fine!")
        else:
            self.log_exit(2, "No ProductAdword was updated in the last 24hours")