import hashlib

from django.utils.datastructures import SortedDict
from django.contrib.auth.hashers import BasePasswordHasher, mask_hash
from django.utils.translation import ugettext as _
from django.utils.crypto import constant_time_compare, salted_hmac


class JoomlaPasswordHasher(BasePasswordHasher):
    """
    Joomla 1.5 password hash checker

    The passwords in Joomla are stored in the following format:

    pwhash:salt (e.g.
    22b2e970f29aad96a71e0b8220a31b27$ypEyTmO9gCQM17ISIhBWxms2abimUxDP)

    For this to work in Django, you must convert it into the following string:

    joomla$pwhash$salt (e.g.
    joomla$22b2e970f29aad96a71e0b8220a31b27$ypEyTmO9gCQM17ISIhBWxms2abimUxDP)

    To convert an old hash, simply use:
    _hash = JoomlaPasswordHasher().convert_old_hash(_jhash)

    Then, to use that hash, you'd simply do;
    user.password = _hash
    user.save()

    """
    algorithm = "joomla"

    def encode(self, password, salt):
        assert password
        assert salt and '$' not in salt
        hash = hashlib.md5(str(password + salt)).hexdigest()
        return "%s$%s$%s" % (self.algorithm, hash, salt)

    def verify(self, password, encoded):
        algorithm, algohash, salt = encoded.split('$', 3)
        #assert len(encoded) == 65
        encoded_2 = self.encode(password, salt)
        return constant_time_compare(encoded, encoded_2)

    def safe_summary(self, encoded):
        algorithm, hash, salt = encoded.split('$', 3)
        #assert len(encoded) == 65
        return SortedDict([
            (_('algorithm'), self.algorithm),
            (_('salt'), mask_hash(salt, show=2)),
            (_('hash'), mask_hash(hash)),
        ])

    def convert_old_hash(self, encoded):
        hash, salt = encoded.split(":", 2)
        return "%s$%s$%s" % (self.algorithm, hash, salt)
