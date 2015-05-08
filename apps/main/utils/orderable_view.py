from django.views.generic import ListView
import django.template.loader
import urlparse
import urllib

from main.utils import add_get_params

class OrderableListView(ListView):

    def get_queryset_order(self):
        field, direction = self._get_field_and_direction()
        return self._translate_direction_to_field_prefix(direction) + field

    def get_order_by_param(self):
        if "order_by" not in self.request.REQUEST:
            raw_order = self.default_order
        else:
            raw_order = self.request.REQUEST['order_by']
        return raw_order

    def _translate_direction_to_field_prefix(self, direction):
        if direction == "desc":
            return "-"
        return ""

    def _get_field_and_direction(self):
        order_by_param = self.get_order_by_param()
        try:
            field, direction = order_by_param.split("-")
        except ValueError:
            field, direction = order_by_param, "asc"
        return field, direction

    def get_context_data(self, **kwargs):
        context = super(OrderableListView, self).get_context_data(**kwargs)
        context["order_by"] = self.get_order_by_param()
        self._populate_context_with_tabs(context)
        return context

    def get_queryset(self):
        queryset = super(OrderableListView, self).get_queryset()
        return queryset.order_by(self.get_queryset_order())

    def get_sort_tab(self, tab_fieldname, **kwargs):
        fieldname, direction = self._get_field_and_direction()
        if direction == "asc":
            return SortTab(tab_fieldname, fieldname, self.request, **kwargs)
        else:
            return SortTab(tab_fieldname, fieldname, self.request, ascending=False, **kwargs)

    def _populate_context_with_tabs(self, context):
        for tab_obj in self.tabs:
            if type(tab_obj) == str:
                context[tab_obj + "_tab"] = self.get_sort_tab(tab_obj)
            else:
                context[tab_obj.keys()[0] + "_tab"] = self.get_sort_tab(
                    tab_obj.keys()[0],
                    display_name = tab_obj.values()[0]
                )



class SortTab(object):

    def __init__(self, fieldname, order_by, request, ascending=True, display_name=None):
        self.fieldname = fieldname
        self.display_name = display_name
        self.order_by = order_by
        self.ascending = ascending
        self.request = request

    def render(self):
        t = django.template.loader.get_template(
            'main/includes/sortable-tab.html')
        context = self._get_context()
        result = t.render(context)
        return result

    def _get_context(self):
        context_dict = {
            "active": self.is_active(),
            "fieldname": self.fieldname,
        }
        if self.display_name:
            context_dict["display_name"] = self.display_name
        else:
            context_dict["display_name"] = self.fieldname
        if self.is_active():
            context_dict["ascending"] = self.ascending
        context_dict["ascending_link"] = self._get_sort_link("asc")
        context_dict["descending_link"] = self._get_sort_link("desc")
        return django.template.Context(context_dict)

    def is_active(self):
        return self.fieldname == self.order_by

    def _get_sort_link(self, direction):
        params = {
            "page": 1,
            "order_by": "{0}-{1}".format(self.fieldname, direction)
        }
        return add_get_params(self.request.build_absolute_uri(), params)
