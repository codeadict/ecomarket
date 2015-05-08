from functools import partial
from urllib import urlencode

from django.db.models import Q, F
from django.conf import settings
from django.core.paginator import Paginator, Page, EmptyPage
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, render

from django.contrib import messages
from django.utils import simplejson
from django.utils.datastructures import SortedDict

from haystack.views import SearchView
from haystack.forms import ModelSearchForm, SearchForm

from marketplace.models import Category, Cause, Color, Recipient, Product
from django.db.models.query import QuerySet

from search.filter_presenters import FilterPresenter, CategoryFilterPresenter

PRODUCT_NOT_FOUND_ERROR = ('Sorry, it seems this product was not found or is '
                           'no longer published on Eco Market. Fear not, we '
                           'have plenty more where that came from!')
RESULTS_PER_PAGE = getattr(settings, "PAGINATION_DEFAULT_PAGINATION", 20)


def _get_category_parent_slugs(category):
    parents = []
    while category.parent is not None:
        parents.insert(0, category.parent.slug)
        category = category.parent
    return parents

def category_discover(request, category=None):
    template_name = "search/category_discover.html"
    if category is None:
        category = Category(name="Discover", slug="discover")
    else:
        category = get_object_or_404(Category, slug=category)

    # Do a 301-redirect for SEO purposes
    parents = _get_category_parent_slugs(category)
    if len(parents) > 0:
        url = reverse("category_discover", args=parents + [category.slug])
        if len(request.GET):
            url = "%s?%s" % (url, request.GET.urlencode())
        return HttpResponseRedirect(url)

    if category.id is None:
        subcategories = Category.objects
        search_terms = ""
    else:
        subcategories = category.get_descendants()
        search_terms = category.get_slug_path()


    # Show only categories with products in stock
    #
    # doing exclude(products=None) doesn't work because it'll still include
    # categories which only have out of stock products.
    # But you can't do exclude(products=None, products__stock=0) or any combination
    # like that because the Django ORM ... basically can't do the query like that
    # because the `product.stock != 0` needs to be a JOIN condition, then 
    # `product.id IS NULL` as a WHERE condition, but Django puts both as WHERE
    # conditions.
    empty_categories = [cat.pk for cat in Category.objects.raw("""
SELECT c.id, c.parent_id, c.tree_id, c.name FROM marketplace_category c
  LEFT JOIN marketplace_product p ON(p.primary_category_id = c.id AND p.stock != 0)
 WHERE p.id IS NULL
 GROUP BY c.id
 """)]    
    subcategories = (subcategories.exclude(slug__contains="adult")                                  
                                  .order_by('-products__number_of_recent_sales',
                                            '-products__number_of_sales'))
    
    subcat_query = subcategories.query
    subcat_query.group_by = ['id']
    subcategories = QuerySet(model=Category, query=subcat_query)
    subcategories = subcategories.exclude(pk__in=empty_categories)
    subcategories = subcategories[:16]

    context = {
        "category": category,
        "subcategories": subcategories,
        "search_terms": search_terms,
        'ecomm_pagetype': 'category',
    }

    if category.id is not None:
        context['ecomm_category'] = category.name

    return render(request, template_name, context)

class ProductSearchView(SearchView):

    template = "search/search.html"
    results_per_page = RESULTS_PER_PAGE

    def __init__(self, *args, **kwargs):
        self.as_discover = kwargs.pop("as_discover", False)
        super(ProductSearchView, self).__init__(*args, **kwargs)

    def _get_categories(self, category_slugs):
        categories = Category.objects.get_toplevel()
        for category_slug in category_slugs:
            category = get_object_or_404(categories, slug=category_slug)
            yield category
            categories = category.children

    def _get_category(self):
        if len(self.categories) > 0:
            return self.categories[-1]
        return None

    def __call__(self, request, *categories):
        if "category" in request.GET:
            if request.GET["category"] == "none":
                return self._get_no_cat_redirect(request)
            else:
                return self._get_category_redirect(request)
        self.categories = list(self._get_categories(categories))
        
        self.request = request
        self.form = self.build_form({'request':request})
        self.query = self.get_query()
        self.results = self.get_results()
        return self.create_response()

    def _get_no_category_redirect(self, request):
        querydict = request.GET.copy()
        del querydict["category"]
        url = reverse("product_search") + "?" + querydict.urlencode()
        return HttpResponseRedirect(url)

    def _get_category_redirect(self, request):
        category = get_object_or_404(Category, id=request.GET["category"])
        querydict = request.GET.copy()
        del querydict["category"]
        url = category.get_search_url() + "?" + querydict.urlencode()
        return HttpResponseRedirect(url)

    def build_form(self, form_kwargs=None):
        """
        Instantiates the form the class should use to process the search query.
        """
        data = None
        kwargs = {
            'load_all': self.load_all,
        }
        if form_kwargs:
            kwargs.update(form_kwargs)

        data = {}
        if len(self.request.GET):
            data = self.request.GET.copy()

        if self.searchqueryset is not None:
            kwargs['searchqueryset'] = self.searchqueryset

        return self.form_class(self._get_category(), data, **kwargs)

    def build_page(self):
        """For some reason occasionally the default pagination contains Nones
        (probably a bug in django-haystack. We don't want that."""
        # Copied from super()
        try:
            page_no = int(self.request.GET.get('page', 1))
        except (TypeError, ValueError):
            raise Http404("Not a valid number for page.")

        if page_no < 1:
            raise Http404("Pages should be 1 or greater.")

        start_offset = (page_no - 1) * self.results_per_page
        self.results = self.results.load_all() # Force haystack to pull all 'Product' objects at the same time
        self.results[start_offset:start_offset + self.results_per_page]

        paginator = Paginator(self.results, self.results_per_page)

        # My stuff
        try:
            page = paginator.page(page_no)
        except EmptyPage:
            page = Page([], page_no, paginator)
        page.object_list = [o for o in page.object_list if o is not None]
        return paginator, page

    def extra_context(self):
        def compose_json_autocomplete_for(model):
            return simplejson.dumps(
                [i['title'] for i in model.objects.values('title')])

        page_no = int(self.request.GET.get('page', 1))
        product_notfound = self.request.GET.get('product') == 'notfound'
        if product_notfound:
            messages.error(self.request, PRODUCT_NOT_FOUND_ERROR)

        res = {
            'page_no': page_no,
            'ecomm_pagetype': 'searchresults'
        }

        res["filter_presenters"] = self._get_filter_presenters(self.form)
        res["category"] = self._get_category()
        res["as_discover"] = self.as_discover
        if res["category"] is None:
            search_terms = ""
        else:
            search_terms = res["category"].get_slug_path()
        relevant_data = SortedDict()
        for key in ["q", "recipients", "causes", "colors", "page"]:
            if key in self.request.GET:
                relevant_data[key] = self.request.GET[key].encode("utf-8")
        if len(relevant_data):
            search_terms += "?" + urlencode(relevant_data)
        res["search_terms"] = search_terms
        if "causes" in self.request.GET:
            try:
                cause = Cause.objects.get(slug=self.request.GET["causes"])
                res["cause"] = cause
            except Cause.DoesNotExist:
                pass

        return res

    def _get_filter_presenters(self, form):
        presenters = []
        friendly_names = {
            'causes': lambda val: Cause.objects.get(slug=val),
            'price': lambda val: "{0}-{1}".format(val),
            'ships_to': lambda val: "To: {0}".format(val),
            'ships_from': lambda val: "To: {0}".format(val),
            'recipients': lambda val: Recipient.objects.get(slug=val),
        }
        for fieldname, friendly_value_func in friendly_names.items():
            presenters.append(FilterPresenter(
                fieldname,
                form,
                self.request,
                friendly_value_calculator=friendly_value_func
            ))
        presenters.append(FilterPresenter(
            "colors",
            form,
            self.request,
            friendly_value_calculator=lambda val: Color.objects.get(slug=val),
            template="search/color_filter_include.html"
        ))
        if not self.as_discover:
            presenters.insert(0, CategoryFilterPresenter(
                self._get_category(),
                form["category"],
                self.request,
            ))
        return presenters
