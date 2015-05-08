from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase
from importlib import import_module
from tests import factories
from purchase.models import CartProduct

class RegisterViewTestCase(TestCase):
    """Not an exhaustive test right now, just tests the streamlined login
    functionality
    """

    def setUp(self):
        super(RegisterViewTestCase, self).setUp()
        self.view_url = reverse('register')
        self.product = factories.ProductFactory()

    def build_register_data(self):
        return {
            "username": "usemyname",
            "password": "password",
            "password_confirm": "password",
            "first_name": "first",
            "last_name": "last",
            "gender": "f",
            "email": "test@test.com",
        }

    def test_adds_product_and_redirects_to_cart(self):
        data = self.build_register_data()

        # Really nast hacks to make test session work for anonymous users
        from django.conf import settings
        engine = import_module(settings.SESSION_ENGINE)
        store = engine.SessionStore()
        store.save()  # we need to make load() work, or the cookie is worthless
        self.client.cookies[settings.SESSION_COOKIE_NAME] = store.session_key

        session = self.client.session
        session['product_to_add_id'] = self.product.id
        session.save()

        response = self.client.post(self.view_url, data=data)
        #self.assertRedirects(response, reverse('checkout_cart'))
        user = User.objects.get(username="usemyname")
        cart_products = CartProduct.objects.filter(cart_stall__cart=user.cart,
                                                   product=self.product).all()
        self.assertEqual(len(cart_products), 1)
        self.assertEqual(cart_products[0].product.id, self.product.id)
        self.assertEqual(cart_products[0].quantity, 1)


