from django.test import TestCase

from django.contrib.auth.models import User

from apps.social_network.models import UserFollow

class UserFollowTests(TestCase):
    """
    Represents the tests for the UserFollow model.
    """

    def setUp(self):
        self.users = User.objects.all()[0:3]

    def test_save_existing_relation(self):
        first = self.users[0]
        second = self.users[1]
        user_follow = UserFollow(user=first, follow=second)
        user_follow.save()

        another_follow = UserFollow(user=first, follow=second)

        self.assertRaisesMessage(Exception, "Relation between %s and %s "
                                            "already exists" % (first, second),
                                 callable_obj=another_follow.save)

    def test_save_relation_user_following_itself(self):
        user = self.users[0]
        user_follow = UserFollow(user=self.users[0], follow=user)
        self.assertRaisesMessage(Exception, "An user cannot follow itself",
                                 callable_obj=user_follow.save)

    def test_save_user(self):
        first = self.users[0]
        second = self.users[1]
        user_follow = UserFollow(user=first, follow=second)
        user_follow.save()