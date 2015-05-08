from django.test import TestCase
from mailing_lists.management.commands import import_from_csv
from mailing_lists.models import MailingListSignup
import os
from os import path
from tests import factories

def get_fixture_filename(filename):
    return path.join(path.dirname(__file__), filename)

class ImportCsvTestCase(TestCase):

    def setUp(self):
        self.fixture_filename = get_fixture_filename("test_contacts.csv")
        self.command = import_from_csv.Command()

    def test_imported_csv_creates_signups(self):
        self.command.handle(self.fixture_filename)
        signups = MailingListSignup.objects.all()
        self.assertEqual(len(signups), 1)
        self.assertEqual(signups[0].email_address, "thisisatest@gmail.com")

    def test_existing_address_causes_no_problems(self):
        signup = MailingListSignup.objects.create(
            email_address="thisisatest@gmail.com")
        self.command.handle(self.fixture_filename)

    def test_skips_duplicate_users(self):
        user1 = factories.UserFactory(email="thisisatest@gmail.com")
        user2 = factories.UserFactory(email="thisisatest@gmail.com")
        self.command.handle(self.fixture_filename)

    def test_emails_with_spaces_dont_error_out(self):
        fixture_name = get_fixture_filename("test_bad_dupe_space_emails.csv")
        self.command.handle(fixture_name)
