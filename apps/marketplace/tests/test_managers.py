from django.test import TestCase
from marketplace.models import Product
from tests import factories

class ProductManagerTestCase(TestCase):

    def test_unpublished_method_returns_draft_and_unpublished(self):
        published = factories.ProductFactory(status=Product.PUBLISHED_LIVE)
        draft = factories.ProductFactory(status=Product.PUBLISHED_DRAFT)
        unpublished = factories.ProductFactory(
            status=Product.PUBLISHED_UNPUBLISHED)
        result = Product.objects.unpublished()
        self.assertEqual(len(result), 2)
        self.assertEqual(set(result), set([draft, unpublished]))
