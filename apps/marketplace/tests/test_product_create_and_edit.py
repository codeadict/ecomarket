from marketplace.forms import ProductCreationForm
from marketplace.models import Product
from django.test import TestCase
from django.http import QueryDict
import mock
from tests import factories
import urllib

def get_valid_form_data(stall):
    profile = factories.ShippingProfileFactory(stall=stall)
    category = factories.CategoryFactory()
    return {
        "title": "Some Product",
        "description": "This is a productive product",
        "primary_category": category.id,
        "keywords_field": ["keyword1", "keyword2"],
        "shipping_profile": profile.id,
        "status": Product.PUBLISHED_DRAFT,
        "save-publish":True,
    }

class ProductFormKeywordsTestCase(TestCase):

    def get_form_for_keyword_data(self, keywords):
        stall = factories.StallFactory()
        data = dict(get_valid_form_data(stall))
        querystring = urllib.urlencode(data)
        querydict = QueryDict(querystring).copy() #copy so it's mutable
        querydict.setlist("keywords_field", keywords)
        mock_request = mock.Mock()
        mock_request.POST = querydict
        return ProductCreationForm(querydict, request=mock_request, stall=stall)

    def test_keywords_with_commas_give_errors(self):
        form = self.get_form_for_keyword_data(["keyword1", "keyword, 2"])
        form.is_valid()
        errors = form.errors["keywords_field"]
        self.assertEqual(errors, ["Commas are not allowed in keywords"])

    def test_on_save_saves_keywords(self):
        form = self.get_form_for_keyword_data(["biscuits"])
        print(form.errors)
        form.save()
        product = form.save()
        self.assertEqual(product.keywords.all()[0].title, "biscuits")

