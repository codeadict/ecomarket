from django.test import TestCase
from main.utils import remove_get_param
import mock
from search.filter_presenters import FilterPresenter
from tests import utils

class FilterPresenterTestCase(TestCase):

    def create_presenter(self, value="somevalue", request=None, friendly_value_calculator=None,
                         template=None):
        form = mock.MagicMock()
        mock_field = mock.MagicMock()
        mock_field.label = "Test Field"
        mock_field.value.return_value = value
        form.__getitem__.return_value = mock_field
        request = request or mock.Mock()
        if template is None:
            presenter = FilterPresenter("test_field", form, request,
                                        friendly_value_calculator=friendly_value_calculator)
        else:
            presenter = FilterPresenter("test_field", form, request,
                                        friendly_value_calculator=friendly_value_calculator,
                                        template=template)
        return presenter

    def test_active_if_fieldname_not_blank(self):
        presenter = self.create_presenter(value="somevalue")
        self.assertTrue(presenter.active)

    def test_disabled_if_fieldname_empty(self):
        presenter = self.create_presenter(value="")
        self.assertFalse(presenter.active)

    def test_disable_link_removes_get_parameter(self):
        mock_request = mock.Mock()
        mock_request.build_absolute_uri.return_value = \
            "http://testserver/?test_field=test_value&someotherfield=someothervalue"
        presenter = self.create_presenter(request=mock_request)
        expected_link = "http://testserver/?someotherfield=someothervalue"
        result = presenter.disable_link
        utils.compare_urls(expected_link, result)

    def test_friendly_value_calculator_used_for_friendly_value(self):
        presenter = self.create_presenter(
            friendly_value_calculator=lambda x: "it's {0}".format(x),
            value="blah",
        )
        self.assertEqual(presenter.friendly_value, "it's blah")

    def test_friendly_value_is_field_value_if_calc_not_specified(self):
        presenter = self.create_presenter(value="somevalue")
        self.assertEqual(presenter.friendly_value, "somevalue")

    def test_filter_presenter_renders_default_template(self):
        with mock.patch("django.template.loader.get_template") as mock_get_template:
            presenter = self.create_presenter()
            presenter.render()
            mock_get_template.assert_called_with("search/filter_field_include.html")

    def test_filter_presenter_renders_custom_template(self):
        with mock.patch("django.template.loader.get_template") as mock_get_template:
            presenter = self.create_presenter(template="sometemplatename")
            presenter.render()
            mock_get_template.assert_called_with("sometemplatename")
