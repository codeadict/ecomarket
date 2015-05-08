import csv
import logging
import sys

from django.core.urlresolvers import reverse

from main.utils import absolute_uri
from apps.purchase.models import LineItem
from apps.marketplace.product_feed import XMLProductFeedBuilder, XMLFeedWriter, currency_convert, \
    COUNTRY_US, COUNTRY_GB
from apps.marketplace.management.commands.shopzilla_categories import shopzilla_categories


def removeNonAscii(s):
    if isinstance(s, basestring):
        return "".join(i for i in s if ord(i)<128)
    else:
        return str(s)

EcoMarket_to_Shopzilla_Category_Map = {
    'animals & pets': 13035, # more pet supplies
    'baby clothing accessories': 12977, # miscellaneous baby & toddler accessories
    'baby hats, gloves & scarves': 12977, # miscellaneous baby & toddler accessories
    'baby clothing sets': 13604, # miscellaneous baby & toddler apparel
    'baby coats & jackets': 13604, # miscellaneous baby & toddler apparel
    'baby grows': 13604, # miscellaneous baby & toddler apparel
    'baby jumpers & cardigans': 13604, # miscellaneous baby & toddler apparel
    'baby dresses': 14034, # baby & toddler dresses & skirts
    'baby shoes': 13455, # baby & toddler shoes & booties
    'baby socks': 14017, # baby & toddler socks
    'bibs': 13173, # baby bibs
    'bodysuits & onesies': 13177, # baby & toddler all-in-ones
    'baby clothing': 13604, # miscellaneous baby & toddler apparel
    'cots, carriers & prams': 13739, # miscellaneous baby gear
    'dummies & pacifiers': 13739, # miscellaneous baby gear
    'maternity gear': 14024, # miscellaneous maternity clothing & accessories
    'cots, carriers & prams': 13683, # pushchairs, buggies & prams
    'plates bottles & cups': 13739, # miscellaneous baby gear
    'rattles & teethers': 13739, # miscellaneous baby gear
    'blocks & building sets': 9935, # building toys,
    'dolls & doll houses': 14094, # dolls
    'bath toys & accessories': 13028, # bath & water toys
    'toys & activities': 13079, # miscellaneous infant toys
    'musical toys & instruments': 13048, # infant musical toys
    'games & puzzles': 9916, # miscellaneous games & puzzles
    'vehicle toys': 13416, # toy vehicles & planes
    'animals & soft toys': 13751, # soft toys & puppets
    'outdoor activities': 100001078, # miscellaneous outdoor games & fun
    'hair dryers': 14180, # hair care appliances
    'irons': 13279, # electric irons
    'kitchen appliances': 13744, # kitchen gadgets & utensils
    'other appliances': 13310, # miscellaneous appliances
    'vacuums': 9698, # vacuum cleaners
    'computer accessories': 13919, # desktop computer accessories
    'portable music players': 14125, # mp3 & media players
    'radios': 13992, # portable radios
    'speakers': 9673, # hi-fi speakers
    'blouses & tunics': 13396, # women's shirts & blouses
    'skirts': 13966, # women's skirts
    'bras': 13230, # women's bras
    'lingerie': 9020, # women's lingerie sets
    'hand bags': 14093, # handbags
    'bags & purses': 13750, # miscellaneous handbags & luggage
    'laptops': 13908, # laptop accessories
    'bracelets & bangles': 14135, # bracelets
    'jewellery': 14157, # other jewellery
    'necklaces': 14153, # necklaces & pendants
    'coffee': 14101, # coffee & tea
    'juices & soft drinks': 13203, # drinks & juices
    'tea': 14101, # coffee & tea
    'condiments': 14056, # condiments, seasonings & sauces
    'cooking oil': 13166, # oil & vinegar
    'fresh vegetables': 13003, # fruits & vegetables
    'herbs, spices & seasoning': 14056, # condiments, seasonings & sauces
    'home baking': 100000313, # baking ingredients
    'jams & preserves': 100000321, # honey, jam & marmalade
    'meat': 13579, # meat & seafood
    'snacks': 13827, # appetisers & snacks
    'sweets, cakes & chocolate': 13688, # miscellaneous chocolates & sweets
    'other tinned foods': 13043, # canned food
    'lubricant & oils': 13050, # lubricants
    'nails': 100000358, # nail care products
    'eyes': 13631, # eye care products
    'dental care': 14145, # dental care products
    'shaving': 14160, # shaving appliances
    'skin care': 13313, # skin care producs
    'bath robes': 12950, # bathroom linen
    'beds & bedding': 13167, # bedding
    'home cleaning': 9702, # cleaning accessories
    'mops & brushes': 9705, # miscellaneous home cleaning appliances
    'cleaning cloths & wipes': 9705, # miscellaneous home cleaning appliances
    'other cleaning accessories': 9705, # miscellaneous home cleaning appliances
    'spray & liquid cleaners': 9705, # miscellaneous home cleaning appliances
    'bowls & plates': 13744, # kitchen gadgets & utensils
    'cookware sets': 13744, # kitchen gadgets & utensils
    'cups & glasses': 13744, # kitchen gadgets & utensils
    'jugs': 13744, # kitchen gadgets & utensils
    'cushions & textiles': 9363, # cushions & cushion covers
    'craft materials & tools': 13143, # miscellaneous home decor
    'drawings, paintings & photos': 13143, # miscellaneous home decor
    'ornaments & sculptures': 13143, # miscellaneous home decor
    'other decor items': 13143, # miscellaneous home decor
    'picture frames': 13143, # miscellaneous home decor
    'candles & candle holders': 13117, # candles & home scents
    'ceiling lights': 14036, # home lighting
    'floor lights': 14036, # home lighting
    'other lighting': 14036, # home lighting
    'table lamps': 14036, # home lighting
    'paper & notebooks': 13982, # notebooks & pads
    'sticky notes': 14072, # miscellaneous office basics
    'rulers': 14072, # miscellaneous office basics
    'other office accessories': 14072, # miscellaneous office basics
    'camping gear': 13748, # camping & hiking equipment
    'barbecues & stoves': 13766, # barbecues & outdoor cooking equipment
    'gardening tools & accessories': 13040, # garden tools
    'plants': 14054, # plants & trees
    'seeds': 14054, # plants & trees
    'trees': 14054, # plants & trees
    'cycling': 100001031, # bicycle components & accessories
}

class TSVProductFeedBuilder(XMLProductFeedBuilder):
    def _gen(self, name, value):
        return value

    def generate_category_id(self):
        # The Shopzilla categories are stored in apps.marketplace.management.commands.shopzilla_categories
        # All categories are converted to lower case, and have only "&" symbol, no "and"
        cat = self.product.primary_category
        in_category = False
        while cat:
            _cat = str(cat.name).lower().replace('and', '&')
            if _cat in EcoMarket_to_Shopzilla_Category_Map:
                in_category = EcoMarket_to_Shopzilla_Category_Map[_cat]
                break
            if _cat in shopzilla_categories:
                in_category = shopzilla_categories[_cat]
                break
            cat = cat.parent

        if in_category:
            return self._gen('category_id', in_category)
        else:
            self.exclude = True

    def generate_title(self):
        title = self.product.title
        if title.upper() == title:
            title = title.title()
        return self._gen('title', title[0:99])

    def generate_link(self):
        path = reverse('product_page', kwargs={
            "stall_identifier": self.product.stall.identifier,
            "product_name": self.product.slug,
        })
        uri = absolute_uri(path)
        link_str = "%s" % (uri,)
        return self._gen('link', link_str)

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
        return self._gen('manufacturer', self.product.stall.title)

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
        if self.country.code == 'GB':
            self.check_shipping()
            self.exlucde_if_not_source_country()
            self.exclude_if_not_sold()
            if self.exclude:
                return None
            item = list([
                self.generate_category_id(),
                self.generate_manufacturer(),
                self.generate_title(),
                self.generate_description(),
                self.generate_link(),
                self.generate_image(),
                self.generate_id(), # SKU
                self.generate_nothing(), # Quantity on Hand
                self.generate_condition(), 
                self.generate_nothing(), # Ship. Weight
                self.generate_nothing(), # Ship. Cost
                self.generate_nothing(), # Bid
                self.generate_nothing(), # Promo Value
                self.generate_nothing(), # UPC
                self.generate_price()
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
            tsvh.writerow(['Category ID', 'Manufacturer', 'Title', 'Description', 'Link',
                'Image', 'SKU', 'Quantity on Hand', 'Condition', 'Ship. Weight',
                'Ship. Cost', 'Bid', 'Promo Value', 'UPC', 'Price'])
        for item in self.generate_data():
            ascii_item = [removeNonAscii(v)[0:990] for v in item]
            tsvh.writerow(ascii_item)


def write_feed(currency, country_obj, fh):
    return TSVFeedWriter(currency, country_obj).write(fh)