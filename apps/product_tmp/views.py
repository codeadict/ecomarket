import logging

from django.contrib.auth.decorators import login_required
from django.core.serializers.json import DjangoJSONEncoder
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest, Http404
from django.middleware.csrf import get_token
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import simplejson as json
from django.views.generic import DetailView
