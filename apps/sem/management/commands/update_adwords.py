# -*- encoding: utf-8 -*-
from decimal import InvalidOperation
from django.utils.datetime_safe import datetime
from marketplace.models import Country

from sem.adwords_api_helper import perform_adgroup_operations
from sem.models import ActiveCampaignId, ProductAdWords

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Create a Google AdWords Ad for a particular product"

    def handle(self, *args, **options):
        try:
            # you can add a slug as an argument to process only one AdWord
            single_slug = args[0]
        except IndexError:
            single_slug = None

        operations = []
        country = Country.objects.get(code="GB")

        if single_slug:
            adgroups = ProductAdWords.objects.filter(product__slug=single_slug)
        else:
            adgroups = ProductAdWords.objects.order_by('datetime_updated')[:1000]

        for ad in adgroups:
            try:
                ad.update_adwords_data(country)
            except InvalidOperation:
                # this exception is raised when a product does not ship to a certain country
                #print "does not ship", ad.product.get_absolute_url()
                continue

            if ad.changed_essentials:
                operations.append({
                    'operator': 'SET',
                    'operand': {
                        'id': ad.ad_group_id,
                        'status': ad.status,
                        'biddingStrategyConfiguration': {
                            'bids': [
                                {
                                    'xsi_type': 'CpcBid',
                                    'bid': {
                                        'microAmount': str(int(ad.max_cpc.amount * 1000000))
                                    },
                                }
                            ]
                        }
                    }
                })

            ad.datetime_updated = datetime.now()
            ad.save()

        if len(operations) > 0:
            result = perform_adgroup_operations(operations)

            for entry in result[0]['value']:
                adword = ProductAdWords.objects.get(
                    ad_group_id=entry['id'], campaign_id=entry['campaignId']
                )
                adword.changed_essentials = False
                adword.save()