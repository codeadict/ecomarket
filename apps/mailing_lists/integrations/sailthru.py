from __future__ import absolute_import

import logging

import IPy

from sailthru.sailthru_client import SailthruClient

from django.conf import settings
from django.contrib.auth.models import User

logger = logging.getLogger(__name__)


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


class SailthruError(Exception):
    pass


class ApiKeyNotSet(SailthruError):
    pass


class Sailthru(object):

    def __init__(self, request):
        if settings.SAILTHRU_API_KEY in [None, '']:
            self._api = None
        else:
            self._api = SailthruClient(settings.SAILTHRU_API_KEY,
                                       settings.SAILTHRU_API_SECRET)
        self.request = request

    @property
    def api(self):
        if self._api is None:
            raise ApiKeyNotSet()
        return self._api

    def enabled(self):
        """
        Is SailThru integration enabled?
        """
        # TODO: Is this necessary? Exception handling is a much better way
        # to deal with this kind of thing...
        return self._api is not None

    def login(self, user):
        if self.request is None or not self.enabled():
            return None
        sailthru_hid = self.request.COOKIES.get('sailthru_hid', None)
        sailthru_vars = {}

        # We send the "persistent" utm cookie (first one) data to sailthru.
        # That data would be in the DB, else from current request
        campaign = {}
        from apps.analytics.models import CampaignTrack
        ct = CampaignTrack.objects.filter(user=user).\
            order_by('-created_at')
        if ct and not ct[0].sent_to_sailthru:
            values = ct.values('source', 'name', 'medium', 'term', 'content')
            campaign = values[0]
            ct = ct[0]
            ct.sent_to_sailthru = True
            ct.save()
        elif self.request.campaign:
            campaign = self.request.campaign

        if campaign:
            for k, v in campaign.items():
                sailthru_vars['campaign_%s' % k] = v

        if not sailthru_hid:
            try:
                response = self.api.api_post('user', {
                    'id': user.email,
                    'fields': {'keys': 1},
                    'login': {
                        'site': 'www.ecomarket.com',
                        'ip': _get_request_ip(self.request),
                        'user_agent': self.request.META.get(
                            'HTTP_USER_AGENT', '')
                    },
                    'vars': sailthru_vars
                })
                if response.is_ok():
                    sailthru_hid = response.response.json['keys']['cookie']
                    self.request.set_sailthru_hid = sailthru_hid
            except:
                logger.warn('Could not set users sailthru_hid token',
                            exc_info=True)

    def signup(self, user=None, email=None):
        from mailing_lists.models import MailingListSignup

        # Allow either user or e-mail to be passed
        if self.request is None or not self.enabled():
            return None
        if email is None and user is not None:
            email = user.email
        if email is None:
            return None
        if user is None:
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                pass

        # Default to Allow Marketing
        sailthru_vars = {
            'notifications_site_updates_features': True,
            'notifications_stall_owner_tips': True,
            'notifications_product_curations': True,
            'notifications_blog_posts': True
        }

        try:
            # and sync the full sailthru info etc. if they have a MLS
            mls = MailingListSignup.objects.get(email_address=email)
            sailthru_vars = mls.export()
        except MailingListSignup.DoesNotExist:
            if user is not None:
                # mls.export will have these, but if there's no MLS object for
                # some reason then we might as well set it manually
                sailthru_vars['notifications_site_updates_features'] = \
                    sailthru_vars['notifications_stall_owner_tips'] = \
                    sailthru_vars['notifications_product_curations'] = \
                    sailthru_vars['notifications_blog_posts'] = \
                    user.email_notification.send_newsletters

        # Sync Google utm_ cookies when users signup
        if self.request.campaign:
            for k, v in self.request.campaign.items():
                sailthru_vars['campaign_%s' % k] = v

        # Notify Sailthru of new login & sync their vars
        try:
            response = self.api.api_post('user', {
                'id': email,
                'fields': {'keys': 1},
                'login': {
                    'site': 'www.ecomarket.com',
                    'ip': _get_request_ip(self.request),
                    'user_agent': self.request.META.get('HTTP_USER_AGENT', '')
                },
                'vars': sailthru_vars
            })
            if response.is_ok():
                # Middleware will set the sailthru_hid cookie for Horizon
                sailthru_hid = response.response.json['keys']['cookie']
                self.request.set_sailthru_hid = sailthru_hid
        except:
            logger.warn('Could not synchronise new user with SailThru',
                        exc_info=True)

    def update_product(self, product):
        """Tell Sailthru to (re)spider a product that has been published"""
        response = self.api.api_post('content', {
            'url': self.request.build_absolute_uri(product.get_absolute_url()),
            'spider': True,
        })
        self.check_response(response)
        logger.info("Respider scheduled on product with ID {}".format(
            product.id))

    def change_email(self, old_email, new_email):
        assert isinstance(old_email, basestring)
        assert isinstance(new_email, basestring)
        if not self.enabled():
            logger.warn(
                'Cannot change %s to %s on SailThru, SailThru is disabled'
                % (old_email, new_email))
            return False
        user_data = self.get_user_data(email=old_email)
        if user_data is None:
            logger.warn(
                'Cannot change %s to %s on SailThru, could not find record on '
                'SailThru' % (old_email, new_email))
            return False
        sailthru_id = user_data['keys']['sid']
        self.api.api_post('user', {'key': 'sid',
                                   'id': sailthru_id,
                                   'keys': {'email': new_email}})
        return True

    def check_response(self, response, error_class=SailthruError):
        if not response.is_ok():
            error = response.get_error()
            raise SailthruError(error.message, error.code)
        return response.get_body()

    def get_user_data(self, sailthru_id=None, email=None):
        if sailthru_id is not None:
            key = 'sid'
            lookup_id = sailthru_id
        elif email is not None:
            key = 'email'
            lookup_id = email
        else:
            raise RuntimeError("Must pass either sailthru_id or email")
        results = self.api.api_get('user', {
            'key': key,
            'id': lookup_id,
            'fields': {'vars': 1, 'keys': 1},
        })
        self.check_response(results)
        return results.response.json

    def get_item_details(self, item, order=None):
        """
        @item may be a CartProduct or a LineItem. It doesn't matter as they
        have the same API, more or less.
        """
        try:
            # item is a CartProduct
            price = item.unit_price
        except AttributeError:
            # item is a LineItem
            price = item.price
        try:
            product = item.product
        except:
            short_return = {
                "id": item.product_id,
                "qty": item.quantity,
                "title": 'Product %d' % (item.product_id,),
                'tags': ['unknown-product'],
                'url': 'http://www.ecomarket.com/',
                # Price in cents
                "price": int(price.amount * 100),
                'vars': {}
            }
            if order is not None:
                short_return['vars']['order_id'] = order.id
            return short_return
        absolute_uri = self.request.build_absolute_uri
        details = {
            "qty": item.quantity,
            "title": product.title,
            # Price in cents
            "price": int(price.amount * 100),
            "id": product.id,
            "url": absolute_uri(product.get_absolute_url()),
            "tags": [keyword.title for keyword in product.keywords.all()],
            "vars": {
                "image_uri": absolute_uri(product.image.url),
                "image_thumb50_uri": absolute_uri(product.image.url_50),
                "image_thumb100_uri": absolute_uri(product.image.url_100),
                "stall_description": product.stall.description_short,
                "stall_uri": absolute_uri(product.stall.get_absolute_url()),
                "stall_twitter": product.stall.twitter_username,
                "stall_desc_short": product.stall.description_short,
                "stall_name": product.stall.title,
                "stall_username": product.stall.user.username,
                "product_category": product.primary_category.name,
            }
        }
        if order is not None:
            details["vars"]["order_id"] = order.id
        return details

    def cart_updated(self, cart):
        """
        The user has added products to their cart, sync cart contents with
        SailThru
        """
        if cart.user is None:
            # Not possible to tell email address
            return
        if not self.enabled():
            msg = 'Not sending {} to SailThru because SailThru disabled'
            logger.warn(msg.format(cart))
            return None
        items = [self.get_item_details(cart_product)
                 for cart_stall in cart.cart_stalls.all()
                 for cart_product in cart_stall.cart_products.all()]
        message_id = None
        if self.request is not None:
            message_id = self.request.COOKIES.get("sailthru_hid", None)
        response = self.api.purchase(
            cart.user.email, items, message_id=message_id,
            options={"incomplete": 1})
        self.check_response(response)

    def order_purchased(self, order):
        if not self.enabled():
            msg = 'Not sending {} to SailThru because SailThru disabled'
            logger.warn(msg).format(order)
            return None
        items = [self.get_item_details(item, order)
                 for item in order.line_items.all()]
        message_id = None
        if self.request is not None:
            # This must be `sailthru_bid` as per
            # http://getstarted.sailthru.com/api/purchase
            message_id = self.request.COOKIES.get("sailthru_bid", None)
        order_options = {
            'date': order.created.strftime('%Y-%m-%d %H:%M:%S') + ' UTC',
            'adjustments': [
                {
                    'price': (order.delivery_charge.amount * 100),
                    'title': 'Shipping',
                },
            ],
            'tenders': [{
                'price': order.total().amount * 100,
                'title': 'PayPal'
            }]
        }
        response = self.api.purchase(order.user.email, items=items,
                                     message_id=message_id,
                                     options=order_options)
        logger.info('Purchase synchronised: sailthru ID %s'
                    % response.json['purchase']['_id'])
        self.check_response(response)

    def send_template(self, template_name, to_email, context_data,
                      is_test=None):
        if not self.enabled():
            msg = 'Not sending {} to {} via SailThru because SailThru disabled'
            logger.warn(msg).format(template_name, to_email)
            return None
        if is_test is None:
            is_test = getattr(settings, 'SAILTHRU_TEST', True)
        is_test = bool(is_test)
        response = self.api.send(template_name, to_email, context_data,
                                 {"test": is_test})
        return self.check_response(response)
