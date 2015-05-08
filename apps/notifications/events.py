# coding=utf-8
"""
This module handles triggering events when actions are performed on the site.
"""
from django.template import Context, loader
from djipchat.lib import send_to_hipchat


__all__ = 'Events'
import logging
import datetime

from django.core.urlresolvers import reverse
from django.conf import settings

from mailing_lists.integrations.sailthru import Sailthru
from main.utils import mixpanel_track, mixpanel_engage, absolute_uri
from social_network.models import UserFollow
from apps.analytics.models import LifetimeTrack


LOG = logging.getLogger(__name__)


def suffix(d):
    return 'th' if 11 <= d <= 13 else {1: 'st', 2: 'nd', 3: 'rd'}.get(d % 10, 'th')


def custom_strftime(format, t):
    return t.strftime(format).replace('{S}', str(t.day) + suffix(t.day))


def get_mixpanel_info(user, ignore_time=False):
    """
    Dictionary of User properties to be used with mixpanel_engage
    XXX: bad naming
    """
    following = UserFollow.user_follow(user).count()
    followers = UserFollow.user_following(user).count()
    mp_dict = {'$set': {'followers': followers, 'following': following}}

    # This causes MixPanel to leave the 'last seen' alone
    # e.g. when you Follow somebody, it won't update the 'last seen' time
    # of the person being Followed    
    if ignore_time:
        mp_dict['$ignore_time'] = True
    return mp_dict


def merge_lifetime_track(browser_lt, user_lt):
    user_lt.cookie_key = browser_lt.cookie_key
    if not user_lt.acquired_at and browser_lt.acquired_at:
        user_lt.acquired_at = browser_lt.acquired_at
    if not user_lt.activated_at and browser_lt.activated_at:
        user_lt.activated_at = browser_lt.activated_at
    if not user_lt.retained_at and browser_lt.retained_at:
        user_lt.retained_at = browser_lt.retained_at
    if not user_lt.referred_at and browser_lt.referred_at:
        user_lt.referred_at = browser_lt.referred_at
    if not user_lt.purchased_at and browser_lt.purchased_at:
        user_lt.purchased_at = browser_lt.purchased_at
    browser_lt.delete()
    user_lt.save()


class Events(object):
    """
    Trigger site-wide notifications for events which we want to keep track of.

    Usage:

    >>> Events(request).logged_in(request.user)
    """
    def __init__(self, request):
        self.request = request
        self.sailthru = Sailthru(request)

    def _sendmail(self, template_name, to_email, context):
        """
        Use SailThru to deliver a templated e-mail

        :param template_name: SailThru template name
        :param to_email: string E-mail address
        :param context: Dictionary of parameters for the template
        """
        assert isinstance(template_name, basestring)
        assert isinstance(to_email, basestring)
        assert type(context) == dict
        if self.sailthru.enabled():
            response = self.sailthru.send_template(template_name, to_email, context)
            LOG.info("Sent e-mail to %s (SailThru send ID: %s)",
                     response['email'], response['send_id'])
            return response
        else:
            LOG.warn(
                'Not sending template %s to %s because SailThru disabled',
                template_name, to_email
            )
            return None

    def logged_in(self, user):
        """
        The user has logged in to the site

        :param user: User object
        """
        # Integration with sailthru
        if self.sailthru.enabled():
            self.sailthru.login(user)

        # Internal LifetimeTrack
        try:
            lt = LifetimeTrack.objects.get(user=user)
            merge_lifetime_track(self.request.lifetime_track, lt)
        except Exception as e:
            print "=-"*34, e

        # Integration with mixpanel
        try:
            mixpanel_track(
                self.request,
                "logged in",
                {
                    "$last_seen": datetime.datetime.now()
                }
            )
            mixpanel_engage(self.request, {'$add': {'Times Logged In': 1}})
            try:
                has_stall = user.stall is not None
            except:
                has_stall = False
            if has_stall:
                member_type = 'Regular'
            else:
                member_type = 'Stall Owner'
            mixpanel_engage(self.request, {'$set': {
                'last_login': datetime.datetime.now().isoformat(),
                '$email': user.email,
                '$username': user.username,
                '$created': user.date_joined.isoformat(),
                "$last_seen": datetime.datetime.now().isoformat(),
                '$first_name': user.first_name,
                '$last_name': user.last_name,
                'gender': user.user_profile.get_gender_display(),
                'mp_name_tag': user.get_full_name(),
                'Member Type': member_type,
            }})
        except:
            LOG.warn('Could not send login event to MixPanel', exc_info=True)

    def user_changed_email(self, user, old_email, new_email):
        """
        The user has changed their e-mail address

        :param user: User object
        :param old_email: Old e-mail address
        :param new_email: New e-mail address
        """
        from mailing_lists.models import MailingListSignup
        self.sailthru.change_email(old_email, new_email)
        old_mls = MailingListSignup.objects.filter(user=user)

        # Multiple mailing list signup objects for the same user
        # This shouldn't happen, but we can safely clean up.
        if len(old_mls) > 1:
            MailingListSignup.objects.filter(user=user).exclude(email_address=old_email).delete()
            old_mls = MailingListSignup.objects.filter(user=user)        

        if MailingListSignup.objects.filter(email_address=new_email).count() != 0:
            LOG.warn('Cant update MailingListSignup from %s to %s '
                     'because MLS with new email already exists', old_email, new_email)
            return False   

        if len(old_mls) == 1:     
            old_mls[0].email_address = new_email
            old_mls[0].save()

    def cart_updated(self, cart):
        """
        Syncs contents of cart with SailThru and updates MixPanel properties
        for # of items in cart.

        :param cart: Cart object
        """
        try:
            self.sailthru.cart_updated(cart)
            mixpanel_engage(self.request, {'$set': {
                'Items in Cart': cart.num_items()
            }})
        except:
            LOG.error("cart_updated failed", exc_info=True)

    def user_followed(self, follow):
        """
        :param follow: UserFollow object which has just been created
        """
        mixpanel_track(self.request,
                       "Followed User",
                       {"followed_user": follow.target.username})

        mixpanel_engage(self.request,
                        get_mixpanel_info(follow.user),
                        follow.user.id)

        mixpanel_engage(self.request,
                        get_mixpanel_info(follow.target, ignore_time=True),
                        follow.target.id)

        template_name = 'new-follower-notification'
        context = {
            'USER_USERNAME': follow.user.username,
            'USER_PROFILE_URL': absolute_uri(follow.user.get_profile().get_absolute_url()),
            'TARGET_USER_USERNAME': follow.target.username,
            'TARGET_USER_PROFILE_URL': absolute_uri(follow.target.get_profile().get_absolute_url())
        }
        print absolute_uri(follow.user.get_profile().get_absolute_url()), \
            absolute_uri(follow.target.get_profile().get_absolute_url())
        email_notification = follow.target.email_notification
        if email_notification.follower_notifications:
            self._sendmail(template_name, follow.target.email, context)
        else:
            LOG.info(
                "Email not send to %s, since follower_notifications is set to OFF",
                follow.target.email
            )

    def user_unfollowed(self, unfollow):
        """
        :param unfollow: UserFollow object which is about to be deleted
        """
        mixpanel_track(self.request,
                       "Unfollowed User",
                       {"followed_user": unfollow.target.username})

        mixpanel_engage(self.request,
                        get_mixpanel_info(unfollow.user),
                        unfollow.user.id)

        mixpanel_engage(self.request,
                        get_mixpanel_info(unfollow.target, ignore_time=True),
                        unfollow.target.id)

    def message_sent(self, msg):
        """
        A new message has been sent, notify the recipient via e-mail

        :param msg: Message object
        """
        if not msg.parent_msg:
            template_name = "new-message-received"
        else:
            template_name = "message-reply-received"

        # TODO: notification settings

        context = {
            "SENDER_USERNAME": msg.sender.username,
            "MESSAGE_SUBJECT": msg.subject,
            "MESSAGE_BODY": msg.body,
            'MESSAGE_VIEW_URL': absolute_uri(reverse('messaging_inbox'))
        }

        # send mail to hipchat
        template_context = Context({
            'request': self.request,
            'message': msg,
        })
        template = loader.get_template("messaging/fragments/hipchat_message.html")
        output = template.render(template_context)

        send_to_hipchat(
            output,
            room_id=settings.HIPCHAT_MAIL_ROOM,
            notify=1,
        )

        mixpanel_track(self.request, "Sent Message", {})
        mixpanel_engage(self.request, {'$add': {'Messages Sent': 1}})

        self._sendmail(template_name, msg.recipient.email, context)

    def seller_paypal_error(self, payment_attempt):
        """
        The payment attempt failed because the Seller has an invalid Paypal
        address

        :param payment_attempt: PaymentAttempt object
        """
        try:
            stall = payment_attempt.cart_stall.stall
            stall_url = reverse("my_stall", kwargs={"slug": stall.slug})
            settings_url = reverse("account_email_notifications")
            context = {
                'stall': {
                    'title': stall.title,
                    'url': absolute_uri(stall_url),
                },
                'PAYPAL_SETTINGS_URL': absolute_uri(settings_url)
            }
            to_email = stall.user.email

            self._sendmail("seller-erroneous-paypal-account",
                           to_email, context)
        except:
            LOG.error('seller_paypal_error failed', exc_info=True)

    def _order_item_context(self, item):
        """
        XXX: move somewhere else?
        """
        product = item.product
        return {
            'qty': item.quantity,
            'title': product.title,
            'price': str(item.price),
            'total': str(item.price * item.quantity),
            'id': product.id,
            'url': absolute_uri(product.get_absolute_url())
        }

    def _order_context(self, order):
        """
        XXX: move somewhere else?
        """
        items = [self._order_item_context(line_item)
                 for line_item in order.line_items.all()]                

        address = order.address

        delta = datetime.datetime.now().date() - order.created
        context = {
            'ORDER': {
                'items': items,
                'subtotal': str(order.subtotal()),
                'shipping': str(order.delivery_charge),
                'total': str(order.total()),
                'note': order.note,
                'address': {
                    'name': address.name,
                    'city': address.city,
                    'country': address.country.title,
                    'line1': address.line1,
                    'line2': address.line2,
                    'postal_code': address.postal_code,
                    'state': address.state,
                },
            },
            "FNAME": order.user.first_name,
            "ORDER_DATE": custom_strftime('{S} %B %Y', order.created),
            "CUSTOMER_FIRST_NAME": order.user.first_name,
            "CUSTOMER_FULL_NAME": order.user.get_profile().full_name,
            "CUSTOMER_USERNAME": order.user.username,
            "CUSTOMER_PROFILE_URL": absolute_uri(
                reverse("public_profile",
                        kwargs={"username": order.user.username})),
            "ORDER_ID": order.id,
            "INVOICE_URL": absolute_uri(reverse("invoice",
                                        kwargs={"order_id": order.id})),
            "STALL_TITLE": order.stall.title,
            "STALL_URL": absolute_uri(reverse("my_stall",
                                      kwargs={"slug": order.stall.slug})),
            "STALL_OWNER_USERNAME": order.stall.user.username,
            'STALL_OWNER_URL': order.stall.user.get_profile().get_absolute_url(),
            "NUMBER_OF_DAYS_SINCE_ORDER": delta.days,
            "MESSAGE_CUSTOMER_URL": absolute_uri(
                reverse("messaging_compose_to", kwargs={
                    "recipient": order.user.username,
            })),
            "MESSAGE_STALL_URL": absolute_uri(
                reverse("messaging_compose_to", kwargs={
                    "recipient": order.stall.user.username,
                })
            ),
            "UPDATE_PROFILE": absolute_uri(reverse("account_email_notifications")),
        }
        return context

    def _mixpanel_order_info(self, order):
        order_info = {
            "Order ID": order.id,
            "Order Date": order.created.isoformat(),
            "Total Order Value": str(order.total().amount),
            "Total Shipping Value": str(order.delivery_charge.amount),
            "No of Products": order.line_items.all().count(),
            "No of Items": order.num_items(),
            "Delivery Country": order.address.country.title
        }
        return order_info

    def order_reminder(self, order):
        """
        The seller needs to be reminded about an order.
        """
        days_map = {
            3: "3-day-dispatch-chase-up-stall-owner",
            7: "7-day-dispatch-chase-up-stall-owner",
            13: "13-day-dispatch-chase-up-stall-owner",
            14: "14-day-dispatch-chase-up-and-refund-warning",
        }
        days = (datetime.datetime.now().date() - order.created).days
        allowed_days = days_map.keys()
        if days not in allowed_days:
            return
        context = self._order_context(order)
        self._sendmail(days_map[days], order.stall.user.email, context)

    def order_refunded(self, order):
        """
        The seller has refunded an order
        """
        context = self._order_context(order)
        self._sendmail(
            'order-refunded-to-customer',
            order.user.email, context
        )

        self._sendmail(
            'order-refunded-to-stall-owner',
            order.stall.user.email,
            context
        )

        try:
            # Track the Seller refunding the Order
            order_info = self._mixpanel_order_info(order)
            mixpanel_track(self.request, "Clicked Refund Button", order_info)
            mixpanel_engage(self.request, {
                '$add': {
                    'Refunds Made': 1
                }
            })

            # Update the Buyers properties, reducing their GMV
            # XXX: we can't delete the transaction after it's refunded!!!
            #      adding the transaction needs to happen on Dispatch
            user = order.user
            stall = order.stall
            mixpanel_engage(None, {
                '$set': {
                    'Orders': user.orders.completed().count(),
                    'Total GMV to Date': str(user.get_profile().total_gmv.amount),
                },
                '$ignore_time': True
            }, distinct_id=user.id)
        except: 
            LOG.warning("Couldn't notify MixPanel of refund", exc_info=True)

    def order_dispatched(self, order):
        """
        The seller has marked an order as dispatched
        """
        try:
            context = self._order_context(order)
            self._sendmail(
                'order-dispatched-to-customer',
                order.user.email,
                context
            )
        except:
            LOG.warning("Couldn't send Order Dispatched email to Customer", exc_info=True)

        try:
            order_info = self._mixpanel_order_info(order)
            mixpanel_track(self.request, 'Clicked Mark Order as Dispatched', order_info)
            mixpanel_engage(self.request, {
                '$add': {
                    'Orders Dispatched': 1
                }
            }, distinct_id=order.stall.user.id)
        except:
            LOG.warning("Couldn't update MixPanel after Order Dispatch", exc_info=True)

    def order_placed(self, order):
        """
         1) Syncs cart with SailThru
         2) Sends 'Order Completed' e-mail to customer via Sailthru
         3) Syncs order information with MixPanel
        """
        # Technically the transaction isn't complete yet because the seller hasn't
        # marked the order as complete so could potentially refund the money.
        try:
            context = self._order_context(order)
            self._sendmail(
                'order-placed-to-customer',
                order.user.email,
                context
            )

            self._sendmail(
                'order-placed-to-stall-owner',
                order.stall.user.email,
                context
            )
        except:
            LOG.error("Events.order_placed failed to send email", exc_info=True)

        # Send completed order to SailThru, this updates the users 'Total Revenue'
        try:
            self.sailthru.order_purchased(order)
        except:
            LOG.error("Events.order_placed failed to sync order with SailThru", exc_info=True)

        # Sync user properties with MixPanel
        try:
            user = order.user
            mixpanel_engage(self.request, {
                '$set': {
                    'Orders': user.orders.completed().count(),
                    'Total GMV to Date': str(user.get_profile().total_gmv.amount),
                }
            }, distinct_id=user.id)
            mixpanel_engage(self.request, {
                '$append': {
                    '$transactions': {
                        '$time': order.created.isoformat(),
                        '$amount': str(order.total().amount),
                        'Order ID': order.id
                    }
                }
            }, distinct_id=user.id)
            if self.request is not None:
                order_info = self._mixpanel_order_info(order)
                mixpanel_track(self.request, "Purchased Order", order_info)
        except: 
            LOG.warning("Couldn't notify MixPanel of new order", exc_info=True)

    def forgot_password(self, user, token_generator=None):
        """
        Sends 'Forgot Username or Password?' with their username and a link
        to the password reset form.
        """
        from django.utils.http import int_to_base36
        if token_generator is None:
            from django.contrib.auth.tokens import default_token_generator      
            token_generator = default_token_generator
        token = token_generator.make_token(user)
        uid = int_to_base36(user.id)
        ctx = dict(
            PASSWORD_RESET_URL=absolute_uri(
                reverse("password_reset_confirm", kwargs={
                    "uidb36": uid,
                    "token": token
                })
            )
        )
        self._sendmail('forgot-username-or-password', user.email, ctx)

    def stall_opened(self, stall):
        """
        A new stall has been opened, welcome the user to the site and give them
        information about how to add products & optimize their stuff.
        """
        user = stall.user
        context = {
            "STALL_URL": absolute_uri(reverse("my_stall", kwargs={
                "slug": stall.slug,
            }))
        }
        self._sendmail("stall-owner-welcome", user.email, context)

    def user_signup(self, user, requires_activation=True):
        """
        Welcomes the user to the site
        Includes URL for them to activate their account / verify their e-mail.
        """
        if requires_activation:
            user_profile = user.user_profile
            verify_url = absolute_uri(reverse("verify", args=[user_profile.activation_key]))
            ctx = dict(ACTIVATION_URL=verify_url)
            self._sendmail('regular-user-welcome-email', user.email, ctx)

        profile = user.get_profile()

        # Fix up their MailingLists objects
        from mailing_lists.models import MailingListSignup
        mls = MailingListSignup.objects.create_from_user(user)
        mls.marketing_optin = profile.send_newsletters
        if self.request is not None:
            mls.set_ip_address(self.request)
        mls.save()

        # Apply defaults to EmailNotification preferences
        email_notification = user.email_notification
        email_notification.site_updates_features = profile.send_newsletters
        email_notification.stall_owner_tips = True
        email_notification.product_inspirations = profile.send_newsletters
        email_notification.blogs_you_might_like = profile.send_newsletters
        email_notification.save()

        # Integration with sailthru
        if self.sailthru.enabled():
            self.sailthru.signup(user=user)

    def newsletter_signup(self, email):
        """
        This is a newsletter signup that is available from the homepage modal,
        and at the bottom of the blog.
        """
        # Integration with sailthru
        # XXX: we should be doing the mailinglistsignup thing here too!!!
        if self.sailthru.enabled():
            self.sailthru.signup(email=email)

    def stall_stockcheck(self, stall):
        user = stall.user
        context = {
            "STALL_URL": absolute_uri(reverse("my_stall", kwargs={
                "slug": stall.slug,
            })),
            "DAYS_LEFT": stall.days_to_next_stockcheck
        }
        self._sendmail("stock-check-reminder-1", user.email, context)

    def stall_stockcheck_urgent(self, stall):
        user = stall.user
        context = {
            "STALL_URL": absolute_uri(reverse("my_stall", kwargs={
                "slug": stall.slug,
            })),
            "DAYS_LEFT": stall.days_to_next_stockcheck
        }
        self._sendmail("stock-check-reminder-2", user.email, context)

    def stall_suspended(self, stall):
        user = stall.user
        context = {
            "STALL_URL": absolute_uri(reverse("my_stall", kwargs={
                "slug": stall.slug,
            }))
        }
        self._sendmail("stock-check-suspension-notice", user.email, context)