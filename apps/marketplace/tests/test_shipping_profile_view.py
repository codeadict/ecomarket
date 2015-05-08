from django.utils import unittest

from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.test import TestCase

from marketplace.models \
    import Stall, ShippingProfile, Country
from tests import factories


class BaseShippingProfileTestCase(TestCase):

    def setUp(self):
        self.userid = 'myuser'
        self.pw = 'mypassword'
        self.user = User.objects.create_user(
            self.userid, password=self.pw)
        self.stall = Stall.objects.create(
            user=self.user)
        self.client.login(
            username=self.userid,
            password=self.pw)

    def _create_country(self, country):
        return Country.objects.create(
            title=country,
            code=country[:2].lower())

    def _create_shipping_profile(self, title, country):
        shipping_country = self._create_country(country)
        return ShippingProfile.objects.create(
            title=title,
            shipping_country=shipping_country,
            stall=self.stall)

    def _create_shipping_rule(self, shipping_profile, countries):
        return factories.ShippingRuleFactory(profile=shipping_profile)

    def _get(self, params=None):
        params = [
            '%s=%s' % (k, v)
            for k, v in (params or {}).items()]
        if params:
            return self.client.get(
                '%s?%s' % (
                    reverse("stall_shipping_profile"),
                    '&'.join(params)))
        return self.client.get(
            reverse("stall_shipping_profile"))

    def _post(self, data=None):
        return self.client.post(
            reverse("stall_shipping_profile"),
            data=data or {})


class ShippingProfileViewTestCase(BaseShippingProfileTestCase):

    # TODO: Fix these tests

    @unittest.skip
    def test_get_with_no_profileid(self):
        response = self._get()
        self.assertEqual(
            response.context['profile'], None)
        self.assertEqual(
            response.context['rules'], [])

    @unittest.skip
    def test_get_with_invalid_profileid(self):
        response = self._get(
            {'profile': 'Foo'})
        self.assertEqual(
            response.context['profile'], None)
        self.assertEqual(
            response.context['rules'], [])

    @unittest.skip
    def test_get_with_profileid(self):
        shipping_profile = self._create_shipping_profile(
            'Bar', 'Barland')
        self._create_shipping_rule(
            shipping_profile, [])
        response = self._get(
            {'profile': shipping_profile.id})
        self.assertEqual(
            response.context['profile'].title, 'Bar')
        self.assertEqual(
            len(response.context['rules']), 1)
