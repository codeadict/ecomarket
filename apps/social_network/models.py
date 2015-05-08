import datetime

from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

from actstream import action


class UserFollow(models.Model):
    """
    Contains the follow and following relations of users.
    """
    user = models.ForeignKey(User, related_name='follows')
    target = models.ForeignKey(User, related_name='following')
    date = models.DateTimeField()

    def save(self, *args, **kwargs):
        """
        Saves an UserFollow instance checking that an User cannot follow itself
        and that the relation between those users doesn't exists.
        """
        if self.user == self.target:
            raise Exception("An user cannot follow itself")
        if UserFollow.objects.filter(user=self.user, target=self.target):
            raise Exception("Relation between %s and %s already exists" % (self.user, self.target))
        if not self.date:
            self.date = datetime.datetime.now()
        return super(UserFollow, self).save(*args, **kwargs)

    @staticmethod
    def relation_exists(user, target):
        """
        Determines if a given user follows other
        :param user: The user that follow the other user
        :param target: The other users
        :return: Returns true if the first user follows the second, False otherwise
        """
        return UserFollow.objects.filter(user=user, target=target).count() == 1

    @staticmethod
    def get_follow_candidates(user=None, take=3, avatar_size=80):
        """
        Retrieves a list of possible follow options to a given user
        :param user: The user we want to provide candidates for
        :return: Returns an User queryset containing all of the candidate users to follow
        """
        from apps.purchase.models import LineItem

        all_items = LineItem.objects.order_by('-created')
        candidate_users = []
        start, end = (0, 100)

        while True:
            sliced_items = all_items[start: end]
            for sliced_item in sliced_items:
                try:
                    stall = sliced_item.product.stall
                    user = stall.user
                    profile = user.get_profile()
                    required_avatar = profile.avatar_or_default(avatar_size)
                    has_suitable_avatar = not required_avatar.endswith("images/avatar/%s/avatar.png" % avatar_size)
                    if has_suitable_avatar and stall.description_short and \
                            (user not in candidate_users):
                        candidate_users.append(user)
                        yield user
                        if len(candidate_users) == take:
                            return
                except ObjectDoesNotExist:
                    pass
            start, end = end, start+end
            if not sliced_items:
                break

    @staticmethod
    def user_follow(user):
        """
        Determines all of the users followed by a given user
        :param user: The given user
        :return:Returns an iterable with the user's followed people
        """
        return UserFollow.objects.filter(user=user)


    @staticmethod
    def user_following(user):
        """
        Determines all of the users following a given user
        :param user: The given user
        :return:Returns an iterable with the user's following people
        """
        return UserFollow.objects.filter(target=user)

    def __unicode__(self):
        return u'%s follows %s' % (self.user.username, self.target.username)

    class Meta:
        verbose_name_plural = 'user follows'
        ordering = ("user", )


def create_follow_action(sender, instance, created, **kwargs):
    if created:
        action.send(
            instance.user,
            verb='followed',
            action_object=instance, target=instance.target)
post_save.connect(create_follow_action, sender=UserFollow, dispatch_uid="social_network_models_create_follow_action")