from django.test import TestCase
from django.test.client import RequestFactory
from django.views.generic import ListView
from tests.utils import RenderingObjectTestCase

from main.utils import DynamicPaginationMixin
from main.utils.dynamic_paginate_view import  PaginateByControl, PaginateByOption

class TestPaginationView(DynamicPaginationMixin, ListView):
    pass

class DynamicPaginationTestCase(TestCase):

    def setUp(self):
        self.factory = RequestFactory()

    def create_view(self, paginate_by=None):
        view = TestPaginationView()
        if paginate_by:
            url = "/ignored?paginate_by={0}".format(paginate_by)
        else:
            url = "/ignored"
        request = self.factory.get(url)
        view.request = request
        view.kwargs = {}
        view.args = []
        return view

    def test_paginate_by_got_from_get_params(self):
        view = self.create_view(paginate_by=20)
        self.assertEqual(view.get_paginate_by("ignored"), 20)

    def test_paginate_by_default_is_10(self):
        view = self.create_view()
        self.assertEqual(view.get_paginate_by("ignored"), 10)

    def test_context_contains_pagination_control(self):
        view = self.create_view()
        context = view.get_context_data(object_list=[1,2,3,4,5])
        self.assertTrue("paginate_by_control" in context)


class PaginateByControlTestCase(RenderingObjectTestCase):

    def setUp(self):
        self.template_name = "main/includes/paginate_by_control.html"
        self.request = RequestFactory().get("/ignored")
        self.paginate_by_control = PaginateByControl(10, [10, 50, 100], self.request)

    def test_paginate_control_context_contains_all_allowed(self):
        expected = [
            PaginateByOption(10, True, self.request),
            PaginateByOption(50, False, self.request),
            PaginateByOption(100, False, self.request),
        ]
        self.assert_rendered_context_contains(self.paginate_by_control,
                                              {"paginate_by_options": expected})

class PaginateByOptionTestCase(TestCase):

    def setUp(self):
        self.request = RequestFactory().get("/ignored")
        self.paginate_by_option = PaginateByOption(10, True, self.request)

    def test_activate_link(self):
        self.assertEqual(self.paginate_by_option.activate_url, "http://testserver/ignored?paginate_by=10")

