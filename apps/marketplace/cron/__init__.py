import json
import urllib2
import datetime
import logging

from django.utils.timezone import utc
from django.conf import settings
from django_cron import CronJobBase, Schedule

from marketplace.models import CurrencyExchangeRate

logger = logging.getLogger(__name__)


class CurrencyUpdateCron(CronJobBase):
    RUN_AT_TIMES = ['1:00']

    schedule = Schedule(run_at_times=RUN_AT_TIMES)
    code = 'marketplace.cron.currency_update_cron'

    def do(self):
        """
        We use a free plan on OpenExchangeRates (OXR) to get the data.
        In the free plan we receive USD as base currency.
        We do the math for the needed conversion to base GBP.
        """
        url_to_fetch = 'http://openexchangerates.org/api/latest.json?app_id=%s' % settings.OPENEXCHANGE_RATE_APP_ID
        # We save only required rates, add more to this list as needed
        required_currencies = ['USD', 'EUR', 'CAD', 'AUD', 'INR', 'SEK', 'JPY']
        # We set this fixed for a batch (hourly cron), in case we need to find the rates for a whole batch.
        current_data_time = datetime.datetime.utcnow().replace(tzinfo=utc)
        try:
            url_handle = urllib2.urlopen(url_to_fetch)
            json_data = json.load(url_handle)

            # We store GBP as base, do the math as needed.
            base_currency = 'GBP'
            gbp_rate = json_data['rates']['GBP']
            for curr, rate in json_data['rates'].items():
                if curr in required_currencies:
                    c = CurrencyExchangeRate()
                    c.base_currency = base_currency
                    c.currency = curr
                    c.date_time = current_data_time
                    c.exchange_rate = rate / gbp_rate
                    c.save()

            # Now we separately store USD rate, since it does not come in the free plan of OXR
            c = CurrencyExchangeRate()
            c.base_currency = base_currency
            c.currency = 'USD'
            c.date_time = current_data_time
            c.exchange_rate = 1 / gbp_rate
            c.save()
        except:
            logger.warn("There was an error updating the currency list at {0}".format(current_data_time))
