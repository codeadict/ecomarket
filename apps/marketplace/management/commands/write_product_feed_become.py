from django.conf import settings

from marketplace.management.commands.write_product_feed \
        import Command as BaseCommand
from marketplace.product_feed_become import write_feed


class Command(BaseCommand):
    help = ("Generate product_feed file and write to the specified file, then "
            "upload the file to Amazon's servers")
    ftp_upload_needed = True

    def write_feed(self, currency, country_obj, fh):
        write_feed(currency, country_obj, fh)
        self.ftp_setting_key = 'BECOME_%s' % country_obj.code