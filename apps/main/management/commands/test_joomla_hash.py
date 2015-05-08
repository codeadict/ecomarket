#!/bin/sh

from django.contrib.auth.models import User; 
import hashlib
import random
import sys


from django.conf import settings
from django.core.management.base import NoArgsCommand, CommandError

from datetime import datetime
from os import path

import commands
from accounts.hashers import JoomlaPasswordHasher

class Command(NoArgsCommand):
    help = "Tests the Joomla hashing functionality to ensure its working properly"

    def handle_noargs(self, **options):
        t = JoomlaHashTest()
        t.test()

class JoomlaHashTest(object):
    """Runs a test to ensure that the hashing mechanism is
    working correctly."""

    def _generate_random_user(self):
        # Create random user/email
        m = hashlib.sha1()
        m.update(str(random.random()))
        _username = "test_%s" % ( m.hexdigest()[:8], )
        _email = "%s@test.com" % ( _username, )

        u = User.objects.create_user(_username, _email)
        return u

    def test(self):
        # Password of Joomla hash below
        _pw = "gonzo69"

        # Known working hash + salt from Joomla
        _jhash = "22b2e970f29aad96a71e0b8220a31b27:ypEyTmO9gCQM17ISIhBWxms2abimUxDP"

        # Expected Django equivilent hash
        _expected_hash = "joomla$22b2e970f29aad96a71e0b8220a31b27$ypEyTmO9gCQM17ISIhBWxms2abimUxDP"

        # Generate random user
        user = self._generate_random_user()

        # convert the Joomla hash into a Django hash
        _new_hash = JoomlaPasswordHasher().convert_old_hash(_jhash)

        # ensure the hash matches what we expect
        assert _new_hash == _expected_hash, "Hashes do not match, something is wrong"

        # store the hash
        user.password = _new_hash
        user.save()

        # now try and validate the password
        assert user.check_password(_pw), "Joomla password did not verify, something is wrong"
        print "Joomla password hashing OK"

        # Now ensure its not messing with our existing authentication
        _new_pw = "test123"
        user.set_password(_new_pw)
        assert user.check_password(_new_pw), "Django password did not verify, something is wrong"

        # remove the user
        user.delete()
        print "Django password hashing OK"