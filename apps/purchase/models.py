"""Models used to maintain shopping cart, payment data."""

from datetime import datetime
import logging

from django.core.urlresolvers import reverse
from django.core.exceptions import MultipleObjectsReturned
from django.db import models, transaction
from django.db.models.signals import post_save
from django.dispatch import receiver

from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from django_extensions.db.fields import UUIDField
import money
from money.Money import Money

from marketplace.fields import NullableMoneyField as MoneyField
from discounts.models import Discount

import purchase.api
from purchase import settings as purchase_settings
from purchase import managers
from purchase.managers import CartStallManager
from purchase.settings import DEFAULT_CURRENCY

logger = logging.getLogger(__name__)

# This might be dodgy from a threading point of view,
client = purchase.api.Client(
    purchase_settings.PAYPAL_USERID,
    purchase_settings.PAYPAL_PASSWORD,
    purchase_settings.PAYPAL_SIGNATURE,
    purchase_settings.PAYPAL_APPLICATION_ID,
    sandbox=purchase_settings.PAYPAL_SANDBOX
)


@receiver(post_save, sender=User, dispatch_uid="dontbesillydjango")
def user_cart_creation(sender, created=False, instance=None, raw=False,
                       **kwargs):
    if created and not raw:
        Cart.objects.create(user=instance)


class OutOfStockError(Exception):
    pass


class UnavailableShippingCountryError(Exception):
    pass


class MismatchingCountryError(Exception):
    pass


class Cart(models.Model):
    """
    Maintains users shopping cart.

    The DB schema of how a shopping cart is structured is as follows:

    Cart
        CartStall Instance
            CartProduct Instance
        CartStall Instance
            CartProduct Instance
            CartProduct Instance

    Each cart has one or more CartStall(per stall and stores notes for that
    stall) and each CartStall has one or more CartProduct(per product +
    quantity etc.)

    """
    user = models.OneToOneField(User, related_name='cart', null=True)
    created = models.DateField(auto_now_add=True, editable=False)
    updated = models.DateField(auto_now=True, editable=False)

    class Meta:
        ordering = ('-created',)

    def __unicode__(self):
        if self.user is None:
            return "Anonymous User:{0}".format(self.created)
        return u"{0}:{1}".format(self.user.username, self.created)

    def move_contents_to(self, other_cart):
        """
        Move the contents of this cart with another cart

        Nothing will be removed from the other cart, the product quantity will
        be increased to match the quantity from this cart etc.
        """
        assert other_cart is not None
        for cart_stall in self.cart_stalls.filter(checked_out=False):
            if cart_stall.checked_out:
                continue
            other_stall_qs = other_cart.cart_stalls.filter(
                    stall=cart_stall.stall, checked_out=False)
            if other_stall_qs.count():
                # Other cart contains products for this stall that haven't been
                # checked out yet.
                other_stall = other_stall_qs[0]
                for cart_product in cart_stall.cart_products.all():
                    other_product_qs = other_stall.cart_products.filter(
                            product=cart_product.product)
                    # If the product doesn't exist in the cart we're migrating
                    # to then just change the cart_stall it belongs to
                    if other_product_qs.count() == 0:
                        cart_product.cart_stall = other_stall
                        cart_product.save()
                cart_stall.delete()
            else:
                # As simple as changing the 'cart' the cart_stall belongs to :)
                cart_stall.cart = other_cart
                cart_stall.save()

    def remove_product(self, product):
        try:
            cart_stall = CartStall.objects.get(cart=self,
                                               stall=product.stall)
            cart_product = CartProduct.objects.filter(cart_stall=cart_stall,
                                                      product=product)
            cart_product.delete()
        except:
            return False
        return True

    def set_quantity(self, product, quantity, increment=False, country=None):
        """Sets the quantity of product in the cart to quantity.
        If the increment argument is True then adds the quantity to the current
        quantity, otherwise resets quantity.
        """
        if quantity < 0:
            quantity = 0
        stall = product.stall
        if country:
            cart_stall, created = CartStall.objects.get_or_create(
                cart=self,
                stall=stall,
                speculative_country=country
            )
        else:
            cart_stall, created = CartStall.objects.get_or_create(
                cart=self,
                stall=stall
            )

        while True:
            # XXX: hacky - to get around a bug where there could be multiple
            #      duplicate cart_product entries. This was probably due to
            #      buggy cart migration code for anonymous users, but we don't
            #      want to leave people with broken carts :(
            try:
                cart_product, created = CartProduct.objects.get_or_create(
                    cart_stall=cart_stall,
                    product=product,
                    defaults={
                        "quantity": 0,
                        "unit_price": product.get_price_instance().amount,
                    },
                )
                break
            except MultipleObjectsReturned:
                # Delete all but the last one
                cart_products = CartProduct.objects.filter(
                        cart_stall=cart_stall, product=product)
                num_cart_products = len(cart_products)
                i = 0
                for cart_product in cart_products:
                    i += 1
                    if i == num_cart_products:
                        break
                    cart_product.delete()
                continue

        if increment:
            new_quantity = cart_product.quantity + quantity
        else:
            new_quantity = quantity
        if product.stock is not None and new_quantity > product.stock:
            raise purchase.models.OutOfStockError
        cart_product.quantity = new_quantity
        cart_product.unit_price = product.get_price_instance().amount
        cart_product.save()

    def add(self, product, quantity=1, country=None):
        if country:
            self.set_quantity(product, 1, increment=True, country=country)
        else:
            self.set_quantity(product, 1, increment=True)

    def remove(self, product, quantity=1, remove_all=False):
        """
        Removes product from cart.

        Argument:
        ``remove_all`` : If True, then deletes all the cart products. If False,
                        then reduces the quantity by the amount specified.
        ``quantity`` : reduce the quantity by this amount. If it equals
                        zero or less, then delete the whole product along
                        with stall.
        """
        stall = product.stall
        try:
            cart_stall = CartStall.objects.get(
                cart=self,
                stall=stall,
            )
            logger.debug("Stall(id={0}) to already found in the cart.".format(
                stall.id))
        except CartStall.DoesNotExist:
            logger.debug(("Stall(id={0}) to add not found in the cart. Thus,"
                          "product doesn't exist as well.").format(stall.id))
            return

        try:
            cart_product = CartProduct.objects.get(
                cart_stall=cart_stall,
                product=product,
            )
        except CartProduct.DoesNotExist:
            # Item Doesn't exist. Do nothing.
            return

        if remove_all is True:
            cart_product.delete()
            # Delete stall from cart too, if has no items
            if cart_stall.cart_products.all().count() == 0:
                cart_stall.delete()

        else:
            cart_product.quantity -= quantity
            if cart_product.quantity <= 0:
                cart_product.delete()
                # Delete stall from cart too, if has no items
                if cart_stall.cart_products.all().count() == 0:
                    cart_stall.delete()
            else:
                cart_product.save()

    def remove_stall(self, stall):
        """Removes the stall specified by deleting all products of that stall
        from the cart."""

        self.cart_stalls.filter(stall=stall).delete()

    def add_note(self, stall, note):
        """Adds note corresponding to the given stall in the cart."""
        self.cart_stalls.filter(stall=stall).update(note=note)

    def checkout_cart_stall(self, cart_stall):
        """
        Update stall and mark as checked out with a timestamp.

        Means a stall is paid for.
        # TODO: if all stores checked out, then delete from session?, mark
          whole cart as checked_out
        # Update Cart session
        """
        self.cart_stalls.filter(id=cart_stall.id).update(
            checked_out=True,
            checked_out_on=datetime.now()
        )

    def get_quantity(self, product):
        """Convenience method, gets the quantity of an item in the cart """
        try:
            cart_product = CartProduct.objects.get(cart_stall__cart=self,
                                                   product=product)
        except CartProduct.DoesNotExist:
            return 0
        return cart_product.quantity

    def clear(self):
        self.cart_stalls.all().delete()

    def num_items(self):
        return CartProduct.objects.filter(cart_stall__cart=self).count()

    def to_json(self):
        result = {}
        result["cart_stalls"] = [cs.to_json() for cs in self.cart_stalls.all()]
        result["num_items"] = self.num_items()
        return result


class CouponAlreadyInCart(Exception):
    pass


class CouponAlreadyUsed(Exception):
    pass


class CouponExeption(Exception):
    pass


def _get_discount(cart, coupon_code):
    discount = Discount.objects.active().get(code__iexact=coupon_code)

    # It's a real coupon, but don't let it be used twice
    cart_stalls_with_coupon = cart.cart_stalls.filter(
            coupon_code__iexact=coupon_code)
    if cart_stalls_with_coupon.count() > 1:
        raise CouponAlreadyInCart(coupon_code)
    if (cart.user is not None and cart.user.is_authenticated()
            and discount in cart.user.get_profile().used_discounts.all()):
        raise CouponAlreadyUsed(coupon_code)
    return discount


def _coupon_details(cart_stall):
    cart = cart_stall.cart
    coupon_code = cart_stall.coupon_code

    try:
        if cart_stall.has_free_shipping and cart_stall.coupon_code:
            raise CouponExeption("Sorry you can't add a coupon to this product because "
                                 "it's already under a free delivery discount.")

        _get_discount(cart, coupon_code)
    except Discount.DoesNotExist:
        msg = "Sorry, '{}' isn't an active discount coupon".format(
            coupon_code)
        msg_type = "error"
    except CouponAlreadyInCart:
        msg = ("This discount coupon is already active in your cart! Sorry, "
               "this coupon can only be used once on one stall.")
        msg_type = "error"
    except CouponAlreadyUsed:
        msg = "Sorry, you've already used this discount coupon"
        msg_type = "error"
    except CouponExeption as e:
        msg = e.message
        msg_type = "error"
    else:
        msg = "Nice, we've discounted this order"
        msg_type = "info"
    return {
        "coupon": coupon_code,
        "coupon_message": msg,
        "coupon_message_type": msg_type,
        }


class CartStall(models.Model):
    """
    Stores the stalls that get added via products to a cart.
    This makes it easier to store stall related info like notes etc.

    Also since our rendering relies on grouping by stall, this helps logically
    structure helpers.
    """
    cart = models.ForeignKey('purchase.Cart', related_name='cart_stalls')
    stall = models.ForeignKey('marketplace.Stall', verbose_name=_('stall'))
    note = models.TextField(default='', blank=True, null=False)
    checked_out = models.BooleanField(default=False,
                                      verbose_name=_('checked out'))
    checked_out_on = models.DateField(blank=True, null=True, editable=False)
    address = models.ForeignKey("accounts.ShippingAddress", null=True,
                                related_name='cart_stalls')
    speculative_country = models.ForeignKey('marketplace.Country', null=True)

    # Do not store a ForeignKey here, as we must allow bad codes
    coupon_code = models.CharField(max_length=100, blank=True, null=True)

    objects = CartStallManager()

    def __init__(self, *args, **kwargs):
        self.shipping_discount = Money("0", DEFAULT_CURRENCY)
        super(CartStall, self).__init__(*args, **kwargs)

    def __unicode__(self):
        return u"{0}:{1}".format(self.cart, self.stall.title)

    @property
    def estimated_delivery(self):
        """Returns a dict of min, max values in number of days for delivery

        TODO: Calculate min,max of all products in the cart.
        """
        return {'min': 2, 'max': 9}

    @property
    def has_free_shipping(self):
        if self.shipping_discount.amount > 0:
            return True
        else:
            return False

    def delivery_total(self):
        """Returns the delivery charges for this stall, considering all
        products in the cart.
        """
        if self.address:
            country = self.address.country
        else:
            country = self.get_country()

        # This is a little complex so some explanation is in order.
        #
        # We loop through all the products, for each product if there is a
        # rule which matches the selected country we add the price of the
        # _extra_ items to the total. We also keep track of the largest
        # initial price. After we have been through all the products we
        # add the price of the largest initial item and subtract the extra
        # price of the largest initial item rule because otherwise it will
        # be charged twice, once for the initial and once for the already
        # counted extra.

        # This is the rule with the largest initial item price. We need to
        # store it to add to the total later. We also need the extra price
        # because we need to subtract that from the title.
        #
        # Ideally this would be a single variable rule object, unfortunately
        # the shipping rule for the rest of the world is represented as fields
        # on the shipping profile rather than a rule so we need both fields
        # here.
        largest_initial = None
        largest_initial_extra = None
        largest_shipping_discount = None
        largest_shipping_discout_extra = None
        total_shipping_price = money.Money(0, DEFAULT_CURRENCY)
        total_shipping_discount = Money(0, DEFAULT_CURRENCY)

        for cart_product in self.cart_products.all().prefetch_related(
                'product__shipping_profile__shipping_rules__countries'
        ):
            product = cart_product.product

            #Find the a shipping rule for the selected country
            shipping_price, shipping_price_extra = product.get_shipping_prices(self.speculative_country)

            shipping_discount, shipping_discout_extra = product.get_shipping_discounts(self.speculative_country)

            if largest_initial is None or shipping_price > largest_initial:
                largest_initial = shipping_price
                largest_shipping_discount = shipping_discount
                largest_initial_extra = shipping_price_extra
                largest_shipping_discout_extra = shipping_discout_extra

            total_shipping_price += shipping_price_extra * cart_product.quantity
            total_shipping_discount += shipping_discout_extra * cart_product.quantity

        if largest_initial is not None:
            total_shipping_price += largest_initial

        if largest_initial_extra is not None:
            total_shipping_price -= largest_initial_extra

        if largest_shipping_discount is not None:
            total_shipping_discount += largest_shipping_discount

        if largest_shipping_discout_extra is not None:
            total_shipping_discount -= largest_shipping_discout_extra

        self.shipping_discount = total_shipping_discount

        return total_shipping_price

    def discount_amount(self):
        """
        Calculates a discount for a product.

        The two reasons for a discount are:

        - The customer added a coupon code
        - There is free shipping for a product

        @return: Money object representing the discount
        """
        if self.shipping_discount.amount > 0:
            return self.shipping_discount
        elif self.coupon_code:
            try:
                discount = _get_discount(self.cart, self.coupon_code)
            except (Discount.DoesNotExist, CouponAlreadyInCart,
                    CouponAlreadyUsed):
                # Zero discount
                discount = Discount()
        else:
            discount = Discount()
        return Money(discount.calculate(self.pre_discount_total()),
                     DEFAULT_CURRENCY)

    @property
    def sub_total(self):
        """Returns the total price of all products in the cart for a stall.

        TODO: add delivery.

        """
        amount = Money("0", DEFAULT_CURRENCY)
        for cart_product in self.cart_products.all():
            amount += cart_product.total
        return amount

    def pre_discount_total(self):
        """
        Returns total including price of products and delivery charges.
        """
        return self.sub_total + self.delivery_total()

    def total(self):
        return self.pre_discount_total() - self.discount_amount()

    def create_order(self):
        order = Order(stall=self.stall, user=self.cart.user,
                      address=self.address)

        if self.has_free_shipping:
            order.delivery_charge = money.Money(0, DEFAULT_CURRENCY)
        else:
            order.delivery_charge = self.delivery_total()

        order.discount_amount = self.discount_amount()
        order.note = self.note
        order.save()
        if order.discount_amount > 0 and not self.shipping_discount.amount > 0:
            profile = self.cart.user.get_profile()
            discount = Discount.objects.active().get(
                code__iexact=self.coupon_code
            )
            profile.used_discounts.add(discount)
            profile.save()
        for cart_product in self.cart_products.all():
            price = cart_product.product.get_price_instance().amount
            order.line_items.create(product=cart_product.product,
                                    quantity=cart_product.quantity,
                                    price=price)
        return order

    def checkout(self):
        """Creates a new order, then deletes the cart stall"""
        self.create_order()
        self.delete()

    def to_json(self):
        result = {
            "subtotal": float(self.sub_total.amount),
            "delivery": float(self.delivery_total().amount),
            "discount": float(self.discount_amount().amount),
            "total": float(self.total().amount),
            "cart_products": [],
            "id": self.id,
            "note": self.note,
            "title": self.stall.title,
            "stall_url": self.stall.get_absolute_url(),
        }
        if self.coupon_code:
            result.update(_coupon_details(self))
        if self.speculative_country:
            result["speculative_country"] = self.speculative_country.id
        for cart_product in self.cart_products.all():
            result["cart_products"].append(cart_product.to_json())
        result["countries"] = [c.to_json() for c in self.get_countries()]
        result["country"] = self.get_country().to_json()
        result["checkout_url"] = reverse("checkout_pay_stall",
                                         kwargs={"cart_stall_id": self.id})
        result["shipping_url"] = reverse("checkout_shipping_stall",
                                         kwargs={"stall_id": self.stall_id})
        return result

    def get_countries(self):
        # This is naive and possibly going to be very slow.
        from marketplace.models import Country

        all_countries = set(Country.objects.all())
        products = [cp.product for cp in self.cart_products.all()]
        for product in products:
            if product.shipping_profile.others_price is not None:
                # This indicates that this profile ships to anywhere
                # the world
                continue
            countries = set([])
            for rule in product.shipping_profile.shipping_rules.all():
                for country in rule.countries.all():
                    countries.add(country)
            all_countries = countries.intersection(all_countries)
        return list(all_countries)

    def get_country(self):
        from marketplace.models import Country

        if self.speculative_country:
            return self.speculative_country
        uk = Country.objects.get(code="GB")
        if uk in self.get_countries():
            return uk
        return self.get_countries()[0]

    def set_address(self, address):
        if self.speculative_country and (
                self.speculative_country != address.country):
            raise purchase.models.MismatchingCountryError()
        if address.country not in self.get_countries():
            raise purchase.models.UnavailableShippingCountryError()
        self.address = address

    def is_valid_shipping_country(self, country):
        return country in self.get_countries()


class CartProduct(models.Model):
    """
    Stores the products in a cart.

    """
    cart_stall = models.ForeignKey(CartStall, verbose_name=_('cart stall'),
                                   related_name='cart_products')
    product = models.ForeignKey('marketplace.Product',
                                verbose_name=_('product'))
    quantity = models.PositiveIntegerField(verbose_name=_('quantity'))
    unit_price = MoneyField(_(u'amount'), max_digits=6, decimal_places=2,
                            default_currency="GBP")
    #created?

    class Meta:
        ordering = ('cart_stall',)

    def __unicode__(self):
        return u"{0}:{1}".format(self.product.title, self.quantity)

    @property
    def total(self):
        return self.quantity * self.unit_price

    @property
    def delivery(self):
        """
        TODO: Pull from db.
        """
        return Money("0", DEFAULT_CURRENCY)

    def to_json(self):
        result = {
            "id": self.id,
            "quantity": self.quantity,
            "product": {
                "id": self.product.id,
                "title": self.product.title,
                "description": self.product.description,
                "absolute_url": self.product.get_absolute_url(),
                "image_url": self.product.image.url_80,
                "price": float(self.product.get_price_instance().amount),
            }
        }
        return result


class PaymentAttempt(models.Model):
    """Created as part of the payment process by the cart stall"""
    cart_stall = models.ForeignKey(CartStall, related_name='payment_attempts',
                                   null=True, on_delete=models.SET_NULL)
    payment = models.OneToOneField('purchase.Payment',
                                   related_name='payment_attempt')
    created = models.DateField(auto_now_add=True, editable=False)
    updated = models.DateField(auto_now=True, editable=False)

    def complete(self):
        order = self.cart_stall.create_order()
        order.save()
        self.payment.order = order
        self.payment.save()
        self.cart_stall.delete()


class Order(models.Model):
    """An Order is related to a CartStall, not a Cart"""
    refund_reasons = (
        (0, 'Products in the order were not in stock'),
        (1, 'Products in the order were damaged/faulty'),
        (2, 'Products in the order went missing in the post'),
        (3, 'My business has closed'),
        (4, 'I no longer wish to sell items on Eco Market'),
        (5, 'I aggreed a refund with the customer for another reason'),
    )

    objects = managers.OrderManager()

    user = models.ForeignKey(User, related_name='orders')
    address = models.ForeignKey("accounts.ShippingAddress")
    stall = models.ForeignKey("marketplace.Stall", related_name='orders')
    created = models.DateField(auto_now_add=True, editable=False)
    updated = models.DateField(auto_now=True, editable=False)
    delivery_charge = MoneyField(max_digits=6, decimal_places=2,
                                 default_currency="GBP")
    discount_amount = MoneyField(max_digits=6, decimal_places=2,
                                 default_currency="GBP", default=0)
    note = models.TextField(default='', blank=True, null=False)

    # True if this is an order imported from the old ethicalcommunity website
    is_joomla_order = models.BooleanField(default=False)
    refund_reason = models.IntegerField(max_length=10, choices=refund_reasons, blank=True, null=True)

    def subtotal(self):
        return sum([line_item.total() for line_item in self.line_items.all()])

    def pre_discount_total(self):
        return self.subtotal() + self.delivery_charge

    def total(self):
        return self.pre_discount_total() - self.discount_amount

    def refund(self, reason, line_items=None, send_to_paypal=True,
               automated=False):
        """Refunds line items for this order, if no
        line_items are specified refunds the whole order. Notifies the user
        via email

        :param send_to_paypal: if false this will generate notifications to the
        user and update the DB but won't send a refund message to paypal.
        Useful for refunds created outside of ecomarket.

        :param automated: Whether the refund was refunded by the payments cron
        or by user action.
        """
        if not line_items:
            line_items = self.line_items.all()
            entire_order = True
        else:
            entire_order = False

        allowed_ids = [l.id for l in self.line_items.all()]

        self.refund_reason = int(reason)

        refund = Refund(order=self, reason=reason)
        refund.save()
        for line_item in line_items:
            if line_item.id not in allowed_ids:
                refund.delete()
                raise RuntimeError("Attempted refund of line_item id:{0} "
                                   "in order id:{1}".format(line_item.id,
                                                            self.id))
            line_item.refund = refund
            line_item.save()

        if not send_to_paypal:
            if entire_order:
                purchase.models.client.refund(self.payment.pay_key)
            else:
                amount = sum([l.price for l in line_items])
                purchase.models.client.refund(
                        self.payment.pay_key, amount=amount.amount,
                        receiver_email=self.stall.paypal_email)

        self.payment.status = Payment.STATUS_REFUNDED
        self.payment.save()

    def mark_dispatched(self):
        refunded_line_items = self.line_items.filter(refund__isnull=False)
        for line_item in self.line_items.all():
            if line_item not in refunded_line_items:
                line_item.dispatched = True
                line_item.save()

    def is_dispatched(self):
        ref_or_dispatched = self.line_items.filter(
            dispatched=True
        ) | self.line_items.filter(
            refund__isnull=False,
            dispatched=False
        ).all()
        return len(ref_or_dispatched) == len(self.line_items.all())

    def is_refunded(self):
        return len(self.line_items.filter(refund__isnull=False).all()) > 0

    def estimated_delivery(self):
        return {
            "min": 2,
            "max": 5,
        }

    def is_refundable(self):
        return not (self.is_refunded() or self.is_joomla_order)

    def is_dispatchable(self):
        return not (self.is_dispatched() or self.is_joomla_order)

    def num_items(self):
        total = 0
        for line_item in self.line_items.all():
            total += line_item.quantity
        return total


class OrderFeedback(models.Model):
    order = models.OneToOneField(Order, related_name='feedback', null=True)
    feedback_text = models.TextField(blank=False)
    created = models.DateField(auto_now_add=True, editable=False)
    updated = models.DateField(auto_now=True, editable=False)


class LineItem(models.Model):
    order = models.ForeignKey(Order, related_name='line_items')
    price = MoneyField(max_digits=6, decimal_places=2, default_currency="GBP")
    quantity = models.PositiveIntegerField()
    product = models.ForeignKey("marketplace.Product")
    dispatched = models.BooleanField(default=False)
    refund = models.ForeignKey('purchase.Refund', related_name='line_items',
                               null=True)

    created = models.DateField(auto_now_add=True, editable=False)
    updated = models.DateField(auto_now=True, editable=False)

    def total(self):
        return self.price * self.quantity


class Refund(models.Model):
    order = models.ForeignKey(Order, related_name='refunds')
    reason = models.CharField(max_length=200)
    created = models.DateField(auto_now_add=True, editable=False)
    updated = models.DateField(auto_now=True, editable=False)


# Payments
# --------
# Models to support Paypal Adaptive API."""
class PaypalAdaptive(models.Model):
    """Base fields used by all PaypalAdaptive models."""

    order = models.OneToOneField(Order, related_name="payment", null=True)
    amount = MoneyField(_(u'amount'), max_digits=6, decimal_places=2,
                        default_currency="GBP")
    discount_amount = MoneyField(max_digits=6, decimal_places=2,
                                 default_currency="GBP", default=0)
    created = models.DateTimeField(_(u'created on'), auto_now_add=True)
    secret_uuid = UUIDField(_(u'secret UUID'))  # to verify return_url
    debug_request = models.TextField(_(u'raw request'), blank=True, null=True)
    debug_response = models.TextField(_(u'raw response'), blank=True,
                                      null=True)

    class Meta:
        abstract = True


class Payment(PaypalAdaptive):
    """Models a payment made using Paypal. """

    STATUS_NEW = 'new'
    STATUS_CREATED = 'created'
    STATUS_PRIMARY_PAID = 'primary_paid'
    STATUS_ERROR = 'error'
    STATUS_CANCELED = 'cancelled'
    STATUS_COMPLETED = 'completed'
    STATUS_REFUNDED = 'refunded'

    STATUS_CHOICES = (
        (STATUS_NEW, _('new')),
        (STATUS_CREATED, _(u'Created')),
        (STATUS_PRIMARY_PAID, _(u'primary_paid')),
        (STATUS_ERROR, _(u'Error')),
        (STATUS_CANCELED, _(u'Canceled')),
        (STATUS_COMPLETED, _(u'Completed')),
        (STATUS_REFUNDED, _(u'Refunded')),
    )

    purchaser = models.ForeignKey(User, related_name='payments_made')
    pay_key = models.CharField(_(u'paykey'), max_length=255)
    transaction_id = models.CharField(_(u'paypal transaction ID'),
                                      max_length=128, blank=True, null=True)
    status = models.CharField(_(u'status'), max_length=200,
                              choices=STATUS_CHOICES, default=STATUS_NEW)
    status_detail = models.CharField(_(u'detailed status'), max_length=2048)

    # This may be True even if the transaction hasn't actually been logged in
    # Google analytics. What it means is that we have made our best attempt to
    # log, but in case the user is blocking tracking scripts the transaction
    # will still not be logged.
    logged_to_google = models.BooleanField(default=False)

    @transaction.autocommit
    def process(self, request):
        self.save()

        ipn_url = request.build_absolute_uri(
            reverse('ipn_handler',
                    kwargs={'payment_id': self.id,
                            'payment_secret_uuid': self.secret_uuid}))

        return_url = request.build_absolute_uri(
            reverse('paypal_adaptive_return',
                    kwargs={'payment_id': self.id,
                            'payment_secret_uuid': self.secret_uuid}))
        cancel_url = request.build_absolute_uri(
            reverse('paypal_adaptive_cancel',
                    kwargs={'payment_id': self.id,
                            'payment_secret_uuid': self.secret_uuid}))

        # Cart to payment data
        receiver_email = self.payment_attempt.cart_stall.stall.paypal_email
        amount = self.amount
        pay = purchase.api.ChainedPayment(
            receiver_email,
            amount,
            self.discount_amount,
            request.META.get('REMOTE_ADDR'),
            return_url,
            cancel_url,
            ipn_url=ipn_url
        )

        self.debug_request = pay.raw_request
        self.debug_response = pay.raw_response
        self.pay_key = pay.paykey

        if pay.status == 'CREATED':
            self.status = Payment.STATUS_CREATED
        else:
            self.status = Payment.STATUS_ERROR

        self.save()

        return self.status == Payment.STATUS_CREATED

    def next_url(self):
        return '%s?cmd=_ap-payment&paykey=%s' \
            % (purchase_settings.PAYPAL_PAYMENT_HOST, self.pay_key)

    def execute(self):
        response = purchase.models.client.execute_payment(self.pay_key)
        self.status = response["paymentExecStatus"]
        self.save()


class PaymentReturnRedirect(models.Model):
    user = models.ForeignKey(User)
    payment_already_processed = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)