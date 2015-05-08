from main.utils import absolute_uri
from marketplace.models import Product, CurrencyExchangeRate
from purchase.models import LineItem
from django.core.management.base import BaseCommand, CommandError, make_option
from django.core.urlresolvers import reverse
import json, re, traceback


def f7(seq):
    """
    Getting uniques from a list
    http://stackoverflow.com/questions/480214/how-do-you-remove-duplicates-from-a-list-in-python-whilst-preserving-order
    """
    seen = set()
    seen_add = seen.add
    return [ x for x in seq if x not in seen and not seen_add(x)]


class Command(BaseCommand):

    help = "Generate product_feed file and write to the specified file"
    args = "filename"
    option_list = BaseCommand.option_list + (
        make_option("--format", default=None, dest="format",
                    help="File format to use (xml or txt)"),
    )

    def _truncate_text(self, content, length=100, suffix='...'):
      content = re.sub('<[^<]+?>', '', content)
      content = re.sub('\s+', ' ', content)
      if len(content) > length:
          return ' '.join(content[:length+1].split(' ')[0:-1]) + suffix
      return content.strip()

    def format_currency(self, code, value):
        if code in ['SEK', 'JPY', 'INR']:
            return int(value)
        return "%.2f" % (value,)

    def get_all_prices(self, price):
        prices = {code: self.format_currency(code, value)
                  for code, value in CurrencyExchangeRate.amount_in_all_currencies(price.amount).items()}
        if 'GBP' not in prices:
          prices['GBP'] = self.format_currency('GBP', price.amount)
        return prices

    def handle(self, *args, **options):
        try:
            filename, = args
        except ValueError:
            raise CommandError(
                "This command takes 1 argument: the filename to write to")

        feed = {
            'feed': {
                'name': 'Products Feed'
            },
            'content': []
        }
        lines = LineItem.objects.all().order_by('-pk')
        products = list()
        for l in lines:
            try:
                if l.product.status == Product.PUBLISHED_LIVE:
                    products.append(l.product)
            except:
                pass

        # Make unique, only first 1800
        products = f7(products[:1800])
        
        for product in products:
            stall = product.stall
            owner = stall.user
            keywords = [keyword.slug for keyword in product.keywords.all()]
            categories = [c.slug for c in product.category_objs()]
            tags = ['ecomarket-product'] + keywords + categories
            image = product.image

            stall_url = stall.get_absolute_url()
            stall_owner_url = reverse('public_profile', args=[owner.username])

            try:
                record = {'tags': tags,
                          'date': int(product.updated.strftime('%s')),
                          'title': product.title,
                          'description': self._truncate_text(product.description),
                          'price': self.get_all_prices(product.get_price_instance()),
                          'url': product.get_absolute_url(),
                          'images': {'thumb': image.url_50,
                                     'thumb400': image.url_400},
                          'stall_title': product.stall.title,
                          'stall_owner': product.stall.user.username,
                          'stall_owner_id': product.stall.user.id,
                          'urls': {'stall_owner': stall_owner_url,
                                 'stall': stall_url}}                
            except Exception:              
                traceback.print_exc()
                continue
            feed['content'].append(record)

        with open(filename, "w") as fh:
            fh.write(json.dumps(feed))
