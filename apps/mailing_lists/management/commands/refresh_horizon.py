from __future__ import print_function

from urlparse import urljoin

from django.core.management.base import NoArgsCommand

from marketplace.models import Product

from mailing_lists.integrations.sailthru import Sailthru


class FakeRequest(object):

    URI_BASE = "http://www.ecomarket.com/"

    def build_absolute_uri(self, url):
        return urljoin(self.URI_BASE, url)


class Command(NoArgsCommand):

    help = "Tell Sailthru's Horizon to respider all published products"

    def handle_noargs(self, **options):
        sailthru = Sailthru(FakeRequest())
        for count, product in enumerate(Product.objects.live(), 1):
            sailthru.update_product(product)
            if count % 100 == 0:
                print("Updated {} products".format(count), file=self.stdout)
        # Final count (don't repeat)
        if count % 100 != 0:
            print("Updated {} products".format(count), file=self.stdout)
