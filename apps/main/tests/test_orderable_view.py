from django.test import TestCase
from django.test.client import RequestFactory
import django.template.loader
from main.utils import OrderableListView, SortTab
import mock
from tests.utils import Matcher, RenderingObjectTestCase, compare_urls

class TestView(OrderableListView):
    queryset = [1,2,3,4,5]
    default_order = "created-desc"
    tabs = ["username", {"email": "user email"}]

class OrderableViewTestCase(TestCase):

    def create_view(self, order_by=None, *args, **kwargs):
        factory = RequestFactory()
        if order_by:
            url = '/ignored?order_by={0}'.format(order_by)
        else:
            url = '/ignored'
        request = factory.get(url)
        view = TestView()
        view.request = request
        view.args = args
        view.kwargs = kwargs
        return view

    def test_get_queryset_uses_default_order(self):
        view = self.create_view()
        self.assertEqual(view.get_queryset_order(), "-created")

    def test_get_queryset_with_order_by_parameter(self):
        view = self.create_view(order_by="username-asc")
        self.assertEqual(view.get_queryset_order(), "username")

    def test_get_queryset_with_desc_order_by_parameters(self):
        view = self.create_view(order_by="username-desc")
        self.assertEqual(view.get_queryset_order(), "-username")

    def test_get_context_data_contains_default_order(self):
        view = self.create_view()
        data = view.get_context_data(object_list=[1,2,3,4,5])
        self.assertEqual(data["order_by"], "created-desc")

    def test_get_context_data_with_non_default_order(self):
        view = self.create_view(order_by="username-asc")
        data = view.get_context_data(object_list=[1,2,3,4,5])
        self.assertEqual(data["order_by"], "username-asc")

    def test_queryset_order_by_called_with_default_order_param(self):
        view = self.create_view()
        mock_queryset = mock.Mock(spec=["order_by"])
        view.queryset = mock_queryset
        view.get_queryset()
        mock_queryset.order_by.assert_called_with("-created")

    def test_queryset_order_by_called_with_order_by_parameter(self):
        view = self.create_view(order_by='username')
        mock_queryset = mock.Mock(spec=["order_by"])
        view.queryset = mock_queryset
        view.get_queryset()
        mock_queryset.order_by.assert_called_with("username")

    def test_get_sorttab(self):
        view = self.create_view(order_by='username')
        sorttab = view.get_sort_tab("username")
        self.assertEqual(sorttab.is_active(), True)

    def test_get_sorttab_not_active(self):
        view = self.create_view(order_by='ignored')
        sorttab = view.get_sort_tab("username")
        self.assertEqual(sorttab.is_active(), False)

    def test_get_sorttab_order(self):
        view = self.create_view(order_by='username-asc')
        sorttab = view.get_sort_tab('username')
        self.assertEqual(sorttab.ascending, True)

    def test_get_sorttab_order(self):
        view = self.create_view(order_by='username-desc')
        sorttab = view.get_sort_tab('username')
        self.assertEqual(sorttab.ascending, False)

    def test_tab_fields_added_to_context(self):
        view = self.create_view(order_by="username=desc")
        data = view.get_context_data(object_list=[1,2,3,4,5])
        self.assertTrue("username_tab" in data)

    def test_dictionary_tabs_added_to_context(self):
        view = self.create_view(order_by="username-desc")
        data = view.get_context_data(object_list=[1,2,3,4])
        self.assertTrue("email_tab" in data)
        self.assertEqual(data["email_tab"].display_name, "user email")


class SortTabTestCase(RenderingObjectTestCase):

    def setUp(self):
        self.fieldname = "created"
        self.template_name = "main/includes/sortable-tab.html"
        self.factory = RequestFactory()
        self.request = self.factory.get("/someurl")

    def create_sorttab(self, order_by, ascending=True, display_name=None):
        return SortTab(self.fieldname, order_by, self.request, ascending=ascending,
                       display_name=display_name)

    def test_context_active_if_fieldname_matches(self):
        tab = self.create_sorttab("created")
        self.assert_rendered_context_contains(tab, {"active":True})

    def test_context_not_active_if_fieldname_is_not_matches(self):
        tab = self.create_sorttab('username')
        self.assert_rendered_context_contains(tab, {"active": False})

    def test_ascending_context_variable_correctly_set(self):
        tab = self.create_sorttab(self.fieldname)
        self.assert_rendered_context_contains(tab, {"active":True, "ascending":True})

    def test_ascending_context_variable_correctly_set_descending(self):
        tab = self.create_sorttab(self.fieldname, ascending=False)
        self.assert_rendered_context_contains(tab, {"active":True, "ascending":False})

    def test_active_ascending_link(self):
        tab = self.create_sorttab("somefield")
        expected_link = "http://testserver/someurl?order_by={0}-asc&page=1".format(self.fieldname)
        self.assert_rendered_context_contains(tab,
                                              {"ascending_link": expected_link})

    def test_active_descending_link(self):
        tab = self.create_sorttab("somefield")
        expected_link = "http://testserver/someurl?order_by={0}-desc&page=1".format(self.fieldname)
        self.assert_rendered_context_contains(tab,
                                              {"descending_link":
                                               expected_link},
                                              comp_func=compare_urls)

    def test_ascending_link_after_multiple_clicks(self):
        """Catch an issue where the query was being appended to the entire
        URL so for example, on the second time round of clicking the sort
        tab you would get something like
        http://blahblahserver/?order=field-asc&page=1&order=field-desc&pge=1
        """
        self.request = self.factory.get("/someurl?order_by={0}-asc&page=1".
                                        format(self.fieldname))
        tab = self.create_sorttab("somefield")
        expected_link = "http://testserver/someurl?order_by={0}-asc&page=1".format(self.fieldname)
        self.assert_rendered_context_contains(tab,
                                              {"ascending_link":expected_link},
                                              comp_func=compare_urls)

    def test_ascending_link_doesnt_clobber_other_get_params(self):
        self.request = self.factory.get("/someurl?someparam=somevalue")
        tab = self.create_sorttab("somefield")
        expected_link = "http://testserver/someurl?order_by={0}-asc&page=1&someparam=somevalue".format(self.fieldname)
        self.assert_rendered_context_contains(tab,
                                              {"ascending_link":expected_link},
                                              comp_func=compare_urls)

    def test_sorttab_display_name_in_renderer(self):
      tab = self.create_sorttab("somefield", display_name="threat")
      self.assert_rendered_context_contains(tab,
                                            {"display_name":"threat"})



