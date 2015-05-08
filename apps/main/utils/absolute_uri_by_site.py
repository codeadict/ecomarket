from django.contrib.sites.models import Site

def absolute_uri(path):
    site = Site.objects.get_current()
    return "http://{0}{1}".format(site.domain, path)
