import os
import sys
sys.path.insert(0, os.path.join('..', '..', '..', '..', '..'))

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError, make_option
from adspygoogle import AdWordsClient
from adspygoogle.common import Utils

from marketplace.models import Product
import codecs


class Command(BaseCommand):
    help = "Create a Google AdWords Ad for a particular product"
    args = "product.id"

    def handle(self, *args, **options):
        if len(args) != 1:
            raise CommandError("Usage: <product.id>")

        product_id = args

        product = Product.objects.get(pk=product_id)
        campaign_name = 'PLA - %s' % product.category_tree

        client = AdWordsClient(path=os.path.join('..', '..', '..', '..', '..'))
        campaign_service = client.GetCampaignService(version='v201306')

        selector = {
            'fields': ['Id', 'Name', 'Status'],
            'paging': {
                'startIndex': str(0),
                'numberResults': str(10)
            },
            'predicates': [{
                'field': 'Name',
                'operator': 'EQUALS',
                'values': ['PLA - Animals and Pets > Houses and Kennels > Houses']
            }]
        }