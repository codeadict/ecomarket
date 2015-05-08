import os
from os.path import abspath, dirname, join
import sys

sys.path.insert(0, abspath(join(dirname(__file__), "..")))
sys.path.insert(0, abspath(join(dirname(__file__), "")))
sys.path.insert(0, abspath(join(dirname(__file__), "apps")))

os.environ["DJANGO_SETTINGS_MODULE"] = "ecomarket.settings"

from django.core.handlers.wsgi import WSGIHandler
application = WSGIHandler()
