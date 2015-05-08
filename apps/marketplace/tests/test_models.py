from django.test import TestCase
from tests import factories

from marketplace.management.commands import set_number_of_product_sales
from marketplace.models import Country


class ProductTestCase(TestCase):

    def test_in_stock_true_if_stock_is_none(self):
        product = factories.ProductFactory(stock=None)
        self.assertTrue(product.in_stock())

    def test_in_stock_true_if_stock_is_nonzero(self):
        product = factories.ProductFactory(stock=5)
        self.assertTrue(product.in_stock())

    def test_in_stock_false_if_stock_is_zero(self):
        product = factories.ProductFactory(stock=0)
        self.assertFalse(product.in_stock())


class ProductCategoriesTestCase(TestCase):

    def setUp(self):
        self.cat1 = factories.CategoryFactory(name="cat1")
        self.cat2 = factories.CategoryFactory(name="cat2", parent=self.cat1)
        self.product = factories.ProductFactory(primary_category=self.cat2)

    def test_categories_returned_in_correct_order(self):
        cats = self.product.category_objs()
        self.assertEqual(list(cats), [self.cat1, self.cat2])

    def test_categories_returns_string(self):
        cats = self.product.categories
        self.assertEqual(list(cats), ["cat1", "cat2"])

    def test_categories_absolute_url(self):
        self.assertEqual(self.cat1.get_absolute_url(), "/discover/cat1/")
        self.assertEqual(self.cat2.get_absolute_url(), "/discover/cat1/cat2/")


class ShippingRuleTestCase(TestCase):

    def test_to_json(self):
        rule = factories.ShippingRuleFactory(
            rule_price=10,
            rule_price_extra=20,
            despatch_time=2,
            delivery_time=10,
            delivery_time_max=20
        )
        country1 = factories.CountryFactory(code="USA")
        country2 = factories.CountryFactory(code="NL")
        rule.countries.add(country1)
        rule.countries.add(country2)
        rule.save()
        expected = {
            "rule_price": 10.0,
            "rule_price_extra": 20.0,
            "dispatch_time": 2,
            "delivery_time": 10,
            "delivery_time_max": 20,
        }
        result = rule.to_json()
        countries = result.pop("countries")
        self.assertEqual(len(countries), 2)
        self.assertEqual(expected, result)


class ShippingProfileTestCase(TestCase):

    def create_profile_with_uk(self):
        rule = factories.ShippingRuleFactory()
        uk = Country.objects.get(code="GB")
        rule.countries.add(uk)
        rule.save()
        return rule.profile

    def test_to_json(self):
        profile = factories.ShippingProfileFactory()
        factories.ShippingRuleFactory(profile=profile)
        result = profile.to_json()
        self.assertEqual(len(result["rules"]), 1)
        self.assertEqual(result["shipping_country"]["code"], "GB")
        self.assertEqual(result["ships_worldwide"], False)

    def test_to_json_on_ships_worldwide(self):
        profile = factories.ShippingProfileFactory(
            others_price=10,
            others_price_extra=20
        )
        factories.ShippingRuleFactory(profile=profile)
        result = profile.to_json()
        self.assertTrue(result["ships_worldwide"])
        self.assertEqual(result["others_price"], 10.0)
        self.assertEqual(result["others_price_extra"], 20.0)

    def test_to_json_contains_default_country(self):
        profile = self.create_profile_with_uk()
        result = profile.to_json()
        self.assertEqual(result["default_country_code"], "GB")

    def test_get_default_country_returns_uk_if_in_ruleset(self):
        uk = Country.objects.get(code="GB")
        profile = self.create_profile_with_uk()
        self.assertEqual(profile.get_default_country(), uk)

    def test_get_default_country_returns_first_in_list_if_not_uk(self):
        country1 = factories.CountryFactory(code="USA")
        rule = factories.ShippingRuleFactory()
        rule.countries = [country1]
        rule.save()
        self.assertEqual(rule.profile.get_default_country(), country1)

    def test_get_default_country_returns_none_if_no_rules(self):
        rule = factories.ShippingRuleFactory()
        self.assertIsNone(rule.profile.get_default_country())


class ProductNumberofSalesTest(TestCase):

    def setUp(self):
        self.prod1 = factories.ProductFactory()
        self.prod2 = factories.ProductFactory()
        self.prod3 = factories.ProductFactory()

    def _set_orders(self, product, orders):
        for quantity in orders:
            factories.LineItemFactory(
                product=product, quantity=quantity,
                order=factories.OrderFactory(stall=product.stall))

    def _check_orders(self, product, expected_orders):
        # We need to reload the product
        product = type(product).objects.get(id=product.id)
        self.assertEqual(product.number_of_sales, expected_orders)

    def test(self):
        self._set_orders(self.prod1, (1, 2, 3))
        self._set_orders(self.prod2, (4, 5, 6))
        self._set_orders(self.prod3, (7, ))
        # TODO it would be nice if we could test number_of_sales being updated
        # as orders are placed, but that would require a much more advanced
        # test (ie. integration testing) at present
        set_number_of_product_sales.Command().execute(verbosity=1)
        self._check_orders(self.prod1, 6)   # 1 + 2 + 3
        self._check_orders(self.prod2, 15)  # 4 + 5 + 6
        self._check_orders(self.prod3, 7)
