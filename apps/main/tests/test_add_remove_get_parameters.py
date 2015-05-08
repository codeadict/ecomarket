from django.test import TestCase
from tests.utils import compare_urls
from main.utils import add_get_params, remove_get_param

class AddGetParameterTestCase(TestCase):

    def setUp(self):
        self.initial_url = "http://testserver/?param1=value"

    def test_add_get_leaves_existing_parameters_untouched(self):
        expected_url = "http://testserver/?param1=value&param2=value2"
        new_url = add_get_params(self.initial_url, {"param2":"value2"})
        self.assertTrue(compare_urls(expected_url, new_url))

    def test_add_multiple_parameters(self):
        expected_url = "http://testserver/?param1=value&param2=value2&param3=value3"
        new_url = add_get_params(self.initial_url, {"param2":"value2", "param3":"value3"})
        self.assertTrue(compare_urls(expected_url, new_url))

    def test_overwrite_existing_param(self):
        expected_url = "http://testserver/?param1=newvalue"
        new_url = add_get_params(self.initial_url, {"param1":"newvalue"})
        self.assertTrue(compare_urls(expected_url, new_url))


class RemoveGetParameterTestCase(TestCase):

    def test_remove_get_parameter_leaves_other_parameters(self):
        initial_url = "http://testserver/?param1=value1&param2=value2"
        expected_url = "http://testserver/?param2=value2"
        new_url = remove_get_param(expected_url, "param1")
        self.assertTrue(compare_urls(expected_url, new_url))

    def test_removes_mulitple_instances_of_params(self):
        initial_url = "http://testserver/?param1=value1&param2=value2&param1=value2"
        expected_url = "http://testserver/?param2=value2"
        new_url = remove_get_param(expected_url, "param1")
        self.assertTrue(compare_urls(expected_url, new_url))


