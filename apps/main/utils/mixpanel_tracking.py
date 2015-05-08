# coding=utf-8
import json
import logging
import sys
import urllib
import urllib2
from base64 import b64encode

from django.conf import settings
from libsaas.services import mixpanel
import IPy


logger = logging.getLogger("mixpanel")

api = mixpanel.Mixpanel(token=settings.MIXPANEL_TOKEN)

__all__ = ['mixpanel_track', 'mixpanel_engage', 'mixpanel_import']


def _mixpanel_anon(request):
    """
    Check if the user is an Anonymous User according to mixpanel, if they are
    it returns their distinct id
    """
    for key, value in request.COOKIES.items():
        if key.startswith("mp") and key.endswith("_mixpanel"):
            try:
                data = json.loads(urllib.unquote(value))
                if 'distinct_id' in data:
                    return data['distinct_id']
            except:
                continue


def mixpanel_track(request, event_name, properties=None, distinct_id=None):
    if not settings.MIXPANEL_ACTIVE:
        return None

    if properties is None:
        properties = {}
    if request is not None:
        properties = _add_user_properties(request, properties, distinct_id)
    logger.debug("Mixpanel: Tracking event '{0}'' with properties {1}".format(event_name, properties))
    try:
        # Send 'authenticated' one
        if not request.user.is_anonymous():
            api.track(event_name, properties)        

        # Send 'anonymous' one
        anon_distinct_id = _mixpanel_anon(request)        
        if anon_distinct_id is not None:
            if 'mp_name_tag' in properties:
                del properties['mp_name_tag']
            properties['distinct_id'] = anon_distinct_id
            properties['$distinct_id'] = anon_distinct_id
            api.track(event_name, properties)
    except Exception, ex:
        logger.warning(
            "Mixpanel: Failed to track event '{0}' with properties {1}".format(event_name, properties),
            exc_info=ex
        )
        return None


def _add_user_properties(request, properties, distinct_id=None):
    user = request.user
    try:
        user_profile = user.get_profile()
    except AttributeError:
        user_profile = None
    try:
        user_stall = user.stall
    except:
        user_stall = None
    try:
        user_cart = user.cart
    except:
        user_cart = None
    if 'ip' not in properties:
        properties['ip'] = _get_request_ip(request)
    if 'distinct_id' not in properties:
        if distinct_id is None:
            distinct_id = _get_distinct_user_id(request)
        if distinct_id is not None:
            properties['distinct_id'] = distinct_id
            properties['$distinct_id'] = distinct_id
    properties.update({
        'mp_page': request.build_absolute_uri(),
        '$referrer': request.META.get('HTTP_REFERER', ''),
        'mp_referrer': request.META.get('HTTP_REFERER', ''),        
    })
    if user_profile is not None:
        properties.update({
            'gender': user_profile.get_gender_display(),
            'email': user.email,
            '$email': user.email,        
            'first_name': user.first_name,
            'last_name': user.last_name,
            'name': user.get_full_name(),
            '$username': user.username,
            'username': user.username,
            'mp_name_tag': user.get_full_name()
        })
    if user_cart:
        properties["Items in Cart"] = user_cart.num_items()
    if user_stall:
        properties['Member Type'] = 'Stall Owner'
    else:
        properties['Member Type'] = 'Regular'
    return replace_datetime_properties_with_string(properties)


def mixpanel_engage(request, properties, distinct_id=None):
    if not settings.MIXPANEL_ACTIVE:
        return None
    
    properties = replace_datetime_properties_with_string(properties)
    if distinct_id is None:
        distinct_id = _get_distinct_user_id(request)
        if distinct_id is None:
            return False

    if '$ip' not in properties and request is not None:
        properties['$ip'] = _get_request_ip(request)
    logger.debug("Mixpanel: Engaging user {0} with properties {1}".format(
        distinct_id, properties))
    try:
        return api.engage(distinct_id, properties)
    except Exception:
        logger.warning(
            "Mixpanel: Failed to engage with properties {}".format(properties),
            exc_info=sys.exc_info())
        return None


def mixpanel_import(event_name, properties):
    """
    libsaas doesn't support 'import', so we have to do it manually
    """
    properties['token'] = settings.MIXPANEL_TOKEN
    packet = b64encode(json.dumps({
        'event': event_name,
        'properties': properties
    }))
    url = 'http://api.mixpanel.com/import/'
    data = urllib.urlencode(dict(data=packet, api_key=settings.MIXPANEL_TOKEN))
    req = urllib2.Request(url, data)
    rsp = urllib2.urlopen(req)
    return rsp.read() == '1'


def _get_request_ip(request):
    if "X_FORWARDED_FOR" in request.META:
        forwarded_for = request.META["X_FORWARDED_FOR"]
        ipstrings = [ipstring.strip() for ipstring in forwarded_for.split(",")]
        result = ipstrings[-1]
        for ipstring in ipstrings:
            ip = IPy.IP(ipstring)
            if ip.iptype() == 'PUBLIC':
                result = ipstring
                break
        return result
    return request.META["REMOTE_ADDR"]


def _get_distinct_user_id(request):
    if hasattr(request, "user") and not request.user.is_anonymous():
        return request.user.id


def get_remote_ip_from_x_forwarded_for(x_forwarded_for):
    """Returns the leftmost non private IP address"""
    ipstrings = [ipstring.strip() for ipstring in x_forwarded_for.split(",")]
    result = ipstrings[-1]
    for ipstring in ipstrings:
        ip = IPy.IP(ipstring)
        if ip.iptype() == 'PUBLIC':
            result = ipstring
            break
    return result


def get_request_properties(request):
    props = {}
    if hasattr(request, "user") and not request.user.is_anonymous():
        props["distinct_id"] = request.user.id
    if "X_FORWARDED_FOR" in request.META:
        forwarded_for = request.META["X_FORWARDED_FOR"]
        props["ip"] = get_remote_ip_from_x_forwarded_for(forwarded_for)
    else:
        props["ip"] = request.META["REMOTE_ADDR"]
    return props


def replace_datetime_properties_with_string(properties):
    for key, value in properties.items():
        if hasattr(value, "isoformat"):
            properties[key] = value.isoformat()
    return properties
