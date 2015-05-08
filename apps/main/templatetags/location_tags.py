from django import template
from django.conf import settings
from django.contrib.localflavor.us.us_states import STATE_CHOICES

register = template.Library()

STATE_CHOICES_DICT = dict(STATE_CHOICES) # Given state code, returns state name
STATE_ABBREV_CHOICES_DICT = dict((v,k) for k, v in STATE_CHOICES_DICT.iteritems()) # Given state name, returns state code

@register.filter
def get_state_verbose(statecode):
    return STATE_CHOICES_DICT.get(statecode.upper().strip(), statecode)

@register.filter
def get_state_code(state):
    return STATE_ABBREV_CHOICES_DICT.get(state, state)
