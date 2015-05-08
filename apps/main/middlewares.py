"""
This module contains some custom middlewares
Docs about default middlewares in django can be found at https://docs.djangoproject.com/en/dev/ref/middleware/
"""
import datetime
from urllib import unquote

from django.conf import settings
from django.core import urlresolvers
from django.contrib.sites.models import Site
from django.http import HttpResponsePermanentRedirect, HttpResponseForbidden

from django.utils.http import urlquote
from django.utils.timezone import utc
from impersonation.views import IMPERSONATING_KEY

from main.utils import get_timezone_from_offset
from marketplace.models import CurrencyExchangeRate
from marketplace import CURRENCY_CHOICES
from apps.analytics.models import LifetimeTrack


ADMIN_SECRET = getattr(settings, 'ADMIN_SECRET', None)
BLOCK_PATHS = getattr(settings, 'ADMIN_SECRET_BLOCK_PATHS', [])


class AdminSecretMiddleware(object):
    """
    Blocks certain path for admin eyes only. You need to append a GET parameter to gain access.
    Eg. /path/?secret , where ADMIN_SECRET = 'secret'

    """
    COOKIE_NAME = 'admin_secret'

    def process_request(self, request):
        if not self.is_secret_protected(request) or \
            (self.is_secret_protected(request) and self.COOKIE_NAME in request.COOKIES) or \
            ADMIN_SECRET in request.GET:
            return None
        return HttpResponseForbidden("Access Denied")

    def process_response(self, request, response):
        if self.is_secret_protected(request) and not self.COOKIE_NAME in request.COOKIES and \
            ADMIN_SECRET in request.GET:
            response.set_cookie(self.COOKIE_NAME, True, max_age=365 * 24 * 60 * 60)
        return response

    def is_secret_protected(self, request):
        for path in BLOCK_PATHS:
            if request.path.startswith(path):
                return True
        return False


class DomainRedirectMiddleware(object):

    """Redirect ecomarket.com to www.ecomarket.com
    Taken from http://eikke.com/django-domain-redirect-middleware/index.html
    """

    def process_request(self, request):
        host = request.get_host()
        site = Site.objects.get_current()

        if host in [site.domain, 'testserver']:
            return None

        # Only redirect if the request is a valid path
        try:
            # One issue here: won't work when using django.contrib.flatpages
            # TODO: Make this work with flatpages :-)
            urlresolvers.resolve(request.path)
        except urlresolvers.Resolver404:
            return None

        new_uri = '%s://%s%s%s' % (
                request.is_secure() and 'https' or 'http',
                site.domain,
                urlquote(request.path),
                (request.method == 'GET' and len(request.GET) > 0) and '?%s' % request.GET.urlencode() or ''
            )

        return HttpResponsePermanentRedirect(new_uri)


class ExceptionUserInfoMiddleware(object):
    """
    Adds user details to request context on receiving an exception, so that they show up in the error emails.

    Add to settings.MIDDLEWARE_CLASSES and keep it outermost or on top if possible. This allows
    it to catch exceptions in other middlewares as well.
    """

    def process_exception(self, request, exception):
        """
        Process the exception.
            `request` - request that caused the exception
            `exception` - actual exception being raised
        """
        try:
            if request.user.is_authenticated():
                request.META['USERNAME'] = str(request.user.username)
                request.META['USER_EMAIL'] = str(request.user.email)
        except:
            pass


class SetRemoteAddrFromForwardedFor(object):
    def process_request(self, request):
        try:
            real_ip = request.META['HTTP_X_FORWARDED_FOR']
        except KeyError:
            pass
        else:
            # HTTP_X_FORWARDED_FOR can be a comma-separated list of IPs.
            # Take just the first one.
            real_ip = real_ip.split(",")[0]
            request.META['REMOTE_ADDR'] = real_ip


class GoogleUtmCookies(object):
    def process_request(self, request):
        # We store a "persistent" version of the utm cookie to Session
        # Basically the first time utm cookie does NOT get overwritten
        if '__utmz' in request.COOKIES and not request.session.get('campaign', None):
            utm_vars = [
                ('source', 'utmcsr'),
                ('name', 'utmccn'),
                ('medium', 'utmcmd'),
                ('term', 'utmctr'),
                ('content', 'utmcct')
            ]
            campaign = {
                'source': None,
                'name': None,
                'medium': None,
                'term': None,
                'content': None
            }
            cookie_data = request.COOKIES['__utmz']
            for param in cookie_data.split("|"):
                try:
                    (k, v) = param.split("=")
                except ValueError:
                    continue
                for token in utm_vars:
                    # This is needed since Google may have other chars before the actual variable name.
                    # https://trello.com/c/nFFc52ib
                    temp = k[len(k) - len(token[1]):]
                    if temp == token[1]: campaign[token[0]] = unquote(v).replace('+', ' ')

            # We store this ONLY once for the lifetime of the user's session
            request.session['campaign'] = campaign

        if 'em_campaign' in request.GET and 'em_source' in request.GET and 'em_medium' in request.GET:
            campaign = {
                'source': request.GET.get('em_source', None),
                'name': request.GET.get('em_campaign', None),
                'medium': request.GET.get('em_medium', None),
                'term': None,
                'content': None,
                'query_string': request.META['QUERY_STRING']
            }
            if request.META.get('QUERY_STRING', None):
                campaign['query_string'] = request.META['QUERY_STRING']
            request.session['campaign'] = campaign

        # We want to store this campaign to the DB for future tracking
        # We want to track unique campaigns from where a user has come in
        if request.session.get('campaign', None) and (request.user.is_authenticated() or
            request.session.get('email_lead', None)):
            campaign = request.session['campaign']
            if not request.session.get('campaign_%s_persisted' % campaign['name'], None):
                from apps.analytics.models import CampaignTrack
                try:
                    if request.session.get('email_lead', None):
                        campaign['email_lead_id'] = int(request.session.get('email_lead', None))
                    ct = CampaignTrack(**campaign)
                    if request.user.is_authenticated():
                        ct.user = request.user
                    if '__utmz' in request.COOKIES:
                        ct.utmz = request.COOKIES['__utmz']
                    ct.save()
                    request.session['campaign_%s_persisted' % campaign['name']] = True
                    campaign['id'] = ct.id
                    request.session['campaign'] = campaign
                except Exception as e:
                    # We have probably already tracked this campaign.
                    # There is nothing much to do here.
                    pass


        request.campaign = {}
        # We set this for use in other parts of the site.
        # This is the "persistent" version of the utm cookie (first time)
        if request.session.get('campaign', None):
            request.campaign = request.session.get('campaign', None)

    def process_response(self, request, response):
        for key, value in request.GET.items():
            if key.startswith('utm_'):
                if key not in request.COOKIES:
                    try:
                        response.set_cookie(str(key), str(value), max_age=365*24*60*60)
                    except:
                        pass

        return response


class CookieToUserTimezone():
    def process_request(self, request):
        """
        Populates user_profile.timezone with timezone offset set by javascript.
        """
        minutes = int(request.COOKIES.get('timezone_offset') or 0)
        # FIXME: we're not doing anything with this timezone!
        tz = get_timezone_from_offset(minutes)

        if request.user.is_authenticated():
            pass
            # Process timezone, or save to db etc.


class UserLocaleMiddleware(object):
    """
    This ensures that user Locale information, such as their County and
    Preferred Currency is kept up to date whenever it changes (either via
    connecting from a different country, or changing their preferred Currency
    from the dropdown).

    This is persisted to their profile so the next time they login it is picked
    up again.
    """
    def process_request(self, request):
        country = request.META.get('HTTP_CF_IPCOUNTRY', 'GB')
        currency = request.session.get('preferred_currency', None)

        if request.user.is_authenticated() and not request.session.get(IMPERSONATING_KEY):
            profile = request.user.get_profile()
            profile_needs_save = False
            if profile.detected_country != country:
                profile.detected_country = country
                profile_needs_save = True
            if currency is not None:
                if profile.preferred_currency != currency:
                    profile.saved_currency = currency
                    profile_needs_save = True
            if profile_needs_save:
                profile.save()
            country = profile.detected_country
            currency = profile.preferred_currency

        if request.GET.get('force_country', None) is not None:
            request.country = request.GET.get('force_country', None)
        else:
            request.country = country
        request.preferred_currency = currency
        request.all_currency_rates = CurrencyExchangeRate.get_all_rates()
        request.all_currency_symbols = CURRENCY_CHOICES
