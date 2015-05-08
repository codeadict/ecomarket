from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.utils import unittest
from django.test import TestCase
from tests import factories
from accounts.models import UserProfile
from marketplace.models import Stall
import purchase
from purchase.models import Cart, CartStall, ShippingAddress, CartProduct, \
        OutOfStockError


class CartTestCase(TestCase):

    def setUp(self):
        super(CartTestCase, self).setUp()
        self.user = factories.UserFactory()
        self.cart = self.user.cart
        self.product = factories.ProductFactory.create(stock=10)

    def get_quantity(self):
        cart_stall = self.cart.cart_stalls.get(stall__id=self.product.stall.id)
        cart_product = cart_stall.cart_products.filter(product=self.product)
        if cart_product:
            return cart_product[0].quantity
        return 0

    def test_add_item_to_empty_cart_creates_cart_stall(self):
        self.cart.add(self.product)
        self.assertEqual(len(self.cart.cart_stalls.all()), 1)
        self.assertEqual(self.cart.cart_stalls.all()[0].stall.id, self.product.stall.id)

    def test_add_item_to_empty_cart_sets_quantity_correctly(self):
        self.cart.add(self.product)
        cart_stall = self.cart.cart_stalls.get(stall__id=self.product.stall.id)
        cart_products = cart_stall.cart_products.all()
        self.assertEqual(len(cart_products), 1)
        self.assertEqual(cart_products[0].quantity, 1)

    def test_add_item_to_existing_product_increments_quantity(self):
        self.cart.add(self.product)
        self.cart.add(self.product)
        self.assertEqual(self.get_quantity(), 2)

    def test_remove_item_decrements_quantity(self):
        self.cart.add(self.product)
        self.cart.add(self.product)
        self.cart.remove(self.product)
        self.assertEqual(self.get_quantity(), 1)

    def test_remove_single_product_removes_stall(self):
        self.cart.add(self.product)
        self.cart.remove(self.product)
        self.assertEqual(len(self.cart.cart_stalls.all()), 0)

    def test_remove_all_removes_all_products(self):
        other_product = factories.ProductFactory.create(stall=self.product.stall,
                                                 title="more shampoo")
        self.cart.add(other_product)
        self.cart.add(self.product)
        self.cart.add(self.product)
        self.cart.remove(self.product, remove_all=True)
        self.assertEqual(self.get_quantity(), 0)

    def test_remove_stall_removes_stall(self):
        self.cart.add(self.product)
        self.cart.remove_stall(self.product.stall)
        self.assertEqual(len(self.cart.cart_stalls.all()), 0)

    def test_set_quantity_sets_quantity(self):
        self.cart.set_quantity(self.product, 5)
        cart_stall = self.cart.cart_stalls.get(stall__id=self.product.stall.id)
        cart_prod = cart_stall.cart_products.all()[0]
        self.assertEqual(cart_prod.quantity, 5)

    def test_set_negative_quantity_raises(self):
        with self.assertRaises(RuntimeError):
            self.cart.set_quantity(self.product, -1)

    def test_get_quantity(self):
        self.cart.add(self.product)
        self.cart.add(self.product)
        self.assertEqual(self.cart.get_quantity(self.product), 2)

        other_product = factories.ProductFactory()
        self.assertEqual(self.cart.get_quantity(other_product), 0)

    def test_set_quantity_to_zero_removes_cart_product(self):
        self.cart.set_quantity(self.product, 2)
        self.cart.set_quantity(self.product, 0)
        cart_products = CartProduct.objects.filter(cart_stall__cart=self.cart,
                                                   product=self.product)
        self.assertEqual(len(cart_products.all()), 0)

    def test_set_quantity_to_zero_on_only_product_removes_cart_stall(self):
        self.cart.set_quantity(self.product, 3)
        self.cart.set_quantity(self.product, 0)
        self.assertEqual(len(self.cart.cart_stalls.all()), 0)

    def test_set_quantity_throws_exception_if_out_of_stock(self):
        self.product.stock = 2
        self.product.save()
        with self.assertRaises(purchase.models.OutOfStockError):
            self.cart.set_quantity(self.product, 3)

    def test_set_quantity_doesnt_throw_on_unlimited_stock(self):
        self.product.stock = None
        self.product.save()
        self.cart.set_quantity(self.product, 2)


class CartUserPostCreateSignalTestCase(TestCase):

    def test_cart_created_on_user_post_save(self):
        user = User.objects.create_user("username", "password")
        print("There are {0} carts".format(len(Cart.objects.all())))
        self.assertIsNotNone(user.cart)

    def test_cart_only_created_on_create(self):
        user = User.objects.create_user("username", "password")
        user.username="othername"
        user.save()
        self.assertEqual(len(Cart.objects.all()), 1)


class CartStallTestCase(TestCase):

    def setUp(self):
        super(CartStallTestCase, self).setUp()
        self.cart_stall = factories.create_cart_stall(0)
        self.product = factories.ProductFactory(stall=self.cart_stall.stall)

    def test_total_calculated_correctly(self):
        cart_product = CartProduct(cart_stall=self.cart_stall,
                                   unit_price=5,
                                   product=self.product,
                                   quantity=4)
        self.assertEqual(cart_product.total.amount, 20)



