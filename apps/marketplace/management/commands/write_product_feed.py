import ftplib
import os

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError, make_option

from marketplace.product_feed import write_feed
from marketplace.models import Country
import codecs


class Command(BaseCommand):
    help = "Generate product_feed file and write to the specified file"
    args = "currency [country] filename"

    ftp_upload_needed = False
    ftp_setting_key = False

    def write_feed(self, currency, country_obj, fh):
        write_feed(currency, country_obj, fh)

    def ftp_upload_feed(self, filename):
        if self.ftp_setting_key:
            ftp_settings = settings.SELLER_FTP_ACCOUNTS[self.ftp_setting_key]
            ftp = ftplib.FTP(ftp_settings['host'])
            try:
                ftp.login(ftp_settings['username'],
                          ftp_settings['password'])
                ftp.storlines("STOR " + ftp_settings['filename'],
                              open(filename))
                print "Uploaded to %s - %s" % (self.ftp_setting_key, ftp_settings['filename'])
            except ftplib.error_perm:
                print "Could not connect to FTP"

            data = []
            ftp.dir(data.append)
            for line in data:
                print "-", line
            ftp.quit()

    def handle(self, *args, **options):
        accepted_currencies = ['GBP', 'USD', 'CAD', 'EUR', 'INR', 'NZD', 'AUD']
        if len(args) != 3:
            raise CommandError("Usage: <currency> <country> <filename>")

        currency, country, filename, = args

        if currency not in accepted_currencies:
            raise CommandError("Currency must be one of: " + accepted_currencies)

        try:
            country_obj = Country.objects.get(code=country)
        except Country.DoesNotExist:
            raise CommandError("Unknown country %s" % (country,))

        with open(filename, "w") as fh:
            self.write_feed(currency, country_obj, fh)

        if self.ftp_upload_needed:
            self.ftp_upload_feed(filename)