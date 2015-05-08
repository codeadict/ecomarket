# -*- encoding: utf-8 -*-
from BeautifulSoup import BeautifulSoup
from dateutil.parser import parse
from django.core.management import CommandError
from django_common.tzinfo import utc
from monitoring.lib.nagios_command import NagiosCommand
import requests
import datetime


class Command(NagiosCommand):
    args = "attribute_name value"

    def handle(self, *args, **options):
        attribute_name = args[0]
        attribute_value = args[1]

        result = requests.get("http://localhost:8983/solr/select/?q=*%3A*&start=0&rows=1&sort=updated+desc")
        tree = BeautifulSoup(result.content)

        elements = tree.findAll(self.get_find_method(attribute_name, attribute_value))

        if len(elements) != 1:
            raise CommandError("the search did not return 1 result")

        date_str = elements[0].getText()
        now = datetime.datetime.utcnow().replace(tzinfo=utc)
        last_update = parse(date_str)

        time_diff = now - last_update

        if time_diff.days == 0:
            self.log_exit(0, "Everything is fine!")
        else:
            self.log_exit(2, "No product in the search index was updated in the last 24 hours")

    def get_find_method(self, attribute, name):
        def find_method(tag):
            return tag.get(attribute) == name
        return find_method