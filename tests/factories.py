import factory
import money
from money.Money import Money

from django.contrib.auth.models import User

from accounts.models import ShippingAddress, UserProfile
from lovelists.models import LoveList
from marketplace.models import Stall, Product, Price, ShippingProfile, \
        Country, generate_identifier, ShippingRule, Category
from purchase.models import Cart, CartStall, CartProduct, LineItem, Order,\
        OrderFeedback, Refund, Payment, PaymentAttempt


# TODO: consider splitting this module into app-specific modules

class UserProfileFactory(factory.Factory):
    FACTORY_FOR = UserProfile


class UserFactory(factory.Factory):
    FACTORY_FOR = User

    @classmethod
    def _prepare(cls, create, **kwargs):
        password = kwargs.pop('password', None)
        user = super(UserFactory, cls)._prepare(create, **kwargs)
        if password:
            user.set_password(password)
            if create:
                user.save()
        return user

    username = factory.Sequence(lambda n: "john{0}".format(n))
    password = "password"
    user_profile = factory.RelatedFactory(UserProfileFactory, 'user')


class MerchantFactory(UserFactory):
    username = factory.Sequence(lambda n: "merchant{0}".format(n))
    password = "password"


class StallFactory(factory.Factory):
    FACTORY_FOR = Stall

    user = factory.SubFactory(MerchantFactory)
    title = factory.Sequence(lambda n: "Stall no {0}".format(n))
    paypal_email = "this@that.com"
    identifier = generate_identifier(Stall)


class CountryFactory(factory.Factory):
    code = factory.Sequence(lambda n: "GB{0}".format(n))
    title = factory.Sequence(lambda n: "United Kingdom no {0}".format(n))


class ShippingProfileFactory(factory.Factory):
    FACTORY_FOR = ShippingProfile

    title = factory.Sequence(lambda n: "default shipping {0}".format(n))
    stall = factory.SubFactory(StallFactory)
    shipping_country = factory.LazyAttribute(
        lambda a: Country.objects.get(code="GB"))
    others_delivery_time = 2
    others_delivery_time_max = 5
    others_price = None
    others_price_extra = None


class CartFactory(factory.Factory):
    """ You probably shouldn't use this factory, creating a user creates the
    cart for that user in the post_save signal.
    """
    FACTORY_FOR = Cart


class CartStallFactory(factory.Factory):
    FACTORY_FOR = CartStall

    @classmethod
    def _prepare(cls, create, **kwargs):
        if "address" not in kwargs:
            if create:
                address = ShippingAddressFactory(user=kwargs["cart"].user)
            else:
                address = \
                    ShippingAddressFactory.build(user=kwargs["cart"].user)
            kwargs["address"] = address
        return super(CartStallFactory, cls)._prepare(create, **kwargs)

    cart = factory.SubFactory(CartFactory)
    stall = factory.SubFactory(StallFactory)


class CategoryFactory(factory.Factory):
    FACTORY_FOR = Category

    name = u'Test Category'


class ProductFactory(factory.Factory):
    FACTORY_FOR = Product

    @classmethod
    def _prepare(cls, create, **kwargs):
        if "shipping_profile" not in kwargs:
            if create:
                ship_prof = ShippingProfileFactory(stall=kwargs["stall"])
            else:
                ship_prof = ShippingProfileFactory.build(stall=kwargs["stall"])
            kwargs["shipping_profile"] = ship_prof
        return super(ProductFactory, cls)._prepare(create, **kwargs)

    stall = factory.SubFactory(StallFactory)
    title = factory.Sequence(lambda n: "No {0} shampoo".format(n))
    stock = 10
    primary_category = factory.SubFactory(CategoryFactory)


class LoveListFactory(factory.Factory):

    FACTORY_FOR = LoveList

    user = factory.SubFactory(UserFactory)
    primary_category = factory.SubFactory(CategoryFactory)


class PriceFactory(factory.Factory):
    FACTORY_FOR = Price

    amount = 10
    product = factory.SubFactory(ProductFactory)


class CartProductFactory(factory.Factory):
    FACTORY_FOR = CartProduct

    cart_stall = factory.SubFactory(CartStallFactory)
    product = factory.SubFactory(ProductFactory)
    quantity = 10


class ShippingAddressFactory(factory.Factory):
    FACTORY_FOR = ShippingAddress

    name = "Shipping name"
    line1 = "line 1"
    line2 = "line 2"
    city = "BigCity"
    state = "what a state"
    country = factory.LazyAttribute(lambda a: Country.objects.get(code="GB"))
    postal_code = "E1 4PD"


class OrderFactory(factory.Factory):

    @classmethod
    def _prepare(cls, create, **kwargs):
        if "address" not in kwargs:
            if create:
                address = ShippingAddressFactory(user=kwargs["user"])
            else:
                address = ShippingAddressFactory.build(user=kwargs["user"])
            kwargs["address"] = address
        return super(OrderFactory, cls)._prepare(create, **kwargs)

    user = factory.SubFactory(UserFactory)
    delivery_charge = Money(10, money.CURRENCY["GBP"])
    stall = factory.SubFactory(StallFactory)


class LineItemFactory(factory.Factory):
    FACTORY_FOR = LineItem

    product = factory.SubFactory(ProductFactory)
    price = 10
    quantity = 10
    dispatched = False
    order = factory.SubFactory(OrderFactory)


class RefundFactory(factory.Factory):
    FACTORY_FOR = Refund

    order = factory.SubFactory(OrderFactory)
    reason = "No smoke without fire"


class FeedbackFactory(factory.Factory):
    FACTORY_FOR = OrderFeedback

    order = factory.SubFactory(OrderFactory)
    feedback_text = "Awesome merchant"


class PaymentFactory(factory.Factory):
    status = Payment.STATUS_CREATED
    amount = Money(10, money.CURRENCY["GBP"])
    pay_key = "some-pay-key"
    purchaser = factory.SubFactory(UserFactory)


class ShippingRuleFactory(factory.Factory):
    FACTORY_FOR = ShippingRule

    profile = factory.SubFactory(ShippingProfileFactory)
    rule_price = Money(10, money.CURRENCY["GBP"])
    rule_price_extra = Money(20, money.CURRENCY["GBP"])
    despatch_time = 2
    delivery_time = 5
    delivery_time_max = 10


class PaymentAttemptFactory(factory.Factory):
    FACTORY_FOR = PaymentAttempt

    cart_stall = factory.SubFactory(CartStallFactory)
    payment = factory.SubFactory(PaymentFactory)


def create_order(num_items, dispatched=False,
                 payment_status=Payment.STATUS_CREATED,
                 **kwargs):
    """Creates an order with num_items line items. If dispatched is True
    all the line_items will be marked as dispatched
    """
    order = OrderFactory(**kwargs)
    for index in range(num_items):
        product = ProductFactory(stall=order.stall)
        attrs = LineItemFactory.attributes()
        attrs.update({
            "product": product,
            "dispatched": dispatched,
        })
        order.line_items.create(**attrs)
    payment_amount = sum([l.price for l in order.line_items.all()])
    PaymentFactory(
        order=order,
        amount=payment_amount,
        purchaser=order.user,
        status=payment_status,
    )
    o = Order.objects.get(id=order.id)
    if "created" in kwargs:
        o.created = kwargs["created"]
        o.save()
    return Order.objects.get(id=order.id)


def create_cart_stall(num_products=1, price=5, user=None, address=None):
    """Creates a cart stall with num_products products in it"""
    stall = StallFactory()
    ship_prof = ShippingProfileFactory(
        stall=stall,
        shipping_country=Country.objects.get(code="GB"),
    )
    ship_rule = ShippingRuleFactory(
        profile=ship_prof
    )
    if not user:
        user = UserFactory()
    if not address:
        address = ShippingAddressFactory(
            user=user, country=Country.objects.get(code="GB"))
    ship_rule.countries.add(address.country)
    ship_rule.save()
    cart_stall = CartStallFactory(
        cart=user.cart,
        address=address,
        stall=stall
    )

    stall = cart_stall.stall
    for index in range(num_products):
        product = ProductFactory(stall=stall, shipping_profile=ship_prof)
        prod_price = PriceFactory(product=product)
        CartProductFactory(cart_stall=cart_stall, product=product,
                           unit_price=prod_price.amount,
                           quantity=num_products)
    return cart_stall
