from collections import namedtuple
import django.template.loader
from main.utils import add_get_params

class DynamicPaginationMixin(object):
    """Implements a get_paginate_by method which uses request parameters to
    determine the number of items per page.

    The request parameter used is `paginate_by` and by default it is 10
    """

    def get_paginate_by(self, queryset):
        return self._get_paginate_by()

    def _get_paginate_by(self):
        """Paginate by method which does not refer to queryset"""
        if "paginate_by" in self.request.REQUEST:
            return int(self.request.REQUEST["paginate_by"])
        if getattr(self, "paginate_by"):
            return getattr(self, "paginate_by")
        return 10

    def get_context_data(self, *args, **kwargs):
        context = super(DynamicPaginationMixin, self).get_context_data(*args, **kwargs)
        context.update({
            "paginate_by_control": self._get_paginate_by_control()
        })
        return context

    def _get_paginate_by_control(self):
        allowed_options = [10, 50, 100]
        current_option = self._get_paginate_by()
        return PaginateByControl(current_option, allowed_options, self.request)


PaginateByOption = namedtuple('PaginatebyOption', 'value active')

class PaginateByControl(object):

    def __init__(self, current, allowed, request):
        self.current = current
        self.allowed = allowed
        self.request = request

    def render(self):
        template_name = "main/includes/paginate_by_control.html"
        template = django.template.loader.get_template(template_name)
        context = self._get_template_context()
        return template.render(context)

    def _get_template_context(self):
        context_dict = {
            "paginate_by_options": self._get_options(),
        }
        return django.template.Context(context_dict)

    def _get_options(self):
        options = []
        for option_value in self.allowed:
            if option_value == self.current:
                option = PaginateByOption(option_value, True, self.request)
            else:
                option = PaginateByOption(option_value, False, self.request)
            options.append(option)
        return options

class PaginateByOption(object):
    """Encapsulates a pagination object, including calculating the link to
    activate the option
    """

    def __init__(self, value, active, request):
        self.value = value
        self.active = active
        self.activate_url = self._get_activate_url(request)

    def _get_activate_url(self, request):
        params = {
            "paginate_by":self.value,
        }
        return add_get_params(request.build_absolute_uri(), params)

    def __eq__(self, other):
        return other.value == self.value \
                and other.active == self.active \
                and other.activate_url == self.activate_url

    def __hash__(self):
        return hash(self.value + self.active + self.activate_url)




