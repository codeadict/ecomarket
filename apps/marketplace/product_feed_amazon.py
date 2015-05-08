import csv
import logging
import sys

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

Exclude_Category = {
    'US': [
        'fashion',
        'food and drink',
        'tops and t-shirts',
        'baby cleaning accessories',
        'baby clothing',
    ]
}

Exclude_Product = [
    20078,
    14732,
    2044,
    2042,
    9168,
    14664,
    15758,
    15757,
    5994,
    5995,
    18563,
    18564,
    7655,
    14733,
    18734,
    11539,
    15419,
    11852,
    14175,
    18730,
    18733,
    19468,
    13476,
    20047,
    11179,
    11201,
    17464,
    12802,
    14158,
    14157,
    14155,
    11540,
    20165,
    18105,
    20164,
    14004,
    19370,
    16319,
    20078
]

Amazon_to_EcoMarket_Category_Map = {
    'baby and parenting': 'BABY_PRODUCT',
    'music players': 'AUDIO_OR_VIDEO',
    'speakers': 'SPEAKERS',
    'radios': 'RADIO',
    'batteries': 'BATTERY',
    'phones': 'PHONE_ACCESSORY',
    'chargers': 'POWER_SUPPLIES_OR_PROTECTION',
    'food': 'GOURMET_FOOD',
    'decor': 'HOME_FURNITURE_AND_DECOR',
    'home': 'HOME',
    'kitchen': 'KITCHEN',
    'seeds': 'SEEDS_AND_PLANTS',
    'outdoors': 'OUTDOOR_LIVING',
    'storage': 'HOME_ORGANIZERS_AND_STORAGE',
    'painting and decorating': 'TOOLS',
    'musical toys and instruments': 'INSTRUMENT_PARTS_AND_ACCESSORIES',
    'office accessories': 'OFFICE_PRODUCTS',
    'paper and notebooks': 'PAPER_PRODUCT',
    'writing pads and notebooks ': 'WRITING_INSTRUMENT',
    'school supplies': 'EDUCATIONAL_SUPPLIES',
    'toys and activities': 'TOYS_AND_GAMES',
}

class TSVProductFeedBuilder(XMLProductFeedBuilder):
    def _gen(self, name, value):
        return value

    def generate_title(self):
        title = self.product.title
        if title.upper() == title:
            title = title.title()
        return self._gen('title', title)

    def generate_link(self):
        if self.currency == 'USD':
            # In the case of US feeds we are using product URLs
            # which show product price in USD
            path = reverse('product_page_fixed_currency', kwargs={
                "stall_identifier": self.product.stall.identifier,
                "product_name": self.product.slug,
                "currency": self.currency,
            })
        else:
            path = reverse('product_page', kwargs={
                "stall_identifier": self.product.stall.identifier,
                "product_name": self.product.slug,
            })
        uri = absolute_uri(path)
        link_str = "%s" % (uri,)
        return self._gen('link', link_str)

    def generate_description(self):
        return self.product.description. \
            replace('\t', ' ').replace('\n\r', ' ').replace('\r\n', ' ').replace('\n', ' ').replace('\r', ' ')

    def generate_category(self):
        return self._gen('category', ' > '.join(self.product.categories))

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
        return self._gen('manufacturer', self.product.stall.title)

    def generate_age(self):
        ages = {
            'Men': 17,
            'Women': 17,
            'Unisex Adults': 17,
            'Teen Boys': 13,
            'Teen Girls': 13,
            'Teens': 13,
            'Boys': 4,
            'Girls': 4,
            'Children': 4,
            'Baby Boys': 0,
            'Baby Girls': 0,
            'Babies': 0,
        }
        age = 99
        if self.product.recipients:
            for r in self.product.recipients.all():
                if str(r) in ages and ages[str(r)] < age:
                    age = ages[str(r)]
        return self._gen('age', age)

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

    def exclude_category(self):
        if self.country.code not in Exclude_Category:
            return
        exlcude_list = Exclude_Category[self.country.code]
        cat = self.product.primary_category
        while cat:
            if str(cat.name).lower() in exlcude_list:
                self.exclude = True
                break
            cat = cat.parent

    def exclude_product(self):
        if self.product.id in Exclude_Product:
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
        if self.country.code == 'GB':
            self.exlucde_if_not_source_country()
            self.exclude_if_not_sold()
            self.check_shipping()
            self.exclude_category()
            self.exclude_product()
            if self.exclude:
                return None
            item = list([
                self.generate_product_type(),
                self.generate_title(),
                self.generate_link(),
                self.generate_id(), # SKU
                self.generate_price(),
                self.generate_brand(),
                self.generate_image(),
                self.generate_description(),
                self.generate_manufacturer(),
                self.generate_age(),
                self.generate_color(),
                self.generate_gender()
            ])
            # We double check here if one of the functions above excluded the product
            if self.exclude:
                return None
            return item
        elif self.country.code == 'US':
            self.exlucde_if_not_source_country()
            self.exclude_if_not_sold()
            self.check_shipping()
            self.exclude_category()
            self.exclude_product()
            if self.exclude:
                return None
            item = list([
                self.generate_category(),
                self.generate_title(),
                self.generate_link(),
                self.generate_id(), # SKU
                self.generate_price(),
                self.generate_brand(),
                self.generate_image(),
                self.generate_description(),
                self.generate_manufacturer(),
                self.generate_age(),
                self.generate_color(),
                self.generate_gender()
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
        if self.country.code == 'GB':
            tsvh.writerow(['Product Type', 'Title', 'Link', 'SKU', 'Price',
                'Brand', 'Image', 'Description',
                'Manufacturer', 'Age', 'Color', 'Gender'])
        elif self.country.code == 'US':
            tsvh.writerow(['Category', 'Title', 'Link', 'SKU', 'Price',
                'Brand', 'Image', 'Description',
                'Manufacturer', 'Age', 'Color', 'Gender'])
        for item in self.generate_data():
            ascii_item = [removeNonAscii(v)[0:1800] for v in item]
            tsvh.writerow(ascii_item)


def write_feed(currency, country_obj, fh):
    return TSVFeedWriter(currency, country_obj).write(fh)