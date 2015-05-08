from django.conf import settings
from django.contrib.sites.models import Site


def globals(request):
    data = {}
    data.update({
        'CURRENT_SITE': Site.objects.get_current(),
        'DEFAULT_FROM_EMAIL': settings.DEFAULT_FROM_EMAIL,
        'SUPPORT_EMAIL': settings.SUPPORT_EMAIL,
        'GOOGLE_ANALYTICS_PROPERTY_ID': settings.GOOGLE_ANALYTICS_PROPERTY_ID,
        'GOOGLE_ANALYTICS_ENABLED': settings.GOOGLE_ANALYTICS_ENABLED,
        'GOOGLE_ANALYTICS_SITE_NAME': settings.GOOGLE_ANALYTICS_SITE_NAME,
        'GOOGLE_ADWORDS_ENABLED': settings.GOOGLE_ADWORDS_ENABLED,
        'DEBUG': settings.DEBUG,
        'TESTING': settings.TESTING,
        'MIXPANEL_TOKEN': settings.MIXPANEL_TOKEN,
        'MIXPANEL_ACTIVE': settings.MIXPANEL_ACTIVE,
        'FB_APP_ID': settings.FACEBOOK_APP_ID,
        })
    return data
