# -*- encoding: utf-8 -*-
#
# This is old code that was never really used, but is somehow worth keeping it.
# If you are reading this after Sep 2014 you may just delete the whole file
#
# Have fun!
#
from django.db import models
from django.utils.translation import ugettext_lazy as _


class AdWordsLabel(models.Model):
    label_id = models.IntegerField(null=False, blank=False)
    name = models.CharField(max_length=100, null=False, blank=False, unique=True)

    def __unicode__(self):
        return u"%s" % self.name


OPERATION_TYPE_CHOICES = (
    (10, _('Add Label')),
    (20, _('Remove Label')), # Currently all existing labels are always deleted.
    (30, _('Increase Bid')),
    (40, _('Reduce Bid')),
    (50, _('Pause Ad Group')),
    (60, _('UnPause Ad Group')),
    (70, _('Pause Campaign')),
    (80, _('UnPause Campaign')),
    (90, _('Set Max CPC')),
)

LABEL_CHOICES = (
    (10, _('Experimental')),
)


class AdWordsOperations(models.Model):
    ad_group_id = models.CharField(max_length=30, null=False, blank=False)
    operation_type = models.PositiveSmallIntegerField(choices=OPERATION_TYPE_CHOICES, null=False, blank=False)
    operation_value = models.CharField(max_length=1000, null=False, blank=False)

    datetime_added = models.DateTimeField(
        _('When this operation was generated'),
        auto_now_add=True,
        editable=False
    )
    datetime_applied = models.DateTimeField(_('When was actually applied to AdWords'), null=True, blank=True)
    #checked = models.BooleanField(default=False)


class ProductAdwords(models.Model):
    def recalculate_labels(self, country):
        label = self.get_stage_level(country)

        # To make sure there is only one stage label delete all the others
        other_stage_labels = [x["label_id"] for x in STAGE_LABELS.values() if x["label_id"] != label.label_id]
        delete_labels = self.labels.filter(label_id__in=other_stage_labels)
        self.labels.remove(*delete_labels)

        # check if the product is available
        availability_label = AdWordsLabel.objects.get_or_create(label_id=1, name="out of stock")[0]

        if self.product.stock == 0:
            self.labels.add(availability_label)
        else:
            self.labels.remove(availability_label)

        self.labels.add(label)

        self.set_velocity(label)
        self.set_max_cpc(label)
        self.check_enabled()

    def get_stage_level(self, country):
        value = self.formatted_cost / self.total_price_budget(country)

        if 0 < value <= .5:
            label_data = get_stage_label(100)
        elif 0.5 < value <= .75:
            label_data = get_stage_label(50)
        elif .75 < value <= 1:
            label_data = get_stage_label(25)
        else:
            label_data = get_stage_label(0)

        return AdWordsLabel.objects.get_or_create(label_id=label_data["label_id"], name=label_data["name"])[0]

    def check_enabled(self):
        if self.max_cpc.amount == Decimal("0.01") or self.product.stock == 0:
            self.status = "PAUSED"
        else:
            self.status = "ENABLED"


from decimal import Decimal


STAGE_LABELS = {
    100: {
        "label_id": 100,
        "name": "stage 100",
        "velocity": .5,
        "max_cpc": Decimal("1.0"),
    },
    50: {
        "label_id": 50,
        "name": "stage 50",
        "velocity": .75,
        "max_cpc": Decimal(".5")
    },
    25: {
        "label_id": 25,
        "name": "stage 25",
        "velocity": 1.0,
        "max_cpc": Decimal(".25")
    },
    0: {
        "label_id": 0,
        "name": "stage 0",
        "velocity": 0,
        "max_cpc": Decimal(".01"),
    },
}


def get_stage_label(label_id):
    return STAGE_LABELS[label_id]


##
#
#
#
#
#

@ajax_request
def get_changed_products(request, country_code):
    country = Country.objects.get(code=country_code.upper())

    entries = ProductAdWords.objects.all()[0:100]

    for entry in entries:
        product = entry.product
        price_budget_raw = product.get_price_budget(country) * Decimal(100)
        price_budget = int(price_budget_raw.amount)

    output = [e.to_json() for e in entries]

    return {
        'num_changes': 1,
        'products': output,
    }


@ajax_request
def get_pending_operations(request, country_code):
    # We are currently not doing anything this country_code
    country = Country.objects.get(code=country_code.upper())

    ids = set()
    ads = defaultdict(dict)
    stages = [x["name"] for x in STAGE_LABELS.values()]

    operations = AdWordsOperations.objects.filter(datetime_applied__isnull=True)
    for op in operations:
        ids.add(op.ad_group_id)
        if op.operation_type == 10:
            # Add Labels
            if 'labels' not in ads[op.ad_group_id]:
                ads[op.ad_group_id]['labels'] = []
            ads[op.ad_group_id]['labels'].append(op.operation_value)
        elif op.operation_type == 20:
            if 'delete_labels' not in ads[op.ad_group_id]:
                ads[op.ad_group_id]['delete_labels'] = []
            ads[op.ad_group_id]['delete_labels'].append(op.operation_value)
        elif op.operation_type == 90:
            # Set Max CPC
            if 'max_cpc' not in ads[op.ad_group_id]:
                ads[op.ad_group_id]['max_cpc'] = None
            ads[op.ad_group_id]['max_cpc'] = op.operation_value
        elif op.operation_type == 50:
            # Pause
            ads[op.ad_group_id]['pause'] = True
        elif op.operation_type == 60:
            # UnPause
            ads[op.ad_group_id]['enable'] = True
        elif op.operation_type == 90:
            ads[op.ad_group_id]['max_cpc'] = op.operation_value

    return {
        'stages': stages,
        'ids': list(ids),
        'ads': ads,
    }


urlpatterns = patterns(
    'sem.views',
    url(r'^get_changed_products/(?P<country_code>\w{2})/$','get_changed_products', name='get_changed_products'),
    url(r'^get_pending_operations/(?P<country_code>\w{2})/$','get_pending_operations', name='get_pending_operations'),
)
#
#
#
#

# -*- encoding: utf-8 -*-
from collections import defaultdict
from decimal import InvalidOperation
import io
import json
import os
from django.conf import settings
from django.core.management import BaseCommand
from marketplace.models import Country
from sem import STAGE_LABELS
from sem.models import ProductAdWords, ActiveCampaignId, AdWordsOperations


"""
class Command(BaseCommand):
    help = ""

    def handle(self, *args, **options):
        filename = os.path.join(settings.STATIC_ROOT, "adwords.json")

        activeCampaignsRaw = ActiveCampaignId.objects.all()
        activeCampaigns = [x.campaign for x in activeCampaignsRaw]

        adgroups = ProductAdWords.objects.filter(campaign_id__in=activeCampaigns)
        process_counter = 0
        change_counter = 0
        country = Country.objects.get(code="GB")

        for entry in adgroups:
            try:
                entry.recalculate_labels(country)
            except InvalidOperation:
                # this exception is raised when a product does not ship to a certain country
                print "does not ship", entry.product.get_absolute_url()
                continue

            if entry.changed_essentials:
                entry.has_updates = True
                change_counter += 1

            entry.save()

            process_counter += 1

            if process_counter % 100 == 0:
                print process_counter, "products processed"

        print process_counter, "product Ads processed"
        print change_counter, "product Ads changed"

        # generate json file
        changed_ads = ProductAdWords.objects.filter(campaign_id__in=activeCampaigns)
        output = {}
        ads = defaultdict(dict)
        ids = []
        stages = [x["name"] for x in STAGE_LABELS.values()]

        for ad in changed_ads:
            ids.append(ad.ad_group_id)
            ads[ad.ad_group_id] = {
                'max_cpc': float(ad.max_cpc.amount),
                'labels': [x.name for x in ad.labels.all()]
            }

        output["stages"] = stages
        output["ids"] = ids
        output["ads"] = ads

        with io.open(filename, "w") as f:
            f.write(unicode(json.dumps(output)))
"""


class Command(BaseCommand):
    help = ""

    def handle(self, *args, **options):
        filename = os.path.join(settings.STATIC_ROOT, "adwords.json")

        activeCampaignsRaw = ActiveCampaignId.objects.all()
        activeCampaigns = [x.campaign for x in activeCampaignsRaw]

        adgroups = ProductAdWords.objects.filter(campaign_id__in=activeCampaigns)
        process_counter = 0
        change_counter = 0
        country = Country.objects.get(code="GB")

        for entry in adgroups:
            existing_labels = set([x.name for x in entry.labels.all()])
            try:
                entry.recalculate_labels(country)
            except InvalidOperation:
                # this exception is raised when a product does not ship to a certain country
                print "does not ship", entry.product.get_absolute_url()
                continue

            if entry.changed_essentials:
                entry.has_updates = True
                change_counter += 1

                # add labels
                new_labels = set([x.name for x in entry.labels.all()])
                to_be_added = new_labels - existing_labels
                for x in to_be_added:
                    operation, created = AdWordsOperations.objects.get_or_create(
                        ad_group_id=entry.ad_group_id,
                        operation_type=10,
                        operation_value=x,
                        checked=True,
                    )
                    operation.save()

                # delete labels
                to_be_deleted = existing_labels - new_labels
                for x in to_be_deleted:
                    operation, created = AdWordsOperations.objects.get_or_create(
                        ad_group_id=entry.ad_group_id,
                        operation_type=20,
                        operation_value=x,
                        checked=True,
                    )
                    operation.save()

                # change max_cpc
                operation, created = AdWordsOperations.objects.get_or_create(
                    ad_group_id=entry.ad_group_id,
                    operation_type=90,
                    checked=False
                )
                operation.operation_value = entry.max_cpc.amount
                operation.save()

            entry.save()

            process_counter += 1

            if process_counter % 100 == 0:
                print process_counter, "products processed"

        print process_counter, "product Ads processed"
        print change_counter, "product Ads changed"