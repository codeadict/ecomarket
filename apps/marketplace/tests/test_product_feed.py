from lxml import etree
from django.test import TestCase
from marketplace.product_feed import (
        XMLProductFeedBuilder, TextProductFeedBuilder)
from marketplace.models import Country
import mock
from tests import factories


class FeedBuilderTestCase(TestCase):

    def setUp(self):
        self.product = factories.ProductFactory(
            title="My Product title",
            description="My product description",
            stall__identifier="12345678",
        )
        self.price = factories.PriceFactory(product=self.product, amount=10)
        self.category_mapper = mock.Mock()
        self.category_mapper.get_category.return_value = \
            "some category > some child category"
        self.builder = self.FEED_BUILDER_CLASS(self.product,
                                               self.category_mapper)


class XMLFeedBuilderTestCase(FeedBuilderTestCase):

    FEED_BUILDER_CLASS = XMLProductFeedBuilder

    def test_builder_title_generated(self):
        expected = "<title>My Product title</title>"
        actual = etree.tostring(self.builder.generate_title())
        self.assertEqual(expected, actual)

    def test_builder_generates_description(self):
        expected = "<description>My product description</description>"
        actual = etree.tostring(self.builder.generate_description())
        self.assertEqual(expected, actual)

    def test_generate_description_removes_invalid_control_characters(self):
        self.product.description = "this is invalid \x0b blah blah"
        expected = "<description>this is invalid  blah blah</description>"
        actual = etree.tostring(self.builder.generate_description())
        self.assertEqual(expected, actual)

    def test_generate_description_uses_utf8_encoding(self):
        self.product.description = "this is invalid \xe2\x80\xa6 blah blah"
        expected = \
            "<description>this is invalid &#8230; blah blah</description>"
        actual = etree.tostring(self.builder.generate_description())
        self.assertEqual(expected, actual)

    def test_builder_generates_link(self):
        expected = \
            "<link>http://localhost:8000/products/12345678/my-product-title/</link>"
        actual = etree.tostring(self.builder.generate_link())
        self.assertEqual(expected, actual)

    def test_generates_image_link(self):
        expected_link = \
            "http://localhost:8000{0}".format(self.product.image.url_400)
        expected = "<g:image_link xmlns:g=\"http://base.google.com/ns/1.0\" xmlns=\"\">{0}</g:image_link>".format(expected_link)
        actual = etree.tostring(self.builder.generate_image_link())
        self.assertEqual(expected, actual)

    def test_generates_condition(self):
        expected = "<g:condition xmlns:g=\"http://base.google.com/ns/1.0\" xmlns=\"\">new</g:condition>"
        actual = etree.tostring(self.builder.generate_condition())
        self.assertEqual(expected, actual)

    def test_generates_new(self):
        expected = "<g:price xmlns:g=\"http://base.google.com/ns/1.0\" xmlns=\"\">10 GBP</g:price>"
        actual = etree.tostring(self.builder.generate_price())
        self.assertEqual(expected, actual)

    def test_generates_in_stock_if_product_in_stock(self):
        self.product.stock = 4
        expected = "<g:availability xmlns:g=\"http://base.google.com/ns/1.0\" xmlns=\"\">in stock</g:availability>"
        actual = etree.tostring(self.builder.generate_availability())
        self.assertEqual(expected, actual)

    def test_generates_out_of_stock_if_product_out_of_stock(self):
        self.product.stock = 0
        expected = "<g:availability xmlns:g=\"http://base.google.com/ns/1.0\" xmlns=\"\">out of stock</g:availability>"
        actual = etree.tostring(self.builder.generate_availability())
        self.assertEqual(expected, actual)

    def test_generates_id(self):
        expected = "<g:id xmlns:g=\"http://base.google.com/ns/1.0\" xmlns=\"\">{0}</g:id>".format(
            self.product.id)
        actual = etree.tostring(self.builder.generate_id())
        self.assertEqual(expected, actual)

    def test_generates_shipping(self):
        profile = self.product.shipping_profile
        rule = factories.ShippingRuleFactory(
            profile=profile,
            rule_price=10,
            rule_price_extra=5,
        )
        rule.countries.add(Country.objects.get(code="GB"))
        rule.save()
        expected = "<g:shipping xmlns:g=\"http://base.google.com/ns/1.0\" xmlns=\"\"><g:country>GB</g:country><g:price>10 GBP</g:price></g:shipping>"
        actual_elems = self.builder.generate_shipping()
        self.assertEqual(len(actual_elems), 1)
        actual = etree.tostring(actual_elems[0])
        self.assertEqual(expected, actual)


class TextFeedBuilderTestCase(FeedBuilderTestCase):

    FEED_BUILDER_CLASS = TextProductFeedBuilder

    def test(self):
        profile = self.product.shipping_profile
        rule = factories.ShippingRuleFactory(
            profile=profile,
            rule_price=10,
            rule_price_extra=5,
        )
        rule.countries.add(Country.objects.get(code="GB"))
        rule.save()
        expected = [
            str(self.product.id),
            self.product.title,
            self.product.description,
            "http://localhost:8000/products/12345678/my-product-title/",
            "http://localhost:8000/static/images/product/400/default.png",
            "new",
            "10 GBP",
            "in stock",
            "some category > some child category",
            "Test Category",
            "GB:::10 GBP",
        ]
        actual = self.builder.generate()
        self.assertEqual(expected, actual)
