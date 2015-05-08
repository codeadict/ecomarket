from datetime import datetime
import random

from django.core.urlresolvers import reverse
from django.db import DatabaseError
from django.http import HttpResponsePermanentRedirect, HttpResponseRedirect, Http404
import gc
import pytz
import urlparse
import urllib

# Importable elsewhere
from absolute_uri_by_site import absolute_uri

from .mixpanel_tracking import *

def get_timezone_from_offset(minutes, default='US/Eastern'):
    """Return pytz timezone give offset in minutes.

    If none found, then returns the EST as the default timezone.
    Javascript sends offset in minutes. -120 = GMT+0200, we're storing that in  request.COOKIES.get('timezone_offset')

    minutes = request.COOKIES.get('timezone_offset') or 0
    """
    if minutes < 0:
        minutes = -minutes
        minus = True
    else:
        minus = False

    min = minutes % 60
    hours = (minutes - min) / 60
    offset = "%s%02d%02d" % (minus and "+" or "-", hours, min)

    # This is only method I found to determine timezone by offset.
    # HACK: doing reversed(), to match offset 240, to EST instead of AST
    for tz in reversed(pytz.common_timezones):
        now = datetime.now(pytz.timezone(tz))
        if now.strftime("%z") == offset:
            return tz
    return pytz.timezone(default)


def queryset_iterator(queryset, chunksize=1000):
    """Iterate over a Django Queryset ordered by the primary key

    This method loads a maximum of chunksize (default: 1000) rows in it's
    memory at the same time while django normally would load all rows in it's
    memory. Using the iterator() method only causes it to not preload all the
    classes.

    Note that the implementation of the iterator does not support ordered query sets.

    Source: http://djangosnippets.org/snippets/1949/
    """
    pk = 0
    last_pk = queryset.order_by('-pk')[0].pk
    queryset = queryset.order_by('pk')
    while pk < last_pk:
        for row in queryset.filter(pk__gt=pk)[:chunksize]:
            pk = row.pk
            yield row
        gc.collect()


def redirect_to(view_name=None, permanent=False, pass_params=True):
    """Redirects to the view specified using reverse().

    view_name   -   Name of the urlpattern, you want to redirect to.
    permanent   -   If True it performs a 301 permanent redirect. Default is False.
    pass_params -   if False, ignores the args, kwargs to the view and doesn't pass to the target view.
                    This is used if you're redirecting old/legacy parameterized views to some new static page.
                    Default is True.
    """

    def inner(request, *args, **kwargs):
        if view_name:
            if pass_params:
                redirect_url = reverse(view_name, args=args, kwargs=kwargs)
            else:
                redirect_url = reverse(view_name)

            if permanent:
                return HttpResponsePermanentRedirect(redirect_url)
            else:
                return HttpResponseRedirect(redirect_url)
        raise Http404
    return inner



def add_get_params(url, params):
    """Adds get params to the url, overwrites them if they are already in the
    URL, leaves existing parameters untouched
    """
    uri_without_params = url.split("?")[0]
    query_dict = _get_querydict(url)
    for key, value in params.items():
        query_dict[key] = value
    new_query_string = urllib.urlencode(query_dict)
    return "{0}?{1}".format(
        uri_without_params,
        new_query_string,
    )


def remove_get_param(url, param):
    """Removes the given parameter from the url, leaves everything else
    untouched
    """
    uri_without_params = url.split("?")[0]
    query_dict = _get_querydict(url)
    if param in query_dict:
        del query_dict[param]
    new_query_string = urllib.urlencode(query_dict)
    return "{0}?{1}".format(
        uri_without_params,
        new_query_string,
    )


def _get_querydict(url):
    """Creates a dictionary of get parameters from a query, internal use
    for add_get_params
    """
    querydict = urlparse.parse_qs(urlparse.urlparse(url).query)
    result = {}
    # Acrobatics to get around parse_qs assuming multi-value keys
    for key, value in querydict.items():
        result[key] = value[0]
    return result


from orderable_view import OrderableListView, SortTab
from dynamic_paginate_view import DynamicPaginationMixin

def generate_identifier(model):
    identifier = random.randrange(10000000, 99999999)
    try:
        model.objects.get(identifier=identifier)
        return generate_identifier(model)
    except model.DoesNotExist:
        return identifier
    except DatabaseError:
        return identifier
