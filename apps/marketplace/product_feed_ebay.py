from lxml.builder import E, ElementMaker
from urllib import urlencode

from django.db.models import Q

from main.utils import absolute_uri
from apps.purchase.models import LineItem
from marketplace.product_feed import XMLProductFeedBuilder, XMLFeedWriter, currency_convert, \
    COUNTRY_US, COUNTRY_GB

em = ElementMaker(namespace="")


class EbayXMLProductFeedBuilder(XMLProductFeedBuilder):

    def __init__(self, *args):
        return super(EbayXMLProductFeedBuilder, self).__init__(*args,
                                                               mapper=None)
    def _gen(self, name, value):
        return getattr(em, name)(value)

    def _find_shipping_rule(self):
        shipping_profile = self.product.shipping_profile
        try:
            # Find this country
            return shipping_profile.shipping_rules.filter(
                    countries=self.country)[0]
        except IndexError:
            # Find 'rest of world'
            assert shipping_profile.ships_worldwide(), self.product

    def generate_shipping(self):
        rule = self._find_shipping_rule()
        if rule:
            price = rule.rule_price
        else:
            price = self.product.shipping_profile.others_price
        native_price = currency_convert(float(price.amount), self.currency,
                                        price.currency)
        price_str = "{} {}".format(native_price, self.currency)
        return em.shipping(price_str)

    def generate_category(self):
        return self._gen("Category", " > ".join(self.product.categories))

    def generate_condition(self):
        # This is always 'new' - eBay reject anything else
        return self._gen("Condition", "New")

    def generate_top_seller_rank(self):
        return self._gen("Top_Seller_Rank",
                         str(self.product.ebay_top_seller_rank))

    def generate_shipping_estimate(self):
        rule = self._find_shipping_rule()
        if rule:
            minimum, maximum = rule.delivery_time, rule.delivery_time_max
        else:
            sp = self.product.shipping_profile
            minimum = sp.others_delivery_time
            maximum = sp.others_delivery_time_max
        value = "Between {} and {} days".format(minimum, maximum)
        return self._gen("shipping_estimate", value)

    def _get_gender_groups(self):
        gender_groups = \
            super(EbayXMLProductFeedBuilder, self)._get_gender_groups()
        gender_groups.update({
            "Teen Boys": "boys",
            "Teen Girls": "girls",
            "Boys": "boys",
            "Girls": "girls",
            "Baby Boys": "infants and toddlers",
            "Baby Girls": "infants and toddlers",
            "Babies": "infants and toddlers",
        })
        return gender_groups

    def generate_material(self):
        all_materials = [cl.title for cl in self.product.materials.all()[:3]]
        return self._gen('material', ', '.join(all_materials))

    def generate_availability(self):
        # Ebay feed is very optimized, we remove products if they are not in stock
        if not self.product.in_stock():
            self.exclude = True
        return self._gen("Stock_Availability", "Y")

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

    def generate_link(self):
        url = str(self._generate_link())
        utm_data = {
            "utm_source": "ebay",
            "utm_medium": "cpc",
        }
        url = "%s?%s" % (url, urlencode(dict(utm_data)))
        return E.link(url)

    def generate(self):
        if len(self.product.images) == 0:
            return None
        self.exclude_if_not_sold()
        self.exlucde_if_not_source_country()
        self.check_shipping()
        if self.exclude:
            return None
        item = em.item(
            self.generate_id(),
            self.generate_title(),
            self.generate_link(),
            self.generate_price(),
            self.generate_availability(),
            self.generate_shipping(),
            self.generate_category(),
            self.generate_condition(),
            self.generate_brand(),
            self.generate_description(),
            self.generate_top_seller_rank(),
            self.generate_shipping_estimate(),
            self.generate_gender(),
            self.generate_color(),
            self.generate_material(),
            self.generate_age_group()
        )
        # We double check here if one of the functions above excluded the product
        for image_link in self.generate_image_links():
            item.append(image_link)
        if self.exclude:
            return None
        return item


class EbayXMLFeedWriter(XMLFeedWriter):

    xmlns_str = 'xmlns=""'

    def get_products(self):
        products = super(EbayXMLFeedWriter, self).get_products()
        # Only products that ship to this country
        products = products.filter(
            Q(shipping_profile__shipping_rules__countries=self.country)
            | Q(shipping_profile__others_price__gt=0)
        ).distinct()
        return products.order_by("number_of_sales")

    def products_iterator(self):
        for num, product in enumerate(self.get_products().iterator(), 1):
            # FIXME this is a bit nasty
            product.ebay_top_seller_rank = num
            yield product

    def get_builder(self, product):
        return EbayXMLProductFeedBuilder(self.currency, self.country, product)
