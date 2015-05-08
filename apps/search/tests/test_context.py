from django.core.management import call_command
from django.core.urlresolvers import reverse
from django.test import TestCase, Client

from tests.factories import CategoryFactory, ProductFactory


class SearchTermsTest(TestCase):

    def setUp(self):
        self.client = Client()
        category = CategoryFactory(slug="tier2",
                                   parent=CategoryFactory(slug="tier1"))
        # We need a category so haystack doesn't get upset
        ProductFactory(primary_category=category, status="l")
        call_command("rebuild_index", interactive=False)
        self.addCleanup(call_command, "clear_index", interactive=False)

    def check_search_terms(self, url_name, args, qs, expected_search_terms):
        qs = "?%s" % qs if qs else ""
        url = reverse(url_name, args=args) + qs
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        search_terms = response.context["search_terms"]
        self.assertEqual(search_terms, expected_search_terms)

    def test_discover(self):
        url_name = "category_discover"
        self.check_search_terms(url_name, (), "", "")
        self.check_search_terms(url_name, ("tier1", ), "", "tier1/")
        self.check_search_terms(url_name, ("tier1", ), "q=foo&causes=bar", "tier1/")
        self.check_search_terms(url_name, ("tier1", "tier2"), "", "tier1/tier2/")
        self.check_search_terms(url_name, ("tier1", "tier2"), "q=foo&price=10-20&recipients=bar&ships_from=DE&causes=baz&ships_to=UK&colors=green", "tier1/tier2/?q=foo&recipients=bar&causes=baz&colors=green")

    def test_search(self):
        url_name = "product_search"
        self.check_search_terms(url_name, (), "", "")
        self.check_search_terms(url_name, ("tier1", ), "", "tier1/")
        self.check_search_terms(url_name, ("tier1", ), "q=foo&causes=bar", "tier1/?q=foo&causes=bar")
        self.check_search_terms(url_name, ("tier1", "tier2"), "", "tier1/tier2/")
        self.check_search_terms(url_name, ("tier1", "tier2"), "q=foo&price=10-20&recipients=bar&ships_from=DE&causes=baz&ships_to=UK&colors=green", "tier1/tier2/?q=foo&recipients=bar&causes=baz&colors=green")
