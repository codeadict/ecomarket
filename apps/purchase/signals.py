# -*- encoding: utf-8 -*-
import django.dispatch


order_payed = django.dispatch.Signal(providing_args=["order", "request"])