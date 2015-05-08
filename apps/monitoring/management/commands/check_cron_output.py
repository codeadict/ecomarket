# -*- encoding: utf-8 -*-
from datetime import timedelta, datetime
from optparse import make_option

from dateutil.parser import parse
from django.core.management import CommandError
from monitoring.lib.nagios_command import NagiosCommand


class Command(NagiosCommand):
    help = "Checks a file for a timestamp"
    option_list = NagiosCommand.option_list + (
        make_option(
            "--filename",
            action="store",
            dest="filename",
            help="Name of the file to be checked",
        ),
        make_option(
            "--hours",
            action="store",
            dest="hours",
            help="Number of hours"
        )
    )

    def handle(self, *args, **options):
        filename = options['filename']
        if not filename:
            raise CommandError("Please set filename: --filename=/tmp/somefile.txt")

        try:
            accept_time = int(options['hours'])
        except ValueError:
            accept_time = None

        if not accept_time:
            raise CommandError("Please specify hours: --hours=[NUMBER]")

        now = datetime.now()

        check_file = open(filename, "r")
        check_date = parse(check_file.readline())

        if now - check_date < timedelta(hours=accept_time):
            self.log_exit(0, "Everything is fine")
        else:
            self.log_exit(2, "No Cron output for at least %d hours" % accept_time)