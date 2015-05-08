from __future__ import print_function

import csv

from django.core.management.base import BaseCommand, CommandError

from mailing_lists.importer import CsvImporter


class Command(BaseCommand):
    args = 'contact_filename'
    help = ("Import a CSV file into the mailing list table. It is assumed that"
            " all members are lead sellers.")

    def handle(self, *args, **kwargs):
        try:
            filename, = args
        except ValueError:
            raise CommandError("Please specify only one argument")
        # TODO allow custom rejects filename
        importer = CsvImporter("rejects.txt", self.stdout, self.stderr)
        with open(filename) as fh:
            reader = csv.DictReader(fh)
            importer.import_csv(reader)
        if importer.reject_count > 0:
            reject_msg = ("Created/updated file {fn} with {num} new entries")
            print(reject_msg.format(num=importer.reject_count,
                                    fn=importer.reject_filename),
                  file=self.stderr)
