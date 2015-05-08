from marketplace.management.commands.write_product_feed \
        import Command as BaseCommand
from marketplace.product_feed_ebay import EbayXMLFeedWriter


class Command(BaseCommand):
    ftp_upload_needed = True

    def write_feed(self, currency, country_obj, fh):
        EbayXMLFeedWriter(currency, country_obj).write(fh)
        self.ftp_setting_key = 'EBAY_%s' % country_obj.code