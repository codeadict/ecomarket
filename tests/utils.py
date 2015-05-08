import django.template.loader
from django.test import TestCase
from operator import eq
import mock
import urlparse

class Matcher(object):
    """For use in mocking, allows comparison of objects via some
    arbitrary function called compare,

    see http://www.voidspace.org.uk/python/mock/examples.html#more-complex-argument-matching
    """
    def __init__(self, compare, some_obj):
        self.compare = compare
        self.some_obj = some_obj

    def __eq__(self, other):
        if self.compare(self.some_obj, other):
            return True
        raise AssertionError("{0} is not equal to {1}".format(
            self.some_obj, other))

def assert_in_dicts(dictionary, context, comp_func=eq):
    """Checks that all the key value pairs in dictionary are in a dictionary
    in context, which is a template context
    """
    for key, value in dictionary.items():
        if key not in context:
            raise AssertionError("Context does not contain key {0}".format(
                key))
        actual_value = context.get(key)
        if not comp_func(actual_value, value):
            raise AssertionError("Values for key '{0}' don't match, expected "
                                 "value was {1}, value in context was {2}".
                                 format(key, value, actual_value))
    return True

def make_dict_assert_func(comp_func):
    """Creates an assertion cuntions which compares values in two
    dictionaries using comp_func
    """
    def assert_func(dictionary, context):
        return assert_in_dicts(dictionary, context, comp_func=comp_func)
    return assert_func

def compare_urls(url1, url2):
    """Compares urls for equality without respect to the order of
    GET parameters
    """
    pr1 = urlparse.urlparse(url1)
    pr2 = urlparse.urlparse(url2)
    query1 = urlparse.parse_qs(pr1.query)
    query2 = urlparse.parse_qs(pr2.query)
    result = True
    for key in ["scheme", "netloc", "hostname", "port", "path"]:
        if getattr(pr1, key) != getattr(pr2, key):
            raise AssertionError("url {0} did not match {1}".format(url1, url2))
    if query1 != query2:
        raise AssertionError("GET parameters for {0} and {1} "
                             "did not match".format(url1, url2))
    return result


class RenderingObjectTestCase(TestCase):
    """View which has convenience methods for testing objects which have a
    render method which renders to a template
    """

    def assert_rendered_context_contains(self, obj, context, comp_func=eq):
        """Mocks the template loader so that we can access the arguments passed
        to the tempalte. The context is a normal python dictionary
        """
        matcher = Matcher(make_dict_assert_func(comp_func), context)
        with mock.patch.object(django.template.loader,'get_template') as mock_loader:
            mock_template = mock.Mock()
            mock_loader.return_value = mock_template
            obj.render()
            mock_loader.assert_called_with(self.template_name)
            mock_template.render.assert_called_with(matcher)

