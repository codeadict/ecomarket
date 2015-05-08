import json
import logging
from annoying.decorators import render_to, ajax_request
from django.core.mail import mail_admins
import purchase

from notifications import Events

from purchase.api import PayError

from actstream import action

from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import transaction
from django.http import HttpResponse, HttpResponseBadRequest, \
    HttpResponseForbidden, HttpResponseRedirect, \
    HttpResponseServerError
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.views.generic import View

from django.utils.decorators import method_decorator
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import redirect_to_login

from discounts.models import UTMCode
from marketplace.models import Product, Country
from mailing_lists.integrations.sailthru import Sailthru
from main.utils import absolute_uri
from main.utils import mixpanel_track

from purchase import api
from purchase import settings as purchase_settings
from purchase.forms import ShippingAddressForm
from purchase.models import (CartStall, Payment, Order, Cart,
                             PaymentAttempt, PaymentReturnRedirect)
from accounts.models import ShippingAddress
from purchase.signals import order_payed


logger = logging.getLogger(__name__)

client = api.Client(
    purchase_settings.PAYPAL_USERID,
    purchase_settings.PAYPAL_PASSWORD,
    purchase_settings.PAYPAL_SIGNATURE,
    purchase_settings.PAYPAL_APPLICATION_ID,
    sandbox=purchase_settings.PAYPAL_SANDBOX
)

UNVERIFIED_PAYPAL_EMAIL_ERROR = ("It seems that the seller does not have a "
                                 "correct verified PayPal account set up so we "
                                 "have stopped this order going through. We "
                                 "have notified the stall owner, and suggest "
                                 "that you also send them a message so that "
                                 "you can buy from them when they have updated "
                                 "their PayPal settings.")


class CartProductsView(View):

    def post(self, request, cart=None, product=None):
        if "product_id" not in request.REQUEST:
            return HttpResponseBadRequest()
        product = get_object_or_404(Product, id=request.REQUEST["product_id"])
        if "quantity" in request.REQUEST:
            try:
                quantity = int(request.REQUEST["quantity"])
            except ValueError:
                return HttpResponseBadRequest("quantity must be an integer")
            return self.update_cartstall(cart, product, quantity)
        return self.render_to_response(self.request, {"message": "OK"})

    def put(self, request, cart=None, product=None):
        try:
            data = json.loads(request.body)
        except ValueError:
            return HttpResponseBadRequest("Invalid JSON in request")
        if "quantity" in data:
            quantity = data["quantity"]
            return self.update_cartstall(cart, product, quantity)
        return self.render_to_response(self.request, {"message": "OK"})

    def delete(self, request, cart=None, product=None):
        cart = cart or request.user.cart
        cart.remove_product(product)
        Events(self.request).cart_updated(cart)
        return self.render_to_response(self.request, {"message": "OK"})

    def update_cartstall(self, cart, product, quantity):
        try:
            cart.set_quantity(product, quantity)
        except purchase.models.OutOfStockError:
            return HttpResponse(
                status=409,
                content=json.dumps({
                    "error_title": "not enough stock",
                    "error_message": "There is not enough stock to increase "
                    "the number of items",
                }),
                content_type="application/json"
            )
        Events(self.request).cart_updated(cart)
        if quantity < 0:
            quantity = 0
        if quantity == 0:
            return self.render_to_response(self.request, {
                "product_id": product.id,
                "quantity": 0,
                "num_items": float(cart.num_items()),
            })
        cart_stall = cart.cart_stalls.get(stall=product.stall)
        return self.render_to_response(self.request, {
            "product_id": product.id,
            "quantity": quantity,
            "total": float(cart_stall.total().amount),
            "subtotal": float(cart_stall.sub_total.amount),
            "discount": float(cart_stall.discount_amount().amount),
            "delivery": float(cart_stall.delivery_total().amount),
            "num_items": float(cart.num_items()),
        })

    def render_to_response(self, request, context):
        if request.is_ajax():
            return HttpResponse(json.dumps(context),
                                content_type="application/json")
        else:
            return HttpResponse("All OK")

    def dispatch(self, *args, **kwargs):
        cart = get_object_or_404(Cart, id=kwargs.pop("cart_id"))
        if cart.id != args[0].user.cart.id:  # cart.user != args[0].user:
            return HttpResponseForbidden("That isn't your cart")
        if "product_id" in kwargs:
            product = get_object_or_404(Product, id=kwargs.pop("product_id"))
        else:
            product = None
        return super(CartProductsView, self).dispatch(cart=cart, product=product, *args, **kwargs)


class CartStallView(View):

    def delete(self, request, cart_stall=None):
        cart_stall.delete()
        Events(request).cart_updated(cart_stall.cart)
        content = json.dumps(request.user.cart.to_json())
        return HttpResponse(content, content_type="application/json")

    def put(self, request, cart_stall=None):
        try:
            data = json.loads(request.body)
        except ValueError:
            return HttpResponseBadRequest("invalid json")
        if "country" in data:
            country_id = data["country"]["id"]
            if country_id is not None:
                country = get_object_or_404(Country, id=country_id)
            else:
                country = None
            # This should be done with an exception on the mode
            if country not in cart_stall.get_countries():
                return HttpResponse(
                    status=409,
                    content=json.dumps({
                        "error_title": "Unavailable Country",
                        "error_message": "These items cannot be shipped to that country"
                    }),
                    content_type="application/json"
                )
            cart_stall.speculative_country = country
        if "coupon" in data:
            cart_stall.coupon_code = data["coupon"]
        if "note" in data:
            cart_stall.note = data["note"]
        cart_stall.save()
        Events(request).cart_updated(cart_stall.cart)
        return HttpResponse(json.dumps(cart_stall.to_json()),
                            content_type="application/json")

    def dispatch(self, *args, **kwargs):
        cart_stall_id = kwargs.pop("cart_stall_id", None)
        if cart_stall_id:
            cart_stall = get_object_or_404(CartStall, id=cart_stall_id)
            request = args[0]
            # Anonymous users must have an anonymous cart
            if request.user.is_anonymous() and cart_stall.cart.id != request.user.cart.id:
                return HttpResponseForbidden()
            # Logged in users must have their own cart
            if request.user.is_authenticated() and request.user != cart_stall.cart.user:
                return HttpResponseForbidden()
        else:
            cart_stall = None
        return super(CartStallView, self).dispatch(cart_stall=cart_stall, *args, **kwargs)

    def get(self, request, cart_stall=None):
        if cart_stall:
            return HttpResponse(json.dumps(cart_stall.to_json()), content_type="application/json")
        else:
            content = [c.to_json() for c in request.user.cart.cart_stalls.all()]
            return HttpResponse(json.dumps(content), content_type="application/json")


def checkout_add(request, slug):
    """
    Adds product to cart.
    """
    product = get_object_or_404(Product, slug=slug)
    country = None
    if request.POST.get('shipping_country', None):
        try:
            country = Country.objects.get(code=request.POST.get('shipping_country', None))
        except:
            pass

    # When no cart is found, send them to login - where all users have carts
    if getattr(request.user, 'cart', None) is None:
        # This allows a streamlined log in process, the product_to_add_id
        # session variable is used by the register view to add a product
        # to the cart and redirect straight to the cart view.
        request.session["product_to_add_id"] = product.id
        login_url = reverse('login')
        return redirect_to_login(reverse('checkout_cart'),
                                 login_url=login_url)

    cart = request.user.cart
    try:
        # If the user is anonymous the cart won't exist in the DB yet
        # This avoids doing a DB insert for every request.
        if cart.id is None:
            cart.save()
        cart.add(product, country=country)
        mixpanel_track(request, 'Clicked Add to Cart', {
            'Product Title': product.title,
            'Product ID': product.id,
            'Number in stock': 'unlimited' if product.stock is None else product.stock,
            'Number of Images': product.images.all().count(),
            'Has Welcome Video': product.stall.has_welcome_video(),
            'Ships Worldwide': product.shipping_profile.ships_worldwide(),
            'Price': str(product.get_price_instance().amount)
        })
        Events(request).cart_updated(cart)
    except purchase.models.OutOfStockError:
        messages.error(request, "That product is out of stock")
    return HttpResponseRedirect(reverse('checkout_cart'))


def checkout_cart(request, template_name='purchase/checkout_cart.html'):
    """
    Show cart page
    """
    # If user doesn't have a cart - redirect to Login
    if getattr(request.user, 'cart', None) is None:
        login_url = reverse('login')
        return redirect_to_login(reverse('checkout_cart'),
                                 login_url=login_url)
    context = {}
    cart = request.user.cart
    if cart.id is None:
        # XXX: Anonymous User may end up here with an empty cart
        # But the cart JS code needs a cart.id to display product URLs.
        # It shouldn't be possible for the cart to have any products in it
        # unless it's saved, but the user has gone to their cart page - so lets
        # save just in case!
        cart.save()

    ecomm_prodid = []
    ecomm_quantity = []
    ecomm_totalvalue = 0
    for cart_stall in cart.cart_stalls.filter(checked_out=False):
        for product in cart_stall.cart_products.all():
            ecomm_prodid.append(product.id)
            ecomm_quantity.append(product.quantity)
        ecomm_totalvalue += cart_stall.total().amount

    if request.user.is_authenticated():
        try:
            utm_code = request.user.campaigns.all()[0].name
        except IndexError:
            utm_code = request.campaign.get("name")
    else:
        utm_code = None
    try:
        utm_code_obj = UTMCode.objects.get(code=utm_code)
    except UTMCode.DoesNotExist:
        curebit_site_id = settings.DEFAULT_CUREBIT_SITE_ID
    else:
        curebit_site_id = utm_code_obj.site.slug
    context.update({
        'cart': cart,
        'countries': [c.to_json() for c in Country.objects.all()],
        'ecomm_prodid': ecomm_prodid,
        'ecomm_quantity': ecomm_quantity,
        'ecomm_pagetype': 'basket',
        'ecomm_totalvalue': ecomm_totalvalue,
        'curebit_site_id': curebit_site_id,
        'base_url': request.build_absolute_uri("/"),
    })

    came_from_payment_return = request.GET.get('orderSuccess', None)
    if came_from_payment_return:
        context.update({'came_from_payment_return': True})
    else:
        context.update({'came_from_payment_return': False})

    request.clicktale.record = True
    return render(request, template_name, context)


@login_required
def checkout_shipping_stall(request, stall_id):
    cart_stall = get_object_or_404(CartStall, cart__user=request.user,
                                              stall_id=stall_id)
    return checkout_shipping(request, cart_stall)


@login_required
def checkout_shipping(request, cart_stall_id):
    """Asks the user to select a shipping address or create one"""
    if not isinstance(cart_stall_id, CartStall):
        cart_stall = get_object_or_404(CartStall, id=cart_stall_id)
    else:
        cart_stall = cart_stall_id
        cart_stall_id = cart_stall.id
    address_form = None
    address_with_error = None
    if request.method == "POST":
        address = None
        if "shipping_address_id" in request.POST:
            address_id = request.POST["shipping_address_id"]
            address = ShippingAddress.objects.get(id=address_id)
        else:
            # We have a new shipping address to validate and create
            share_orders = request.POST.get('check_order_in_activity_feed', False)
            request.session['check_orders_in_activity_feed'] = share_orders

            address_form = ShippingAddressForm(request.POST)
            if address_form.is_valid():
                address = address_form.save(commit=False)
                address.user = request.user
                address.save()
        if address:
            address.last_select_date_time = timezone.now()
            address.save()
            try:
                cart_stall.set_address(address)
                cart_stall.save()
                return redirect(reverse('checkout_pay_stall',
                                        kwargs={"cart_stall_id": cart_stall.id}))
            except purchase.models.MismatchingCountryError:
                print("Mismatching country")
                messages.error(
                    request,
                    'Oops. Your delivery prices have been worked out for %s '
                    'only so the address you have selected isn\'t suitable. '
                    'You can add/edit your addresses below or '
                    '<a href="%s" title="Back to your cart">go back to your cart</a> '
                    'to edit your delivery prices for the country you would like to deliver to.'
                    % (cart_stall.speculative_country.title, reverse('checkout_cart'))
                )
                address_with_error = address.id
                address_form = None  # We save this address as is, even though it can't be shipped.
            except purchase.models.UnavailableShippingCountryError:
                messages.error(request, "Sorry that country isn't available for delivery")
                address_with_error = address.id
                address_form = None  # We save this address as is, even though it can't be shipped.

    if address_form is None:
        address_form = ShippingAddressForm()

    share_orders = request.user.email_notification.share_orders_in_activity_feed
    request.session['check_orders_in_activity_feed'] = share_orders

    existing_addresses = request.user.addresses.all().order_by('-pk')
    context = {
        "cart_stall": cart_stall,
        "shipping_addresses": existing_addresses,
        "shipping_addresses_by_use": request.user.addresses.all().order_by('-last_select_date_time'),
        "address_form": address_form,
        'share_orders': request.session['check_orders_in_activity_feed'],
        "address_with_error": address_with_error,
    }
    mixpanel_track(request, 'Clicked Continue to Payment at Delivery', {})
    request.clicktale.record = True
    return render(request, "purchase/checkout_shipping.html", context)


def notify_directors_of_paypal_error(request, info):
    context = {
        'pe_error_id': info['pe'].error_id,
        'pe_error': repr(info['pe']),
        'payment_attempt_id': info['payment_attempt'].id,
        'payment_id': info['payment'].id,
        'purchaser_email': request.user.email,
        'purchaser_id': request.user.id,
        'seller_notified': "Yes" if info['seller_notified'] else "No",
        'stall_user_email': info['cart_stall'].stall.user.email,
        'stall_phone_landline': info['cart_stall'].stall.phone_landline,
        'stall_phone_mobile': info['cart_stall'].stall.phone_mobile,
        "FNAME": info['payment_attempt'].cart_stall.stall.user.first_name,
        "ORDER_DATE": info['payment_attempt'].created.strftime("%d-%m-%Y"),
        "STALL_TITLE": info['payment_attempt'].cart_stall.stall.title,
        "STALL_URL": absolute_uri(reverse("my_stall", kwargs={"slug": info['payment_attempt'].cart_stall.stall.slug})),
        "CUSTOMER_USERNAME": info['payment_attempt'].cart_stall.cart.user.username,
        "CUSTOMER_PROFILE_URL": absolute_uri(
            reverse("public_profile",
                    kwargs={"username": info['payment_attempt'].cart_stall.cart.user.username})),
    }
    to_email = 'director.alerts@ecomarket.com'
    Sailthru(request).send_template('directors-paypal-error', to_email, context)


@login_required
def checkout_pay_stall(request, cart_stall_id, template_name=None):
    """
    Generates Pay(PAY_PRIMARY) request, and redirects buyer to paypal.
    """
    # TODO Put this all in a model somewhere
    context = {}
    cart_stall = get_object_or_404(CartStall, id=cart_stall_id)
    payment = Payment.objects.create(
            purchaser=request.user,
            amount=cart_stall.total(),
            discount_amount=cart_stall.discount_amount(),
    )
    payment_attempt = PaymentAttempt.objects.create(payment=payment,
            cart_stall=cart_stall)
    try:
        success = payment.process(request)
    except PayError as pe:
        seller_notified = False
        # Either errors where seller account is not verified/confirmed OR 
        # seller needs to change settings to accept payment in another currency 
        # see http://bit.ly/183muku
        if pe.error_id in ['559044', '569042', '520009']:
            Events(request).seller_paypal_error(payment_attempt)
            error_message = UNVERIFIED_PAYPAL_EMAIL_ERROR
            seller_notified = True
        else:
            error_message = "There was an error communicating with PayPal"
        notify_directors_of_paypal_error(request, {
            'payment': payment,
            'payment_attempt': payment_attempt,
            'seller_notified': seller_notified,
            'pe': pe,
            'cart_stall': cart_stall
        })
        cart_url = reverse("checkout_cart")
        messages.error(request, error_message)
        return HttpResponseRedirect(cart_url)

    if success:
        return HttpResponseRedirect(payment.next_url())

    # Normally the user will never get here, on production nobody has ever
    # gotten here.... does it even work?
    context.update({
        'cart': cart_stall.cart,
        'cart_stall': cart_stall,
        'success': success,
    })
    request.clicktale.record = True
    return render(request, template_name, context)  # TODO: error template


@login_required
def checkout_review(request, order_id,
                    template_name='purchase/checkout_review.html'):
    """
    Review checkout of a stall payment. Also allow adding shipping info.

    TODO: Can we improve shipping address handling

    """
    context = {}
    order = get_object_or_404(Order, id=order_id)

    #is None if there is no address set yet, shoul never happen
    shipping_address = order.address

    if request.method == "POST":
        address_form = ShippingAddressForm(request.POST,
                                           instance=shipping_address)
        if address_form.is_valid():
            address_form.save()
            return HttpResponseRedirect(
                reverse('checkout_review',
                        kwargs={"order_id": order.id}))
    else:
        address_form = ShippingAddressForm()

    context.update({
        'cart': request.user.cart,
        'address_form': address_form,
        'order': order,
    })
    return render(request, template_name, context)


# Paypal Adaptive
# ================
@login_required
@transaction.autocommit
def payment_cancel(request, payment_id, payment_secret_uuid):
    """Incoming cancellation from paypal."""

    logger.debug("Cancellation received for Payment %s" % payment_id)
    payment = get_object_or_404(Payment, id=payment_id,
                                secret_uuid=payment_secret_uuid)

    if request.user != payment.purchaser:
        return HttpResponseForbidden("Unauthorized")

    payment.status = Payment.STATUS_CANCELED
    payment.save()
    messages.info(request, 'It looks like you cancelled the order at PayPal so '
                           'this order did not go through. Having trouble? '
                           '<a href="http://help.ecomarket.com/customer/portal/emails/new">Contact us for help</a>')

    return HttpResponseRedirect(reverse('checkout_cart'))


@login_required
@transaction.autocommit
def payment_return(request, payment_id, payment_secret_uuid):
    """
    Incoming return from paypal process (note this is a return to the site,
    not a returned payment)
    """

    logger.debug("Return received for Payment %s" % payment_id)
    payment = get_object_or_404(Payment, id=payment_id,
                                secret_uuid=payment_secret_uuid)

    # Go straight to cart page afterwards

    # Check that this order has not already been completed
    if payment.order is not None:
        # Payment has already been completed, just redirect to cart
        PaymentReturnRedirect.objects.create(
            user=payment.purchaser,
            payment_already_processed=True,
        ).save()
        success_url = "%s?orderSuccess=True&cid=%s" % (reverse("checkout_cart"), str(payment.order.id))
        response = HttpResponseRedirect(success_url)
        #logger.debug("Payment %s already complete" % payment_id)
        return response

    if request.user != payment.purchaser:
        return HttpResponseForbidden("Unauthorized")

    PaymentReturnRedirect.objects.create(
        user=payment.purchaser,
        payment_already_processed=False,
    ).save()

    success_url = reverse("payment_pending", kwargs={'payment_id': payment_id})
    return HttpResponseRedirect(success_url)


@login_required
@transaction.commit_on_success
def payment_tracking_complete(request, payment_id):
    # Payment must already be completed by current user
    payment = get_object_or_404(Payment, id=payment_id)
    if payment.order is None or request.user != payment.purchaser:
        return HttpResponseForbidden("Unauthorized")

    payment.logged_to_google = True
    payment.save()
    return HttpResponse(json.dumps({'tracked': True}), mimetype="application/json")


class RefundView(View):

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(RefundView, self).dispatch(*args, **kwargs)

    def post(self, request, order_id=None, *args, **kwargs):
        data = request.REQUEST
        order = get_object_or_404(Order, id=order_id)
        if request.user != order.stall.user:
            return HttpResponseForbidden("That order does not belong to you")

        if "reason" not in data:
            return HttpResponseBadRequest("You must specify a reason")

        if "entire_order" in data:
            order.refund(data["reason"])
            order.save()
        else:
            if "line_items" not in data:
                return HttpResponseBadRequest("You must specify line items"
                                              "as a list of ids or set entire "
                                              "order to True")
            ids = data["line_items"]
            line_items = order.line_items.filter(id__in=ids)
            order.refund(data["reason"], line_items=line_items)
            order.save()
        Events(request).order_refunded(order)

        redirect_url = reverse("invoice",
                               kwargs={"order_id": order.id})
        messages.success(request,
                         "Thanks. We have refunded your item as requested and "
                         "the customer will get an email notifying them of "
                         "this. Please do remember that sellers must not have "
                         "products published on Eco Market that are out of "
                         "stock. Refunding products a lot will eventually "
                         "negatively impact your ranking on our site so "
                         "please try to avoid doing this too often (and only "
                         "in cases where the customer needs to send the item "
                         "back for " "some reason)."
                         )
        return HttpResponseRedirect(redirect_url)


@csrf_exempt
@require_POST
def ipn_handler(request, payment_id, payment_secret_uuid):
    # have to grab this here because accessing the body property
    # after the POST variable is not allowed. But we need the raw
    # request for validting the IPN
    body = request.body
    logger.debug("raw post is: {0}".format(body))
    logger.debug("IPN handler called, request data is "
                 "{0}".format(request.POST))
    if not client.validate_ipn(body):
        logger.debug("Message could not be validated")
        return HttpResponseBadRequest("Unable to validate ipn data")
    logger.debug("ipn data validated")
    parsed_data = client.parse_ipn(request.POST)
    logger.debug("IPN parsed")
    logger.debug("parsed_data is {0}".format(parsed_data))

    payment = get_object_or_404(Payment, id=payment_id,
                                secret_uuid=payment_secret_uuid)

    if parsed_data.get("reason_code", "not found").lower() == "refund":
        logger.debug("Refunding")
        try:
            if payment.order is not None and not payment.order.is_refunded():
                payment.order.refund("refunded from outside of ecomarket",
                                     send_to_paypal=False)
        except Order.DoesNotExist:
            pass

    elif parsed_data.get("action_type", None).upper() == "PAY_PRIMARY":
        if parsed_data["status"] == "INCOMPLETE":
            logger.debug("Marking payment as PRIMARY_PAID")

            payment.payment_attempt.complete()
            payment = Payment.objects.get(id=payment.id)

            order = payment.order
            for line_item in order.line_items.all():
                # Update number_of_sales
                line_item.product.number_of_sales += line_item.quantity
                line_item.product.save()

                share_orders = order.user.email_notification.share_orders_in_activity_feed

                if share_orders:
                    action.send(
                        order.user,
                        verb='purchased product at',
                        action_object=line_item.product, target=order
                    )

            Events(request).order_placed(order)
            order_payed.send(sender=order, order=order, request=request)

            payment.status = Payment.STATUS_PRIMARY_PAID
            payment.save()
        elif parsed_data["status"] == "COMPLETED":

            logger.debug("marking payment as complete")
            payment.status = Payment.STATUS_COMPLETED
            payment.save()

    return HttpResponse("All ok")


@login_required
@require_POST
def mark_dispatched(request, order_id=None):
    order = get_object_or_404(Order, id=order_id)
    if "redirect_url" in request.REQUEST:
        redirect_url = request.REQUEST["redirect_url"]
    else:
        redirect_url = reverse("sold_awaiting_shipping")
    if order.stall.user != request.user:
        return HttpResponseForbidden("You cannot mark this order dispatched")
    order.mark_dispatched()
    Events(request).order_dispatched(order)
    return HttpResponseRedirect(redirect_url)


@render_to("purchase/payment_pending.html")
def payment_pending(request, payment_id):
    """
    This view is called when a user comes from PayPal and the IPN has not been processed, yet.

    :param request:
    :param payment_id:
    :return:
    """
    return {
        'payment_id': payment_id,
    }


@login_required
@ajax_request
def check_payment_status(request, payment_id):
    """
    Checks if a payment has been successfully processed.

    :param request:
    :param payment_id:
    :return:
    """
    payment = get_object_or_404(
        Payment,
        id=payment_id,
    )
    if payment.order:
        success_url = "%s?orderSuccess=True&cid=%s" % (reverse("checkout_cart"), str(payment.order.id))
        status = True
    else:
        success_url = None
        status = False
    return {
        'success_url': success_url,
        'status': status,
    }


@login_required
@ajax_request
def payment_check_timeout(request, payment_id):
    """
    When the pending payment window exeeded the wait limit
    we will send out an email.

    :param request:
    :param payment_id:
    :return:
    """

    mail_admins(
        'Received IPN timeout',
        'A user had an IPN timeout. Payment id: %s' % payment_id,
        True,
    )

    return {
        'result': True,
    }


@login_required
@ajax_request
def store_phone_number(request):
    phone_number = request.POST.get('phone_number', None)

    user_profile = request.user.user_profile
    user_profile.phone_number = str(phone_number)
    user_profile.save()

    return {
        'result': True,
    }