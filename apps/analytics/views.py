from django.core.cache import cache
from django.http import HttpResponse


def clicktale_recorded_page(request, hash):
    response = cache.get(hash)
    if response:
        return response
    else:
        return HttpResponse('Sorry...')