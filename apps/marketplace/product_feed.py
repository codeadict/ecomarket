import csv
import logging
import sys
from urllib import urlencode

from django.core.urlresolvers import reverse

from lxml import etree
from lxml.builder import E, ElementMaker

from main.utils import absolute_uri
from marketplace.models import Product, Country, CurrencyExchangeRate

logger = logging.getLogger(__name__)

g = "http://base.google.com/ns/1.0"
nsmap = {"g": g, None: ""}
em = ElementMaker(namespace=g, nsmap=nsmap)
defaultem = ElementMaker(namespace="", nsmap=nsmap)

# When a shipping profile specifies that the product ships worldwide we need
# to specify the top 100 countries (by number of internet users).
# This is because Google doesn't allow us to specify 'ships worldwide', and we
# must specify individual countries, but restricts us to 100.
# http://www.indexmundi.com/g/r.aspx?t=100&v=118
WORLDWIDE_SHIPPING_COUNTRIES = (
    'CN', 'US', 'JP', 'BR', 'DE', 'IN', 'GB', 'FR', 'NG', 'RU', 'KR', 'MX',
    'IT', 'ES', 'TR', 'CA', 'VN', 'CO', 'PL', 'PK', 'EG', 'ID', 'TH', 'TW',
    'AU', 'MY', 'NL', 'AR', 'MA', 'SA', 'PE', 'VE', 'SE', 'PH', 'IR', 'BE',
    'RO', 'UA', 'CL', 'CZ', 'HU', 'CH', 'AT', 'KZ', 'PT', 'GR', 'HK', 'DK',
    'DZ', 'UZ', 'IL', 'SY', 'NO', 'ZA', 'SD', 'RS', 'SK', 'KE', 'TN', 'AE',
    'NZ', 'BG', 'EC', 'SG', 'UG', 'IE', 'DO', 'BY', 'AZ', 'YE', 'GT', 'HR',
    'KG', 'LT', 'SN', 'LK', 'JO', 'JM', 'LV', 'CR', 'OM', 'ZW', 'BA', 'UY',
    'MD', 'AL', 'GE', 'SI', 'GH', 'PY', 'BO', 'KW', 'MK', 'HT', 'AF', 'LB',
    'PR', 'EE', 'CI'
)

COUNTRY_GB = Country.objects.get(code='GB')
COUNTRY_US = Country.objects.get(code='US')

RATES = CurrencyExchangeRate.get_all_rates()


def currency_convert(amount, to_currency, from_currency='GBP'):
    if str(to_currency) == str(from_currency):
        return amount
    return round((RATES[to_currency] * amount), 2)


class NoCategoryMappingException(Exception):
    pass


class XMLProductFeedBuilder(object):
    def __init__(self, currency, country, product, mapper):
        self.product = product
        self.currency = currency
        self.country = country
        self.exclude = False
        self.mapper = mapper

    def generate_condition(self):
        return self._gen("condition", "new")

    def generate_price(self):
        price_obj = self.product.get_price_instance().amount
        native_price = currency_convert(float(price_obj.amount), self.currency,
                                        price_obj.currency)
        return self._gen("price", "{0} {1}".format(
            native_price, self.currency))

    def generate_availability(self):
        return self._gen("availability", ("in stock" if self.product.in_stock()
                                          else "out of stock"))

    def generate_identifier_exists(self):
        return self._gen('identifier_exists', 'FALSE')

    def generate_category(self):
        google_category = self.mapper.get_category(self.product).strip('"')
        return self._gen("google_product_category", google_category)

    def generate_product_type(self):
        product_type = " > ".join(self.product.categories)
        return self._gen("product_type", product_type)

    def generate_id(self):
        return self._gen("id", str(self.product.id))

    def generate_size(self):
        return self._gen('size', 'M')

    def generate_brand(self):
        return self._gen('brand', self.product.stall.title)

    def generate(self):
        if len(self.product.images) == 0:
            return None
        item = defaultem.item(
            self.generate_id(),
            self.generate_title(),
            self.generate_description(),
            self.generate_link(),
            self.generate_condition(),
            self.generate_price(),
            self.generate_availability(),
            self.generate_category(),
            self.generate_product_type(),
            self.generate_identifier_exists(),
            self.generate_gender(),
            self.generate_age_group(),
            self.generate_size(),
            self.generate_brand(),
            self.generate_color(),
        )
        for label in self.generate_adwords_labels():
            item.append(label)
        for image_link in self.generate_image_links():
            item.append(image_link)
        for shipping in self.generate_shipping():
            item.append(shipping)
        if self.exclude:
            return None
        return item

    def generate_title(self):
        title = self.product.title
        if title.upper() == title:
            title = title.title()
        return E.title(title)

    def generate_description(self):
        return E.description(self.product.description)

    def _generate_link(self):
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
        return absolute_uri(path)

    def generate_link(self):
        url = str(self._generate_link())
        utm_data = {
            "em_source": "google",
            "em_medium": "cpc",
            "em_campaign": "PLA - %s" % self.product.category_tree,
        }
        url = "%s?%s" % (url, urlencode(dict(utm_data)))
        return E.link(url)

    def _gen(self, name, value):
        return getattr(em, name)(value)

    def generate_image_links(self):
        first = True
        for image in self.product.images[:10]:
            if first:
                first = False
                yield self._gen("image_link", absolute_uri(image.url))
            else:
                yield self._gen("additional_image_link",
                                absolute_uri(image.url))

    def generate_adwords_labels(self):
        prod = self.product

        bands = [(a, a + 9.99) for a in range(0, 100, 10)] + [
                 (a, a + 19.99) for a in range(100, 200, 20)]

        label_names = {}
        for price in prod.prices.all():
            native_price = currency_convert(float(price.amount.amount),
                                            self.currency)
            if native_price >= 200:
                label_names['over_200_' + self.currency] = True
                break
            # TODO: easier to do price > 200 ... price % 20 etc.?
            for band in bands:
                if native_price <= band[1] and native_price >= band[0]:
                    label_name = '%d_to_%.2f_%s' % (band[0], band[1],
                                                    self.currency)
                    label_names[label_name] = True
                    break

        toplevel_category = self.product.primary_category
        while toplevel_category.parent:
            toplevel_category = toplevel_category.parent
        label_names[toplevel_category.name.replace(' ', '_')] = True

        shipping_profile = self.product.shipping_profile
        key = '%s_seller' % (shipping_profile.shipping_country.code,)
        label_names[key] = True

        country_label = 'ships_to_%s' % (self.country.code,)

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
            if (country_label not in label_names
                    and not shipping_profile.ships_worldwide()):
                self.exclude = True

        # trello.627 - tag faith in nature for adwords
        if 'faith in nature' in prod.title.lower():
            label_names['brand.faith_in_nature'] = True

        return [em.adwords_labels(label_name) for label_name in label_names]

    def generate_shipping(self):
        shippings = []
        shipping_profile = self.product.shipping_profile
        shipping_rules = shipping_profile.shipping_rules.all()
        ships_to_countries = {}
        for shipping_rule in shipping_rules:
            for country in shipping_rule.countries.all():
                if len(ships_to_countries.keys()) >= 100:
                    break
                if country.code in ships_to_countries:
                    continue
                ships_to_countries[country.code] = True
                # Free shipping is a special discount we run sometimes
                # if self.product.has_free_shipping(country):
                #     native_price = 0
                # else:
                native_price = currency_convert(
                    float(shipping_rule.rule_price.amount), self.currency,
                    shipping_rule.rule_price.currency)
                price_str = "{0} {1}".format(native_price,
                                             self.currency)
                shipping = em.shipping(
                    em.country(country.code),
                    em.price(price_str)
                )
                shippings.append(shipping)
        # When it ships to the rest of the world, output at most 100 of the top
        # internet using countries.
        if shipping_profile.ships_worldwide():
            for country in WORLDWIDE_SHIPPING_COUNTRIES:
                country_obj = Country.objects.get(code=country)
                if country in ships_to_countries:
                    continue
                if len(ships_to_countries.keys()) >= 100:
                    break
                ships_to_countries[country] = True
                # Free shipping is a special discount we run sometimes
                # if self.product.has_free_shipping(country_obj):
                #     native_price = 0
                # else:
                native_price = currency_convert(
                        float(shipping_profile.others_price.amount),
                        self.currency, shipping_profile.others_price.currency)
                price_str = "{0} {1}".format(native_price,
                                             self.currency)
                shipping = em.shipping(
                    em.country(country),
                    em.price(price_str)
                )
                shippings.append(shipping)
        return shippings

    def _get_gender_groups(self):
        return {
            'Everyone': 'unisex',
            'Men': 'men',
            'Women': 'women',
            'Unisex Adults': 'unisex',
            'Teen Boys': 'men',
            'Teen Girls': 'women',
            'Teens': 'unisex',
            'Boys': 'men',
            'Girls': 'women',
            'Children': 'unisex',
            'Baby Boys': 'men',
            'Baby Girls': 'women',
            'Babies': 'unisex',
            'Birds': 'unisex',
            'Dogs': 'unisex',
            'Cats': 'unisex',
            'Animals and Insects': 'unisex',
            'All People': 'unisex'
        }

    def generate_gender(self):
        gender_groups = self._get_gender_groups()
        gender = 'unisex'
        if self.product.recipients:
            for r in self.product.recipients.all():
                if gender_groups[str(r)] == 'unisex':
                    gender = 'unisex'
                    break
                else:
                    gender = gender_groups[str(r)]
        return self._gen('gender', gender)

    def generate_age_group(self):
        age_groups = {
            'Everyone': 'adult',
            'Men': 'adult',
            'Women': 'adult',
            'Unisex Adults': 'adult',
            'Teen Boys': 'adult',
            'Teen Girls': 'adult',
            'Teens': 'adult',
            'Boys': 'adult',
            'Girls': 'adult',
            'Children': 'kids',
            'Baby Boys': 'kids',
            'Baby Girls': 'kids',
            'Babies': 'kids',
            'Birds': 'adult',
            'Dogs': 'adult',
            'Cats': 'adult',
            'Animals and Insects': 'adult',
            'All People': 'adult'
        }
        age_group = 'adult'
        if self.product.recipients:
            for r in self.product.recipients.all():
                if age_groups[str(r)] == 'adult':
                    age_group = 'adult'
                    break
                else:
                    age_group = age_groups[str(r)]
        return self._gen('age_group', age_group)

    def generate_color(self):
        all_colors = [cl.title for cl in self.product.colors.all()[:3]]
        return self._gen('color', '/'.join(all_colors))


class CategoryMapper(object):

    def __init__(self, map_filename):
        self.map_filename = map_filename
        self.category_map = {}
        self._read_map_file()

    def _read_map_file(self):
        with open(self.map_filename) as mapfile:
            rows = csv.reader(mapfile)
            for row in rows:
                key = ''.join([cat_name.lower() for cat_name in row[:4]])
                google_category = row[4]
                self.category_map[key] = google_category

    def get_category(self, product):
        key = ''.join([cat.lower() for cat in product.categories])
        try:
            return self.category_map[key]
        except KeyError:
            raise NoCategoryMappingException(
                "No category found in map file for categories {0}".format(
                    list(product.categories)))


class XMLFeedWriter(object):

    xmlns_str = 'xmlns:g="http://base.google.com/ns/1.0" xmlns=""'

    @property
    def mapper(self):
        if self._mapper is None:
            self._mapper = CategoryMapper("prod_cats.csv")
        return self._mapper

    def get_products(self):
        return (Product.objects
                    .live()
                    .select_related('shipping_profile', 'stall')
                    .prefetch_related('categories')
                    .order_by("id"))

    def products_iterator(self):
        return self.get_products().iterator()

    def generate_data(self):
        unavailable_mapping_ids = []
        _count = 0
        _count_skipped = 0
        for product in self.products_iterator():
            _count = _count + 1
            if _count % 100 == 0:
                logger.debug('Processed %s products, skipped %s, generated %s' % (_count, _count_skipped, (_count - _count_skipped)))
            sys.stdout.flush()
            try:
                data = self.get_builder(product).generate()
                if data is None:
                    _count_skipped = _count_skipped + 1
                    continue
                yield data
            except ValueError:
                pass
            except NoCategoryMappingException as ex:
                logger.warn(ex.message)
                unavailable_mapping_ids.append(product.id)
        logger.debug("Feed generated")
        logger.warn("There were no mappings available for {0} products".format(
            len(unavailable_mapping_ids)))
        logger.warn("Unavailable product ids were {0}".format(
            unavailable_mapping_ids))

    def __init__(self, currency, country):
        self._mapper = None
        self.currency = currency
        self.country = country

    def get_builder(self, product):
        return XMLProductFeedBuilder(self.currency, self.country, product,
                                     self.mapper)

    def write(self, fh):
        fh.write('<?xml version="1.0" encoding="UTF-8" ?>\n')
        fh.write("<rss version=\"2.0\" %s>\n\t<channel>\n" % (self.xmlns_str,))
        for item in self.generate_data():
            try:
                fh.write(etree.tostring(item, pretty_print=True).replace(
                    self.xmlns_str, ''))
            except ValueError:
                pass
        fh.write("\t</channel>\n</rss>\n")


def write_feed(currency, country_obj, fh):
    return XMLFeedWriter(currency, country_obj).write(fh)
