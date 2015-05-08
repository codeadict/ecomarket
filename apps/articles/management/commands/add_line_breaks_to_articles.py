from BeautifulSoup import BeautifulSoup

from django.core.management.base import NoArgsCommand
from django.template.defaultfilters import linebreaks

from articles.models import Article

class Command(NoArgsCommand):

    def handle_noargs(self, **opts):
        for article in Article.objects.all():
            soup = BeautifulSoup(article.content)
            if soup.find("p"):
                continue
            self.stdout.write("Updating %s... " % article.slug)
            self.stdout.flush()
            article.content = linebreaks(article.content)
            article.save()
            self.stdout.write("done\n")
