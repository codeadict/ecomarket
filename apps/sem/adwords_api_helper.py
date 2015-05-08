import time

import os
from adspygoogle.adwords.AdWordsClient import AdWordsClient

PAGE_SIZE = 400


def perform_adgroup_operations(operations):
    """
    Performs a batch of AdWords operations.

    :param operations: list of operations
    :return: tuple of processed operations
    """
    client = _get_client()

    ad_group_service = client.GetAdGroupService(version='v201306')
    ad_groups = ad_group_service.Mutate(operations)

    return ad_groups


def get_adgroup_data(ad_group_list, date_start, date_end):
    client = _get_client()

    ad_group_service = client.GetAdGroupService(version='v201306')

    offset = 0
    selector = {
        'fields': ['Id', 'Cost'],
        'predicates': [
            {
                'field': 'AdGroupId',
                'operator': 'IN',
                'values': ad_group_list
            }
        ],
        'dateRange': {
            'min': date_start.strftime('%Y%m%d'),
            'max': date_end.strftime('%Y%m%d')
        },
        'paging': {
            'startIndex': str(offset),
            'numberResults': str(PAGE_SIZE)
        }
    }

    more_pages = True
    while more_pages:
        page = ad_group_service.Get(selector)[0]

        # Display results.
        if 'entries' in page:
            for ad_group in page['entries']:
                yield ad_group
        else:
            print 'No ad groups were found.'

        offset += PAGE_SIZE
        selector['paging']['startIndex'] = str(offset)
        more_pages = offset < int(page['totalNumEntries'])




def get_all_product_ads():
    client = _get_client()
    ad_group_criterion_service = client.GetAdGroupCriterionService(version='v201306')
    offset = 0

    selector = {
        'fields': ['Id', 'Argument', 'AdGroupId', 'Operand', 'Text'],
        'paging': {
            'startIndex': str(offset),
            'numberResults': str(PAGE_SIZE)
        }
    }

    more_pages = True
    all_product_ads = []
    all_ad_group_ids = []
    while more_pages:
        page = ad_group_criterion_service.Get(selector)[0]
        # Display results.
        if 'entries' in page:
            for entry in page['entries']:
                if entry['criterion']['Criterion_Type'] == 'Product' and 'conditions' in entry['criterion']:
                    try:
                        product_id = int(entry['criterion']['conditions'][0]['argument'])
                        if product_id > 0:
                            """print 'ProductId %s, AdGroupId %s' % (
                                entry['criterion']['conditions'][0]['argument'],
                                entry['adGroupId']
                            )"""
                            all_product_ads.append({
                                'product_id': entry['criterion']['conditions'][0]['argument'],
                                'ad_group_id': entry['adGroupId']
                            })
                    except:
                        pass
        else:
            print 'No ad group criterion was found.'
        offset += PAGE_SIZE
        selector['paging']['startIndex'] = str(offset)
        more_pages = offset < int(page['totalNumEntries'])

        # Uncomment the following 2 lines if you want to test a small batch
        # if len(all_product_ads) >= 1:
        #     break
        time.sleep(1)
        print 'AdGroupCriterionService %s...' % offset

    all_ad_group_ids = [x['ad_group_id'] for x in all_product_ads]
    # print 'Ad Groups: ', len(all_ad_group_ids)

    ad_group_service = client.GetAdGroupService(version='v201306')

    offset = 0
    selector = {
        'fields': ['Id', 'Status', 'AverageCpc', 'Clicks', 'Cost', 'CampaignId', 'Conversions', 'Impressions'],
        'paging': {
            'startIndex': str(offset),
            'numberResults': str(PAGE_SIZE)
        },
        'predicates': [
            # Uncomment the following 5 lines if you want to test a small batch
            # {
            #     'field': 'AdGroupId',
            #     'operator': 'IN',
            #     'values': all_ad_group_ids
            # },
            {
                'field': 'CampaignName',
                'operator': 'STARTS_WITH',
                'values': ['PLA - ']
            }
        ],
    }

    more_pages = True
    while more_pages:
        page = ad_group_service.Get(selector)[0]
        # Display results.
        if 'entries' in page:
            for entry in page['entries']:
                ad_group_id = entry['id']
                try:
                    ad_idx = all_ad_group_ids.index(ad_group_id)
                    all_product_ads[ad_idx]['status'] = entry['status']
                    all_product_ads[ad_idx]['conversions'] = int(entry['stats']['conversions'])
                    all_product_ads[ad_idx]['clicks'] = int(entry['stats']['clicks'])
                    all_product_ads[ad_idx]['cost'] = int(entry['stats']['cost']['microAmount'])
                    all_product_ads[ad_idx]['average_cpc'] = int(entry['stats']['averageCpc']['microAmount'])
                    all_product_ads[ad_idx]['impressions'] = int(entry['stats']['impressions'])
                    all_product_ads[ad_idx]['campaign_id'] = entry['campaignId']
                except Exception as e:
                    # print e
                    pass
        else:
            print 'No ad group was found.'
        offset += PAGE_SIZE
        selector['paging']['startIndex'] = str(offset)
        more_pages = offset < int(page['totalNumEntries'])
        time.sleep(1)
        print 'AdGroupService %s...' % offset

    ads_with_data = []
    for ad in all_product_ads:
        if 'conversions' in ad \
            and 'clicks' in ad \
            and 'cost' in ad \
            and 'average_cpc' in ad \
            and 'impressions' in ad:
            ads_with_data.append(ad)
    return ads_with_data


def get_ads_cost(date_min, date_max, client=None):
    if not client:
        client = AdWordsClient(path=os.path.join('..', '..', '..', '..', '..'))
    ad_group_service = client.GetAdGroupService(version='v201306')
    cost = 0

    offset = 0
    selector = {
        'fields': ['Id', 'Cost'],
        'paging': {
            'startIndex': str(offset),
            'numberResults': str(PAGE_SIZE)
        },
        'predicates': [
            {
                'field': 'CampaignName',
                'operator': 'STARTS_WITH',
                'values': ['PLA - ']
            }
        ],
        'dateRange': {
            'min': date_min,
            'max': date_max
        }
    }

    more_pages = True
    while more_pages:
        page = ad_group_service.Get(selector)[0]
        # Display results.
        if 'entries' in page:
            for entry in page['entries']:
                cost += int(entry['stats']['cost']['microAmount'])
        else:
            print 'No ad group was found.'
        offset += PAGE_SIZE
        selector['paging']['startIndex'] = str(offset)
        more_pages = offset < int(page['totalNumEntries'])
        time.sleep(1)
        print 'AdGroupService %s...' % offset
    return cost

def _get_client():
    return AdWordsClient(path=os.path.join('..', '..', '..', '..', '..'))



if __name__ == '__main__':
  get_all_product_ads()
