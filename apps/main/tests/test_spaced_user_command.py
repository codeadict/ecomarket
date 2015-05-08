from django.contrib.auth.models import User
from django.test import TestCase
from main.management.commands.rename_spaced_users import Command
import mock
from StringIO import StringIO
from tests import factories


class SpacedUserCommandTestCase(TestCase):

    def setUp(self):
        self.command = Command()
        self.user = factories.UserFactory(username="my name")

    def test_user_with_spaces_username_renamed(self):
        self.command.handle()
        user = User.objects.get(id=self.user.id)
        self.assertEqual(user.username, "myname")

    def test_unrenamable_user_written_to_file(self):
        user2 = factories.UserFactory(username="myname")
        user3 = factories.UserFactory(username="your name")
        user4 = factories.UserFactory(username="yourname")
        self.command.handle()
