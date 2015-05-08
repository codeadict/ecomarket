import csv
import logging
import sys
from urllib import urlencode

from django.core.urlresolvers import reverse

from main.utils import absolute_uri
from apps.purchase.models import LineItem
from apps.marketplace.product_feed import XMLProductFeedBuilder, XMLFeedWriter, currency_convert, \
    COUNTRY_US, COUNTRY_GB


def removeNonAscii(s):
    if isinstance(s, basestring):
        return "".join(i for i in s if ord(i)<128)
    else:
        return str(s)

class TSVProductFeedBuilder(XMLProductFeedBuilder):
    def _gen(self, name, value):
        return value

    def generate_category(self):
        return self._gen('category', ' > '.join(self.product.categories))

    def generate_title(self):
        title = self.product.title
        if title.upper() == title:
            title = title.title()
        return self._gen('title', title[0:80])

    def generate_link(self):
        path = reverse('product_page', kwargs={
            "stall_identifier": self.product.stall.identifier,
            "product_name": self.product.slug,
        })
        uri = absolute_uri(path)
        link_str = "%s" % (uri,)
        utm_data = {
            "utm_source": "become",
            "utm_medium": "cpc",
        }
        return "%s?%s" % (self._gen('link', link_str), urlencode(dict(utm_data)))

    def generate_description(self):
        return self.product.description.replace('\t', ' ').replace('\n\r', ' ').replace('\n', ' ').replace('\r', ' ')

    def generate_product_type(self):
        cat = self.product.primary_category
        while cat:
            if str(cat.name).lower() in Amazon_to_EcoMarket_Category_Map:
                return self._gen('product_type', Amazon_to_EcoMarket_Category_Map[str(cat.name).lower()])
            cat = cat.parent
        self.exclude = True

    def generate_price(self):
        price_obj = self.product.get_price_instance().amount
        native_price = currency_convert(float(price_obj.amount), self.currency, price_obj.currency)
        return self._gen("price", native_price)

    def generate_image(self):
        first = True
        image = self.product.images[0]
        return self._gen("image", absolute_uri(image.url))

    def generate_manufacturer(self):
        return self._gen('manufacturer', self.product.stall.title.title())

    def generate_condition(self):
        return self._gen('conditio', 'New')

    def generate_nothing(self):
        return self._gen('nothing', '')

    def check_shipping(self):
        shipping_profile = self.product.shipping_profile
        country_label = 'ships_to_%s' % (self.country.code,)

        label_names = {}
        if shipping_profile.ships_worldwide():
            label_names['ships_worldwide'] = True
        else:
            if shipping_profile.ships_to_country(COUNTRY_US):
                label_names['ships_to_US'] = True
            elif shipping_profile.ships_to_country(COUNTRY_GB):
                label_names['ships_to_GB'] = True
            elif shipping_profile.ships_to_country(self.country):
                label_names[country_label] = True

        if self.country is not None:
            if country_label not in label_names and not shipping_profile.ships_worldwide():
                self.exclude = True

    def exclude_if_not_sold(self):
        # Another case of Ebay feed optimization.
        # If a product has not sold at least 3 times, it is removed
        li = LineItem.objects.filter(product=self.product).count()
        if li < 1:
            self.exclude = True

    def exlucde_if_not_source_country(self):
        if self.country.code != self.product.shipping_profile.shipping_country.code:
            self.exclude = True

    def generate(self):
        if len(self.product.images) == 0:
            return None
        if self.country.code == 'US':
            self.exlucde_if_not_source_country()
            self.exclude_if_not_sold()
            self.check_shipping()
            if self.exclude:
                return None
            item = list([
                self.generate_manufacturer(),
                self.generate_id(), # Mfr Part #
                self.generate_link(),
                self.generate_title(),
                self.generate_price(),
                self.generate_description(),
                self.generate_category(),
                self.generate_image(),
                self.generate_condition(),
            ])
            # We double check here if one of the functions above excluded the product
            if self.exclude:
                return None
            return item


class TSVFeedWriter(XMLFeedWriter):
    def get_builder(self, product):
        return TSVProductFeedBuilder(self.currency, self.country, product, self.mapper)

    def write(self, fh):
        tsvh = csv.writer(fh, dialect='excel-tab')
        if self.country.code == 'US':
            tsvh.writerow(['Manufacturer', 'Mfr Part #', 'Product URL', 'Product Title', 'Price',
                'Product Description', 'Category', 'Image URL', 'Condition'])
        for item in self.generate_data():
            ascii_item = [removeNonAscii(v)[0:250] for v in item]
            tsvh.writerow(ascii_item)


def write_feed(currency, country_obj, fh):
    return TSVFeedWriter(currency, country_obj).write(fh)