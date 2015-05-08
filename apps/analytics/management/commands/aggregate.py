import json
import urllib2
import datetime
import logging
import pytz
from dateutil import parser

from django.core.management.base import BaseCommand, CommandError
from django.utils.timezone import utc
from django.conf import settings
from django_cron import CronJobBase, Schedule
from django.db.models import Sum
from django.contrib.auth.models import User

from apps.analytics.models import CampaignTrack, AggregateData, LifetimeTrack
from apps.purchase.models import Order
from apps.sem.models import ProductAdWords
from apps.sem.adwords_api_helper import get_ads_cost


logger = logging.getLogger(__name__)

class Command(BaseCommand):
    def pla_data(self, *args, **options):
        if len(args) < 1:
            today = datetime.datetime.now(tz=pytz.utc).replace(hour=0, minute=0, second=0, microsecond=0)
        else:
            today = parser.parse(args[0])
        tomorrow = today + datetime.timedelta(days=1)

        data = dict(
            campaign='PLA'
        )

        # Get cost information for Google AdWords
        data['campaign_cost'] = float(get_ads_cost(today.strftime('%Y%m%d'), today.strftime('%Y%m%d')) / 1000000)

        # These MUST be have come to our site today for first time
        emails_acquired_today = set()
        for ct in CampaignTrack.objects.filter(created_at__gte=today, created_at__lt=tomorrow, name__startswith='PLA - '):
            if ct.email_lead and ct.email_lead.date_added >= today and ct.email_lead.date_added < tomorrow:
                emails_acquired_today.add(ct.email_lead.email_address)
            elif ct.user and ct.user.date_joined >= today and ct.user.date_joined < tomorrow:
                emails_acquired_today.add(ct.user.email)

        # Any customer already acquired earlier should not be considered
        data['daily_acquired'] = len(emails_acquired_today)
        if data['daily_acquired'] == 0:
            data['customer_acquistion_cost'] = 0
        else:
            data['customer_acquistion_cost'] = float(data['campaign_cost'] / data['daily_acquired'])
        gross_merchant_value = 0
        order_count = 0
        for order in Order.objects.filter(created__gte=today, created__lt=tomorrow):
            ct = CampaignTrack.objects.filter(user=order.user).order_by('id')
            if ct.count() and ct[0].name.startswith('PLA - '):
                gross_merchant_value += float(order.total())
                order_count += 1
                try:
                    lt = LifetimeTrack.objects.get(user=order.user)
                    if lt.status < 32:
                        lt.purchased_at = order.user.orders.order_by('-id')[0].created
                        lt.status = 32
                        lt.save()
                except Exception as e:
                    print e

        data['gross_merchant_value'] = gross_merchant_value
        data['order_count'] = order_count
        data['revenue_after_commission'] = float((data['gross_merchant_value'] * 20) / 100)

        adata = AggregateData(**data)
        adata.save()
        if len(args) > 0:
            adata.created_at = today.replace(hour=23, minute=56, second=0, microsecond=0)
            adata.save()

    def organic_data(self, *args, **options):
        # There is no cost for Organic traffic
        if len(args) < 1:
            today = datetime.datetime.now(tz=pytz.utc).replace(hour=0, minute=0, second=0, microsecond=0)
        else:
            today = parser.parse(args[0])
        tomorrow = today + datetime.timedelta(days=1)

        data = dict(
            campaign='organic',
            campaign_cost=0
        )

        # These MUST be have come to our site today for first time
        emails_acquired_today = set()
        for ct in CampaignTrack.objects.filter(created_at__gte=today, created_at__lt=tomorrow, medium='organic'):
            if ct.email_lead and ct.email_lead.date_added >= today and ct.email_lead.date_added < tomorrow:
                emails_acquired_today.add(ct.email_lead.email_address)
            elif ct.user and ct.user.date_joined >= today and ct.user.date_joined < tomorrow:
                emails_acquired_today.add(ct.user.email)

        # Any customer already acquired earlier should not be considered
        data['daily_acquired'] = len(emails_acquired_today)
        # There is no cost for Organic traffic
        data['customer_acquistion_cost'] = 0

        gross_merchant_value = 0
        order_count = 0
        for order in Order.objects.filter(created__gte=today, created__lt=tomorrow):
            ct = CampaignTrack.objects.filter(user=order.user).order_by('id')
            if ct.count() and ct[0].medium == 'organic':
                gross_merchant_value += float(order.total())
                order_count += 1
                try:
                    lt = LifetimeTrack.objects.get(user=order.user)
                    if lt.status < 32:
                        lt.purchased_at = order.user.orders.order_by('-id')[0].created
                        lt.status = 32
                        lt.save()
                except Exception as e:
                    print e

        data['gross_merchant_value'] = gross_merchant_value
        data['order_count'] = order_count
        data['revenue_after_commission'] = float((data['gross_merchant_value'] * 20) / 100)

        adata = AggregateData(**data)
        adata.save()
        if len(args) > 0:
            adata.created_at = today.replace(hour=23, minute=56, second=0, microsecond=0)
            adata.save()

    def all_data(self, *args, **options):
        if len(args) < 1:
            today = datetime.datetime.now(tz=pytz.utc).replace(hour=0, minute=0, second=0, microsecond=0)
        else:
            today = parser.parse(args[0])
        tomorrow = today + datetime.timedelta(days=1)

        # These MUST be have come to our site today for first time
        emails_acquired_today = set()
        for ct in CampaignTrack.objects.filter(created_at__gte=today, created_at__lt=tomorrow):
            if ct.email_lead and ct.email_lead.date_added >= today and ct.email_lead.date_added < tomorrow:
                emails_acquired_today.add(ct.email_lead.email_address)
            elif ct.user and ct.user.date_joined >= today and ct.user.date_joined < tomorrow:
                emails_acquired_today.add(ct.user.email)

        gross_merchant_value = 0
        order_count = 0
        for order in Order.objects.filter(created__gte=today, created__lt=tomorrow):
            gross_merchant_value += float(order.total())
            order_count += 1
        data = dict(
            campaign='all',
            campaign_cost=0,
            daily_acquired=len(emails_acquired_today),
            customer_acquistion_cost=0,
            order_count=order_count,
            gross_merchant_value=gross_merchant_value,
            revenue_after_commission=float((gross_merchant_value * 20) / 100)
        )
        adata = AggregateData(**data)
        adata.save()
        if len(args) > 0:
            adata.created_at = today.replace(hour=23, minute=56, second=0, microsecond=0)
            adata.save()

    def handle(self, *args, **options):
        """
        We aggregate a bunch of data on a daily basis and store in apps.analytics.models.AggregateData.
        This is the cron that does the actualy aggregation.

        We credit a campaign to have acquired a user ONLY if the user came to Eco Market
        for the first time from that campaign.
        """
        logger.debug("Aggregating Profitability Data")
        self.pla_data(*args, **options)
        self.organic_data(*args, **options)
        self.all_data(*args, **options)