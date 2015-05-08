import csv
import logging
import sys
from urllib import urlencode

from django.core.urlresolvers import reverse

from lxml import etree
from lxml.builder import E, ElementMaker

from main.utils import absolute_uri
from marketplace.models import Product, Country, CurrencyExchangeRate
from apps.marketplace.product_feed import XMLProductFeedBuilder, currency_convert, \
    XMLFeedWriter, NoCategoryMappingException, CategoryMapper, \
    COUNTRY_US, COUNTRY_GB, WORLDWIDE_SHIPPING_COUNTRIES, RATES

logger = logging.getLogger(__name__)

g = "http://base.google.com/ns/1.0"
nsmap = {"g": g, None: ""}
em = ElementMaker(namespace=g, nsmap=nsmap)
defaultem = ElementMaker(namespace="", nsmap=nsmap)


class TheFindProductFeedBuilder(XMLProductFeedBuilder):
    def generate(self):
        if len(self.product.images) == 0:
            return None
        item = defaultem.item(
            self.generate_id(),
            self.generate_title(),
            self.generate_description(),
            self.generate_link_with_utm_data(),
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
        self.exlucde_if_not_source_country()
        for image_link in self.generate_image_links():
            item.append(image_link)
        for shipping in self.generate_shipping():
            item.append(shipping)
        if self.exclude:
            return None
        return item

    def exlucde_if_not_source_country(self):
        if self.country.code != self.product.shipping_profile.shipping_country.code:
            self.exclude = True

    def generate_utm_data(self):
        pla = {
            "utm_source": "thefind",
            "utm_medium": "referral",
        }
        return urlencode(dict(pla))

    def generate_link_with_utm_data(self):
        uri = "{}?{}".format(self._generate_link(), self.generate_utm_data())
        link_str = "%s" % (uri,)
        return E.link(uri)

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


class TheFindFeedWriter(XMLFeedWriter):
    def get_builder(self, product):
        return TheFindProductFeedBuilder(self.currency, self.country, product,
                                     self.mapper)

def write_feed(currency, country_obj, fh):
    return TheFindFeedWriter(currency, country_obj).write(fh)