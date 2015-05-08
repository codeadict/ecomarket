import sys
import logging

import os


sys.path.insert(0, os.path.join('..', '..', '..', '..', '..'))

import django
from django.core.management.base import BaseCommand

from apps.sem.models import ProductAdWords
from apps.sem.adwords_api_helper import get_all_product_ads


logger = logging.getLogger(__name__)
PAGE_SIZE = 500


class Command(BaseCommand):
    help = "Sync data from Google AdWords into our own DB"

    def handle(self, *args, **options):
        logger.info("Syncing data from Google AdWords into our own DB")
        all_ads = get_all_product_ads()
        for ad_data in all_ads:
            ad_model = ProductAdWords(**ad_data)
            try:
                ad_model.processed = False
                ad_model.save()
            except django.db.utils.IntegrityError:
                ad_model = ProductAdWords.objects.get(
                    product_id=ad_data['product_id'],
                    ad_group_id=ad_data['ad_group_id']
                )
                ad_model.conversions = ad_data['conversions']
                ad_model.clicks = ad_data['clicks']
                ad_model.cost = ad_data['cost']
                ad_model.average_cpc = ad_data['average_cpc']
                ad_model.impressions = ad_data['impressions']
                ad_model.status = ad_data['status']
                ad_model.processed = False
                ad_model.save()