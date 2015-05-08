import inspect

from django.core.urlresolvers import reverse

from main.utils import absolute_uri
from mailing_lists.integrations.sailthru import Sailthru


class CommentNotifier(object):
    @classmethod
    def get_notifier(cls, request, comment):
        from articles.models import Article
        from marketplace.models import Product
        from lovelists.models import LoveList
        from accounts.models import UserProfile

        model = comment.content_type.model_class()
        data = {
            Article: ArticleCommentNotifier,
            LoveList: LoveListCommentNotifier,
            Product: ProductCommentNotifier,
            UserProfile: UserProfileCommentNotifier,
        }
        return data[model](request, comment)

    def __init__(self, request, comment):
        self.request = request
        self._sent_emails = set()
        self.comment = comment
        self.commenter = comment.user

    def get_context(self, user):
        profile_url = reverse("public_profile", args=(self.commenter, ))
        update_profile = reverse("account_email_notifications")
        return {
            "COMMENT": self.comment.comment,
            "COMMENT_REPLY_URL": absolute_uri(self.comment.get_reply_url()),
            "COMMENTER_USERNAME": self.commenter.username,
            "COMMENTER_PROFILE_URL": absolute_uri(profile_url),
            "FNAME": user.first_name,
            "UPDATE_PROFILE": absolute_uri(update_profile),
        }

    def get_content(self):
        return {}

    def send(self, template_name, user, subject):
        if user == self.commenter:
            return
        if (template_name, user.email) in self._sent_emails:
            # Refuse to send duplicates in the same session
            return
        self._sent_emails.add((template_name, user.email))
        return Sailthru(self.request).send_template(
            template_name,
            user.email,
            self.get_context(user))

    def _to_thread(self, callback):
        """Perform the specified callback on every related comment"""
        if self.comment.get_level() > 0:
            callback(self.comment.parent)
            for sibling in self.comment.get_siblings():
                callback(sibling)

    def send_all(self):
        for name, value in inspect.getmembers(self):
            if name in ("send_all", "send"):
                continue
            if name.startswith("send") and callable(value):
                value()


class ArticleCommentNotifier(CommentNotifier):

    def __init__(self, request, comment):
        super(ArticleCommentNotifier, self).__init__(request, comment)
        self.article = comment.content_object
        self.article_owner = self.article.author

    def get_context(self, user):
        context = super(ArticleCommentNotifier, self).get_context(user)
        context.update({
            "BLOG_POST_TITLE": self.article.title,
            "BLOG_POST_URL": absolute_uri(self.article.get_absolute_url())
        })
        return context

    def send_article_notification(self):
        return self.send("comment-notification-blog",
                         self.article_owner,
                         "Someone commented on your article")

    def send_article_replies(self):
        def callback(comment):
            return self.send("comment-notification-blog-reply",
                             comment.user,
                             "Someone replied to your blog comment")
        return self._to_thread(callback)


class ProductCommentNotifier(CommentNotifier):

    def __init__(self, request, comment):
        super(ProductCommentNotifier, self).__init__(request, comment)
        self.product = comment.content_object
        self.product_owner = self.product.stall.user

    def get_context(self, user):
        context = super(ProductCommentNotifier, self).get_context(user)
        context.update({
            "PRODUCT_TITLE": self.product.title,
            "PRODUCT_URL": absolute_uri(self.product.get_absolute_url())
        })
        return context

    def send_product_page_notification(self):
        return self.send("comment-notification-your-product",
                         self.product_owner,
                         "Someone commented on your product")

    def send_product_page_replies(self):
        def callback(comment):
            return self.send("comment-notification-product-reply",
                             comment.user,
                             "Someone replied to a product comment")
        return self._to_thread(callback)


class UserProfileCommentNotifier(CommentNotifier):

    def __init__(self, request, comment):
        super(UserProfileCommentNotifier, self).__init__(request, comment)
        self.user_profile = comment.content_object
        self.user = self.user_profile.user

    def get_context(self, user):
        context = super(UserProfileCommentNotifier, self).get_context(user)
        context.update({
            "PROFILE_URL": absolute_uri(self.user_profile.get_absolute_url())
        })
        return context

    def send_profile_page_notification(self):
        return self.send("comment-notification-profile-wall",
                         self.user,
                         "Someone said something on your profile")

    def send_profile_page_replies(self):
        def callback(comment):
            return self.send("comment-notification-profile-wall-replied",
                             comment.user,
                             "Someone replied to your profile comment")
        return self._to_thread(callback)


class LoveListCommentNotifier(CommentNotifier):

    def __init__(self, request, comment):
        super(LoveListCommentNotifier, self).__init__(request, comment)
        self.love_list = comment.content_object
        self.owner = self.love_list.user

    def get_context(self, user):
        context = super(LoveListCommentNotifier, self).get_context(user)
        context.update({
            "LOVELIST_TITLE": self.love_list.title,
            "LOVELIST_URL": absolute_uri(self.love_list.get_absolute_url()),
        })
        return context

    def send_love_list_notification(self):
        return self.send("comment-notification-love-list",
                         self.owner,
                         "Someone commented on your love list")

    def send_love_list_replies(self):
        def callback(comment):
            return self.send("comment-notification-love-list-replied",
                             comment.user,
                             "Someone replied to your love list comment")
        return self._to_thread(callback)