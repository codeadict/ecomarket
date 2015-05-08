from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.utils import unittest
from django.test import TestCase

from accounts.models import UserProfile, ShippingAddress
from marketplace.models import Country


class AccountShippingAddressTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user("ausername", password="apassword")
        self.user_profile = UserProfile.objects.create(user=self.user)
        self.client.login(username="ausername", password="apassword")
        self.country = Country.objects.get(code="GB")
        self.data = {
                "line1":"Line 1 of address",
                "line2":"line 2",
                "city":"city",
                "state":"what a state",
                "postal_code":"ed34rt",
                "name":"address name",
                "country":self.country.id,
                }

    def create_addr(self):
        data = self.data.copy()
        data.pop("country")
        addr = ShippingAddress(user=self.user,
                country=self.country, **data)
        addr.save()
        return addr

    def do_get(self):
        view_url = reverse("account_delivery_addresses")
        return self.client.get(view_url)

    def do_post(self, data, address_id=None):
        if address_id:
            view_url = reverse("account_delivery_addresses", kwargs={"address_id":address_id})
        else:
            view_url = reverse("account_delivery_addresses")
        return self.client.post(view_url, data=data)

    def test_show_with_no_shippingaddresses_renders_create_form(self):
        response = self.do_get()
        self.assertEqual(len(response.context["addresses"]), 0)
        self.assertIsNotNone(response.context["address_form"])

    def test_show_with_shipping_addresses_contains_addresses(self):
        address = self.create_addr()
        response = self.do_get()
        self.assertEqual(response.context["addresses"][0].id, address.id)
        self.assertEqual(len(response.context["addresses"]), 1)

    def test_create_address(self):
        response = self.do_post(self.data)
        addresses = self.user.addresses.all()
        self.assertEqual(len(addresses), 1)
        self.assertEqual(addresses[0].line1, "Line 1 of address")

    def test_update_address(self):
        addr = self.create_addr()
        new_data = self.data.copy()
        new_data["line1"] = "new line 1"
        response = self.do_post(data=new_data, address_id=addr.id)
        new_addr = ShippingAddress.objects.get(id=addr.id)
        self.assertEqual(new_addr.line1, "new line 1")
