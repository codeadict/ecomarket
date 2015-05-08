import uuid
import datetime
import calendar
import pytz

from django.core.cache import cache
from django.contrib.sites.models import get_current_site
from django.utils.timezone import utc

from apps.analytics.models import LifetimeTrack
from apps.purchase.models import Cart


class ClicktaleSettingsMiddleware(object):
    def process_request(self, request):
        clicktale = type("Clicktale", (object,), {})()
        clicktale.record = False
        clicktale.hash = uuid.uuid4().hex
        clicktale.domain = get_current_site(request).domain
        request.clicktale = clicktale


class ClicktaleRecordMiddleware(object):
    def process_response(self, request, response):
        """
        Save current page output into cache if asked to do so
        """
        if hasattr(request, 'clicktale') and request.clicktale.record:
            clicktale = request.clicktale
            cache.set(clicktale.hash, response, 1800)
        return response


class LifetimeTrackMiddleware(object):
    def process_request(self, request):
        import pickle as serializer
        lt = None
        if 'EMLIFEID' in request.COOKIES and not hasattr(request, 'lifetime_track'):
            try:
                cookie_value = serializer.loads(request.COOKIES['EMLIFEID'])
                lt = LifetimeTrack.objects.get(cookie_key=cookie_value['k'])
                request.lifetime_track = lt
            except Exception as e:
                pass

    def process_response(self, request, response):
        import pickle as serializer
        now = calendar.timegm(datetime.datetime.now(tz=pytz.utc).utctimetuple())
        cookie_key = uuid.uuid4().hex
        url_count = 1
        lt = None

        if 'EMLIFEID' not in request.COOKIES:
            # This is the first visit.
            # Cookie has unique ID, current time, URL count
            cookie_value = dict(
                k=cookie_key, # Cookie key
                v=now, # first visit datetime
                t=[now], # list of visit datetime
                a=None, # time of activation
                r=None, # time of retention
                rf=None, # time of referral
                p=None, # time of first purchase
            )
        else:
            time_on_site = 0
            try:
                cookie_value = serializer.loads(request.COOKIES['EMLIFEID'])
                if len(cookie_value['t']) < 5:
                    cookie_value['t'].append(now) # list of visit datetime
                url_count = len(cookie_value['t'])
                if len(cookie_value['t']) > 1:
                    x = cookie_value['t']
                    time_on_site = sum([x[n] - x[n - 1] for n in range(1, len(x))])
            except Exception as e:
                cookie_value = dict(
                    k=cookie_key, # Cookie key
                    v=now, # first visit datetime
                    t=[now], # list of visit datetime
                    a=None, # time of activation
                    r=None, # time of retention
                    rf=None, # time of referral
                    p=None, # time of first purchase
                )
            if not cookie_value['a'] and (url_count >= 5 or time_on_site > 30):
                # This visitor is now activated, but has not been acquired (no Email address)
                # So note the time of activation.
                cookie_value['a'] = now # Time of actual activation
            if cookie_value['a'] and not cookie_value['r']:
                diff = now - cookie_value['a']
                if diff > 24*3600:
                    cookie_value['r'] = now

        if 'EMLIFEID' in request.COOKIES and not hasattr(request, 'lifetime_track') and \
            ((hasattr(request, 'user') and request.user.is_authenticated()) or
            (hasattr(request, 'session') and request.session.get('email_lead', None))):
            fresh = False
            if hasattr(request, 'user') and request.user.is_authenticated():
                try:
                    lt = LifetimeTrack.objects.get(user=request.user)
                    if request.session.get('email_lead', None):
                        lt.email_lead_id = int(request.session.get('email_lead', None))
                except LifetimeTrack.DoesNotExist:
                    fresh = True
                if ('p' not in cookie_value or not cookie_value['p']) and request.user.orders.count():
                    dt = request.user.orders.order_by('-id')[0].created
                    cookie_value['p'] = calendar.timegm(datetime.datetime.combine(dt, datetime.time(0, 0, 0, tzinfo=pytz.UTC)).utctimetuple())
            if request.session.get('email_lead', None):
                try:
                    lt = LifetimeTrack.objects.get(email_lead_id=int(request.session.get('email_lead', None)))
                except LifetimeTrack.DoesNotExist:
                    fresh = True

            if not fresh:
                cookie_value['k'] = lt.cookie_key
                lt.save()
            else:
                lt = LifetimeTrack()
                lt.cookie_key = cookie_value['k']
                if hasattr(request, 'user') and request.user.is_authenticated():
                    user = request.user
                    lt.user = user
                    # This should be always set
                    lt.acquired_at = user.date_joined
                    lt.status = 2
                if request.session.get('email_lead', None):
                    try:
                        from apps.mailing_lists.models import MailingListSignup
                        mls = MailingListSignup.objects.get(id=request.session.get('email_lead', None))
                        if not lt.acquired_at:
                            lt.acquired_at = mls.date_added
                            lt.status = 2
                        lt.email_lead_id = int(request.session.get('email_lead', None))
                    except Exception as e:
                        pass
                lt.cookie_key = cookie_value['k']
                if lt.acquired_at:
                    lt.save()

        if hasattr(request, 'lifetime_track') or lt:
            if not lt:
                lt = request.lifetime_track

            if request.session.get('campaign', None):
                try:
                    from apps.analytics.models import CampaignTrack
                    campaign = CampaignTrack.objects.get(id=request.session.get('campaign', None)['id'])
                    campaign.cookie = lt
                    campaign.save()
                except Exception as e:
                    pass
            changed = False
            ###
            # Metrics for Purchase
            ###
            if cookie_value['p'] and lt.status < 32:
                converted_time = datetime.datetime.fromtimestamp(cookie_value['p'], tz=pytz.utc)
                if not lt.status or lt.status < 32:
                    lt.status = 32 # Purchased
                    changed = True
                    lt.purchased_at = converted_time
            ###
            # Metrics for Referred (has this user referred someone)
            ###
            if cookie_value['rf'] and lt.status < 16:
                converted_time = datetime.datetime.fromtimestamp(cookie_value['rf'], tz=pytz.utc)
                if not lt.status or lt.status < 16:
                    lt.status = 16 # Referred
                    changed = True
                if not lt.actual_referred_at:
                    lt.actual_referred_at = converted_time
                    changed = True
                if not lt.referred_at and lt.acquired_at:
                    if lt.acquired_at > converted_time:
                        # This user was acquired after they referred someone
                        lt.referred_at = lt.acquired_at
                        changed = True
                    else:
                        lt.referred_at = converted_time
                        changed = True
            ###
            # Metrics for Retained
            ###
            if cookie_value['r'] and lt.status < 8:
                converted_time = datetime.datetime.fromtimestamp(cookie_value['r'], tz=pytz.utc)
                if not lt.status or lt.status < 8:
                    lt.status = 8 # Retained
                    changed = True
                if not lt.actual_retained_at:
                    lt.actual_retained_at = converted_time
                    changed = True
                if not lt.retained_at and lt.acquired_at:
                    if lt.acquired_at > converted_time:
                        # This user was acquired after they were retained
                        lt.retained_at = lt.acquired_at
                        changed = True
                    else:
                        lt.retained_at = converted_time
                        changed = True
            ###
            # Metrics for Activated
            ###
            if cookie_value['a'] and lt.status < 4:
                converted_time = datetime.datetime.fromtimestamp(cookie_value['a'], tz=pytz.utc)
                if not lt.status or lt.status < 4:
                    lt.status = 4 # Activated
                    changed = True
                if not lt.actual_activated_at:
                    lt.actual_activated_at = converted_time
                    changed = True
                if not lt.activated_at and lt.acquired_at:
                    if lt.acquired_at > converted_time:
                        # This user was acquired after they activated someone
                        lt.activated_at = lt.acquired_at
                        changed = True
                    else:
                        lt.activated_at = converted_time
                        changed = True
            if changed:
                lt.save()

        # 10 years * 12 months * 720 approx hours in a month * 3600 secs in an hour
        response.set_cookie('EMLIFEID', serializer.dumps(cookie_value), 10*12*720*3600)
        return response