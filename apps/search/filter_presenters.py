from django.core.urlresolvers import reverse
import django.template
import django.template.loader
from main import utils
from marketplace.models import Category

class FilterPresenter(object):

    def __init__(self, fieldname, form, request,
                 friendly_value_calculator=None,
                 template="search/filter_field_include.html",
                 context={}):
        self.form_field = form[fieldname]
        self.fieldname = fieldname
        self.value = self.form_field.value()
        self.request = request
        self._friendly_val_func = friendly_value_calculator
        self.name = self.form_field.label
        self.template = django.template.loader.get_template(template)
        self.context = context

    @property
    def active(self):
        return not (self.value == "" or self.value is None)

    @property
    def disable_link(self):
        return utils.remove_get_param(self.request.build_absolute_uri(),
                                      self.fieldname)

    @property
    def friendly_value(self):
        if not self.active:
            return None
        if self._friendly_val_func:
            return self._friendly_val_func(self.value)
        return self.value

    def render(self):
        context_dict = {"filter_presenter": self,
                        "request": self.request}
        context_dict.update(self.context)
        context = django.template.Context(context_dict)
        return self.template.render(context)


class CategoryFilterPresenter(object):

    def __init__(self, category, field, request, disable_view='product_search'):
        self.name = "Category"
        self.category = category
        self.request = request
        self.disable_view = disable_view
        self.template = django.template.loader.get_template("search/category_filter_include.html")
        self.form_field = field

    @property
    def active(self):
        return self.category is not None

    @property
    def disable_link(self):
        return reverse(self.disable_view) + "?" + self.request.GET.urlencode()

    def render(self):
        context_dict = {
            "filter_presenter": self,
            "request": self.request,
            "active_category": self.category,
        }
        context = django.template.Context(context_dict)
        return self.template.render(context)
