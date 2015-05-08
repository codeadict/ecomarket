from django.core.urlresolvers import reverse
import django.template
from django.template.defaultfilters import capfirst

from marketplace.models import Category, Product
from articles.models import Article

register = django.template.Library()


def _breadcrumbs_from_categories(categories):
    previous_categories = []
    for category in categories:
        previous_categories.append(category.slug)
        url_name = "category_discover"
        yield reverse(url_name, args=previous_categories), category.name


def _breadcrumbs_from_category(category):
    categories = [category]
    while category.parent:
        categories.insert(0, category.parent)
        category = category.parent
    return _breadcrumbs_from_categories(categories)


def _breadcrumbs_from_product(product):
    categories = list(product.category_objs())
    for data in _breadcrumbs_from_categories(categories):
        yield data
    yield "", capfirst(product.title)


def _breadcrumbs_from_article(article):
    yield "/blog", "Blog"
    yield "", article.title


@register.inclusion_tag("marketplace/fragments/breadcrumb.html")
def generate_breadcrumb(thing):
    lookup = {Category: _breadcrumbs_from_category,
              Product: _breadcrumbs_from_product,
              Article: _breadcrumbs_from_article}
    if type(thing) not in lookup:
        raise django.template.TemplateSyntaxError(
            "Unrecognised object '%s'" % thing)
    return {
        "breadcrumbs":
            [(reverse("home"), "Eco Market")] + list(lookup[type(thing)](thing))
    }
