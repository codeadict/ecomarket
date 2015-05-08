# -*- encoding: utf-8 -*-
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
import requests


def send_to_hipchat(message_text, color="green", room_id=None, notify=0):
    if not room_id:
        room_id = _get_room()
        
    message = {
        'room_id': room_id,
        'from': "Ecomarket",
        'message': message_text,
        'color': color,
        'notify': notify,
        'auth_token': _get_token(),
    }

    raw_response = requests.get(_get_api_url(), params=message)
    response_data = raw_response.json
    return response_data


def _get_token():
    token = getattr(settings, "HIPCHAT_TOKEN")
    if not token:
        raise ImproperlyConfigured("Please set HIPCHAT_TOKEN in your configuration.")

    return token


def _get_room():
    room = getattr(settings, "HIPCHAT_ROOM")
    if not room:
        raise ImproperlyConfigured("Please set HIPCHAT_ROOM in your configuration.")

    return room


def _get_api_url():
    return getattr(settings, "HIPCHAT_API_URL", "https://api.hipchat.com/v1/rooms/message")