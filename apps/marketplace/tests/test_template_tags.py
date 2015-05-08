from django.test import TestCase
from tests import factories

from marketplace.templatetags import breadcrumb


class BreadcrumbTest(TestCase):

    def setUp(self):
        self.cat1 = factories.CategoryFactory(name="cat1")
        self.cat2 = factories.CategoryFactory(name="cat2", parent=self.cat1)
        self.product = factories.ProductFactory(title="Brand name shampoo",
                                                primary_category=self.cat2)

    def check_breadcrumb(self, thing, expected):
        context = breadcrumb.generate_breadcrumb(thing)
        self.assertEqual(context, {
            "breadcrumbs": [("/", "Eco Market")] + expected,
        })

    def test_category(self):
        cat1_breadcrumb = [("/discover/cat1/", "cat1")]
        cat2_breadcrumb = cat1_breadcrumb + [("/discover/cat1/cat2/", "cat2")]
        # Empty URL is OK here as final crumb never shows URL
        product_breadcrumb = cat2_breadcrumb + [("", "Brand name shampoo")]
        self.check_breadcrumb(self.cat1, cat1_breadcrumb)
        self.check_breadcrumb(self.cat2, cat2_breadcrumb)
        self.check_breadcrumb(self.product, product_breadcrumb)
