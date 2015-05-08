# -*- encoding: utf-8 -*-
import sys
from django.core.management import BaseCommand

ERRORS = {
    0: 'OK',
    1: 'WARNING',
    2: 'CRITICAL',
    3: 'UNKNOWN',
    4: 'DEPENDENT',
}


class NagiosCommand(BaseCommand):
    @classmethod
    def log_exit(cls, level, message):
        level_handle = ERRORS[level]

        print "%s - %s" % (level_handle, message)

        sys.exit(level)
