from itertools import chain

from django import forms
from django_countries.countries import COUNTRIES
from haystack.query import SearchQuerySet, SQ

from marketplace.models import (
    Cause, Certificate, Color, Ingredient, Material, Keyword, Occasion,
    Category, Recipient, Product, Stall,
)


class NullableSearchForm(forms.Form):
    q = forms.CharField(required=False, label='Search')

    def __init__(self, *args, **kwargs):
        self.searchqueryset = kwargs.pop('searchqueryset', None)
        self.load_all = kwargs.pop('load_all', False)

        if self.searchqueryset is None:
            self.searchqueryset = SearchQuerySet()

        super(NullableSearchForm, self).__init__(*args, **kwargs)

    def search(self):
        if self.cleaned_data['q']:
            sqs = self.searchqueryset.auto_query(self.cleaned_data['q'])
        else:
            sqs = self.searchqueryset

        if self.load_all:
            sqs = sqs.load_all()

        return sqs

class CustomWeightedSearchQuery(object):
    def __init__(self, obj):
        self.obj = obj
    def __call__(self, *la, **kwa):
        return self.obj.__call__(*la, **kwa)

class ProductSearchForm(NullableSearchForm):

    """
    TODO: Rename fields to singular. Eg category
    """

    PRICE_RANGES = [
        ("0-10", "0-10"),
        ("10-20", "10-20"),
        ("20-30", "20-30"),
        ("30-50", "30-50"),
        ("50-100", "50-100"),
        ("100-150", "100-150"),
        ("150-200", "150-200"),
        ("200-1000", "200-1000"),
        ("1000-5000", "1000-5000"),
        ("5000-10000", "5000-10000"),
        ("10000-50000", "10000-50000"),
    ]

    category = forms.ChoiceField(required=False, choices=chain(
        [("", "")], Category.objects.values_list("id", "name")))
    causes = forms.ChoiceField(required=False, choices=Cause.objects.values_list('slug', 'title'))
    certificates = forms.ChoiceField(required=False, choices=Certificate.objects.values_list('slug', 'title'))
    colors = forms.ChoiceField(required=False, choices=Color.objects.values_list('slug', 'title'))
    price = forms.ChoiceField(required=False, choices=PRICE_RANGES)
    ships_to = forms.ChoiceField(required=False, choices=COUNTRIES)
    ships_from = forms.ChoiceField(required=False, choices=COUNTRIES)
    recipients = forms.ChoiceField(required=False, choices=Recipient.objects.values_list('slug', 'title'),
                                   label="For Who?")

    def __init__(self, category, data, request, *args, **kwargs):
        self.request = request
        if category is not None and "category" not in data:
            data["category"] = category.id
        super(ProductSearchForm, self).__init__(data, *args, **kwargs)
        self.product_category = category

        # choice fields
        for field_name in ['causes', 'certificates', 'colors', 'recipients',
                           'price', 'ships_to', 'ships_from']:
            # We do a special select2 widget for price dropdown with currency symbols
            if field_name != 'price':
                self.fields[field_name].widget.attrs.update({'class': "select"})
            choices = list(self.fields[field_name].choices)
            #choices.insert(0, ('', 'Select %s' % field_name) )  # add blank choice
            choices.insert(0, ('', '') )  # add blank choice
            self.fields[field_name].choices = choices

        self.fields["category"].widget.attrs.update({
            "class": "multiple-dropdown",
            "data-placeholder": "Categories",
        });

        self.fields['colors'].widget.attrs.update({ "class": "color-picker"})

        self.fields['price'].widget.attrs.update({'data-placeholder': "Price"})
        self.fields['causes'].widget.attrs.update({'data-placeholder': "Causes"})
        self.fields['colors'].widget.attrs.update({'data-placeholder': "Colour"})

        self.fields['ships_to'].widget.attrs.update({'data-placeholder': "Ships to"})
        self.fields['ships_from'].widget.attrs.update({'data-placeholder': "Ships from"})
        self.fields['recipients'].widget.attrs.update({'data-placeholder': "For who?"})

        self.fields['recipients'].widget.attrs.update({'data-search': "hide"})
        self.fields['causes'].widget.attrs.update({'data-search': "hide"})

    def clean_price(self, *args, **kwargs):
        price = self.cleaned_data['price']
        if price:
            low, high = price.split("-")
            try:
                low, high = int(low), int(high)
                return (low, high)
            except ValueError:
                pass
        return None, None

    def search(self):
        # First, store the SearchQuerySet received from other processing.
        if self.is_valid():
            sqs = super(ProductSearchForm, self).search()
            if self.product_category:
                sqs = sqs.filter(categories__contains=self.product_category.id)
            sqs = sqs.models(Product)
            sqs = self.filter_price(sqs)
            sqs = self.filter_cause(sqs)
            sqs = self.filter_color(sqs)
            sqs = self.filter_recipient(sqs)
            sqs = self.filter_ships_to(sqs)
            sqs = self.filter_ships_from(sqs)
        else:
            sqs = SearchQuerySet().models(Product).all()
        sqs = self.sort(sqs)
        sqs = sqs.filter(status=Product.PUBLISHED_LIVE)
        country = self.request.country
        sqs.query.backend.boost = ['ships_from:%s^4.0' % (country,),
                                   'ships_to:%s^7.0' % (country,),
                                   'ships_to:worldwide^6.99']
        return sqs

    def sort(self, sqs):
        sqs = sqs.order_by("-score")
        return sqs

    def filter_price(self, sqs):
        low, high = self.cleaned_data['price']
        if not(low==None or high==None):
            sqs = sqs.filter(price__gte=low).filter(price__lte=high)
        return sqs

    def filter_recipient(self, sqs):
        recipient = self.cleaned_data['recipients']
        if recipient:
            sqs = sqs.filter(recipients=recipient)
        return sqs

    def filter_ships_to(self, sqs):
        val = self.cleaned_data['ships_to']
        if val:
            sq = SQ()
            sq.add(SQ(ships_to__contains=val), SQ.OR)
            sq.add(SQ(ships_to='worldwide'), SQ.OR)
            sqs = sqs.filter(sq)
        return sqs

    def filter_ships_from(self, sqs):
        val = self.cleaned_data['ships_from']
        if val:
            sqs = sqs.filter(ships_from=val)
        return sqs

    def filter_cause(self, sqs):
        cause = self.cleaned_data['causes']
        if cause:
            sqs = sqs.filter(causes=cause)
        return sqs

    def filter_color(self, sqs):
        color = self.cleaned_data['colors']
        if color:
            color_id = Color.objects.get(slug=color).id
            sqs = sqs.filter(colors=color_id)
        return sqs
