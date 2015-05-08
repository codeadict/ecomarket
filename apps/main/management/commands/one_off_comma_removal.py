from django.core.management.base import NoArgsCommand, CommandError
from marketplace.models import Keyword
import re

class Command(NoArgsCommand):

    def handle_noargs(self, **options):
        angleReg = re.compile("<|>")
        for keyword in Keyword.objects.filter(title__contains=","):
            self.stdout.write("processing keyword {0}\n".format(keyword))
            # turn '<keyword1, keyword2 keyword2>' into ['keyword1', 'keyword2 keyword2']
            names = [n.strip() for n in angleReg.sub("", keyword.title).split(",")]
            # Create new keywords (or get existing ones) for all the rest of the names.
            new_keywords = []
            for name in names:
                try:
                    new_keyword = Keyword.objects.get(title=name)
                except Keyword.DoesNotExist:
                    new_keyword = Keyword.objects.create(title=name)
                new_keywords.append(new_keyword)
            for product in keyword.products.all():
                product.keywords.add(*new_keywords)
                product.save()
            #Delete the old keyword
            keyword.delete()
