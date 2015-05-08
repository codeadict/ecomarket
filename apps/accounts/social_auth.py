"""Extra stages in the social_auth pipeline
See settings.SOCIAL_AUTH_PIPELINE
"""

from __future__ import absolute_import

from contextlib import closing
import json
from urllib import urlopen

from django.core.exceptions import ObjectDoesNotExist
from django.core.files.base import ContentFile

from social_auth.exceptions import AuthException

from accounts.models import UserProfile
from notifications import Events


class FacebookError(AuthException):
    """Any error relating to our pipeline functions"""


def create_profile(backend, user, user_profile=None, **kwargs):
    """Creates a UserProfile when a user signs up using Facebook."""

    if user_profile is not None:
        return {"user_profile": user_profile}

    try:
        user_profile = UserProfile.objects.get(user=user)
    except UserProfile.DoesNotExist:
        user_profile = UserProfile.objects.create(
            user=user,
            send_newsletters=False,
            activation_key=UserProfile.ACTIVATED,
            social_auth='facebook',
        )

    return {
        "user_profile": user_profile
    }


def _load_person_avatar(backend, person, profile, info):
    image_url = None

    if backend.name == 'facebook':
        image_url = 'http://graph.facebook.com/%s/picture?type=large' % \
            info.get('id')

    if image_url and not profile.avatar.name:
        try:
            with closing(urlopen(image_url)) as image_content:
                # Facebook default image check
                if backend.name == 'facebook' \
                        and 'image/gif' in str(image_content.info()):
                    return

                image_name = "{id}.{subtype}".format(
                    id=person.id, subtype=image_content.headers.subtype)
                profile.avatar.save(image_name,
                                    ContentFile(image_content.read()))
            profile.save()
        except Exception, e:
            raise FacebookError(backend, e)


def _load_person_description(backend, person, profile, person_auth):
    access_token = person_auth.tokens["access_token"]
    me_url = "https://graph.facebook.com/me?access_token={0}".format(
        access_token)

    try:
        with closing(urlopen(me_url)) as raw_result:
            result = json.load(raw_result)
        if "bio" in result:
            desc = result["bio"]
            if not profile.about_me:
                profile.about_me = desc
                profile.save()
    except Exception as e:
        raise FacebookError(backend, e)


def update_person_details(backend, user, user_profile, response, **kwargs):
    """Update user profile using data from provider."""
    
    if user is None or user_profile is None:
        return
    
    try:
        person_auth = user.social_auth.get(provider=backend.name)
    except ObjectDoesNotExist:
        # TODO: person_auth should always exist in our pipeline, but for some
        # reason it sometimes doesn't. Find out why
        return

    if response:
        if not user_profile.city:
            city = response.get('location', None)
            if city:
                # Uppsala, Sweden  -> Uppsala
                user_profile.city = city['name'].split(',')[0]

        if not user_profile.birthday:
            birthday = response.get('birthday', None)
            if birthday:
                month, day, year = birthday.split('/')
                # Quick hack, make this prettier
                if int(month) > 12:
                    month, day = day, month
                user_profile.birthday = '-'.join([year, month, day])

        if not user_profile.gender:
            gender = response.get('gender', 'male')
            if gender == 'male':
                user_profile.gender = UserProfile.GENDER_MALE
            elif gender == 'female':
                user_profile.gender = UserProfile.GENDER_FEMALE

        user_profile.save()

    _load_person_avatar(backend, user, user_profile, response)
    _load_person_description(backend, user, user_profile, person_auth)

    # When all the data is synchronised with facebook do a 'user_signup' event
    # These accounts don't require activation because it comes via Facebook
    if kwargs.get('is_new', False):
        Events(kwargs['request']).user_signup(user, requires_activation=False)
    else:
        Events(kwargs['request']).logged_in(user)

    return {}
