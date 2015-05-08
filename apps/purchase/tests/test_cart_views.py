from accounts.models import UserProfile
from django.core.urlresolvers import reverse
from django.test import TestCase
from marketplace.models import Country
from purchase.models import CartStall, CartProduct
from tests import factories

import json
import mock
import money
import purchase.models

class CartProductsViewPutTestCase(TestCase):

    def setUp(self):
        super(CartProductsViewPutTestCase, self).setUp()
        self.cart_stall = factories.create_cart_stall(1)
        product1 = self.cart_stall.cart_products.all()[0].product
        self.product = factories.ProductFactory(
            stall=self.cart_stall.stall,
            shipping_profile=product1.shipping_profile
        )
        self.cart = self.cart_stall.cart
        self.view_url = reverse('cart_products',
                                kwargs={
                                    "cart_id":self.cart.id,
                                    "product_id": self.product.id,
                                })
        self.client.login(username=self.cart.user.username,
                          password="password")

    def test_quantity_sets_specified_quantity(self):
        data = {
            "quantity": 5
        }
        response = self.client.put(self.view_url,
                                   data=json.dumps(data),
                                   content_type='application/json'
                                   )
        self.assertEqual(self.cart.get_quantity(self.product), 5)

    def test_ajax_request_responds_with_json(self):
        response = self.client.put(
            self.view_url,
            data=json.dumps({"quantity": 10}),
            content_type='application/json',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response["Content-Type"], "application/json")
        data = json.loads(response.content)
        self.assertEqual(data["product_id"], self.product.id)
        self.assertEqual(data["quantity"], 10)

    def test_out_of_stock_returns_409(self):
        self.product.stock = 10
        self.product.save()
        response = self.client.put(
            self.view_url,
            content_type='application/json',
            data=json.dumps({"quantity": 20}),
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 409)


class CartProductsViewPostTestCase(TestCase):

    def setUp(self):
        super(CartProductsViewPostTestCase, self).setUp()
        self.cart_stall = factories.create_cart_stall(1)
        product1 = self.cart_stall.cart_products.all()[0].product
        self.product = factories.ProductFactory(
            stall=self.cart_stall.stall,
            shipping_profile=product1.shipping_profile
        )
        self.cart = self.cart_stall.cart
        self.view_url = reverse('cart_products',
                                kwargs={
                                    "cart_id":self.cart.id
                                })
        self.client.login(username=self.cart.user.username,
                          password="password")

    def test_throws_404_if_cart_does_not_exist(self):
        view_url = reverse('cart_products',
                           kwargs={"cart_id":3})
        response = self.client.post(view_url)
        self.assertEqual(response.status_code, 404)

    def test_throws_403_if_cart_does_not_belong_to_user(self):
        other_user = factories.UserFactory()
        self.client.login(username=other_user.username, password="password")
        response = self.client.post(self.view_url)
        self.assertEqual(response.status_code, 403)

    def test_post_adds_to_cart(self):
        data = {"product_id": self.product.id, "quantity":2}
        response = self.client.post(self.view_url, data=data)

        cart_stall = CartStall.objects.get(id=self.cart_stall.id)
        cart_prod = cart_stall.cart_products.all()
        self.assertEqual(len(cart_prod), 2)
        self.assertEqual(cart_prod[1].product.id, self.product.id)

    def test_throws_404_if_product_does_not_exist(self):
        response = self.client.post(self.view_url, data={"product_id":4})
        self.assertEqual(response.status_code, 404)


class CartProductsViewDeleteTestCase(TestCase):

    def setUp(self):
        super(CartProductsViewDeleteTestCase, self).setUp()
        self.cart_stall = factories.create_cart_stall(1)
        self.product = self.cart_stall.cart_products.all()[0].product
        self.cart = self.cart_stall.cart
        self.view_url = reverse('cart_products',
                                kwargs={
                                    "cart_id":self.cart.id,
                                    "product_id": self.product.id,
                                })
        self.client.login(username=self.cart.user.username,
                          password="password")

    def test_delete_removes_cartproduct(self):
        response = self.client.delete(self.view_url)
        cart_prods = CartProduct.objects.filter(cart_stall=self.cart_stall, product=self.product)
        self.assertEqual(len(cart_prods.all()), 0)
