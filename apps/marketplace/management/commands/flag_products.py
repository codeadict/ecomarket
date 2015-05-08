# -*- encoding: utf-8 -*-
from django.core.management import BaseCommand
from marketplace.models import *


class Command(BaseCommand):

    def handle(self, *args, **options):
        profiles = ShippingProfile.objects.filter(shipping_rules=None)

        counter = 0
        stalls = set()

        for prof in profiles:
            closed = False

            if prof.others_price:
                continue

            products = prof.products.all()
            for p in products:
                if p.stall.is_closed:
                    closed = True

                if p.flag != 0:
                    p.flag = 0
                    p.save()

                    print "flagged ", p.get_absolute_url(), p.stall

            if closed or len(products) == 0:
                continue

            stalls.add(prof.stall)
            counter += products.count()

        print counter
        print len(stalls)
        print stalls