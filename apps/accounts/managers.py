import re

from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

SHA1_RE = re.compile('^[a-f0-9]{40}$')

class UserProfileManager(models.Manager):
    """
    Custom manager for the UserProfile model.
    """

    def create_user(self, is_active=True, **kwargs):
        """ Creates an inactive user. """
        user = User.objects.create_user(kwargs['username'],
            kwargs['email'],
            kwargs['password'])
        # We set this to false as we want the
        # user to verify their email before they
        # use their account.
        user.is_active = is_active
        user.first_name = kwargs['first_name']
        user.last_name = kwargs['last_name']
        user.save()        

        return user

    def activate_user(self, activation_key):
        """ Activates a user if the activation_key is valid. """
        if SHA1_RE.search(activation_key):
            # Activation key matches the regex so go and get it
            try:
                profile = self.get(activation_key=activation_key)
            except self.model.DoesNotExist:
                # Incorrect activation_key
                return False
            if not profile.activation_key_expired():
                # If we have a key that hasn't expired,
                # then we set the user to be active and
                # save the profile
                user = profile.user
                user.is_active = True
                user.save()
                profile.activation_key = profile.ACTIVATED
                profile.save()                
                return user
        return False
