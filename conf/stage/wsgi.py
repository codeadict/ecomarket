import os, sys
import django.core.handlers.wsgi


PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(PROJECT_ROOT)
sys.path.append(os.path.dirname(PROJECT_ROOT))

sys.stdout = sys.stderr

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

application = django.core.handlers.wsgi.WSGIHandler()
