from django.db.models.signals import post_save

from actstream import action

from apps.accounts.models import UserProfile
from apps.articles.models import Article
from apps.lovelists.models import LoveList, LoveListProduct
from apps.threadedcomments.models import ThreadedComment


def love_list_handler(sender, instance, created, **kwargs):
    if created and instance.is_public:
        action.send(
            instance.user,
            verb='created the love list',
            action_object=instance, target=instance.user.get_profile())


def comment_made_handler(sender, instance, created, **kwargs):
    if created:
        if instance.get_level() >= 1:
            verb = "replied to"
            target = instance.parent
        elif isinstance(instance.content_object, UserProfile):
            if instance.user == instance.content_object.user:
                # Updated their own status.
                verb = 'updated their status'
                target = None
            else:
                # Posted on someone's profile page.
                verb = 'wrote'
                target = instance.content_object.user.get_profile()
        else:
            verb = 'commented on'
            target = instance.content_object
        action.send(instance.user, verb=verb, action_object=instance,
                    target=target)


def loved_product_handler(sender, instance, created, **kwargs):
    if created:
        love_list = instance.love_list
        action.send(
            love_list.user,
            verb='added product to love list',
            action_object=instance, target=love_list)


def create_blog_post_action(sender, instance, created, **kwargs):
    if created:
        action.send(
            instance.author,
            verb='wrote a new blog post',
            action_object=instance, target=instance)


post_save.connect(comment_made_handler, sender=ThreadedComment, dispatch_uid="main_models_love_list_handler")
post_save.connect(love_list_handler, sender=LoveList, dispatch_uid="main_models_comment_made_handler")
post_save.connect(loved_product_handler, sender=LoveListProduct, dispatch_uid="main_models_loved_product_handler")
post_save.connect(create_blog_post_action, sender=Article, dispatch_uid="main_models_create_blog_post_action")