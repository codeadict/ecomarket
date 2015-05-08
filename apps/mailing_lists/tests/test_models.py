from django.test import TestCase
from tests import factories
from mailing_lists.models import MailingListSignup

class CreateSignupFromEmailTestCase(TestCase):

    def test_create_with_email_for_existing_user_sets_user_relationship(self):
        existing_user = factories.UserFactory(email="thisisme@gmail.com")
        signup = MailingListSignup.create_from_email("thisisme@gmail.com")
        self.assertEqual(signup.user, existing_user)

    def test_without_existing_user_new_signup_created(self):
        signup = MailingListSignup.create_from_email("thisisme@gmail.com", first_name="test")
        self.assertEqual(signup.first_name, "test")
