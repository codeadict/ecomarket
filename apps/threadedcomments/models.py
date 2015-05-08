import logging

from django.db import models
from django.dispatch import receiver

from django.contrib.auth.models import User
from django.contrib.comments.models import (
    CommentFlag, BaseCommentAbstractModel, COMMENT_MAX_LENGTH)
from django.contrib.comments.managers import CommentManager
from django.contrib.comments.signals import (
        comment_was_posted, comment_was_flagged)
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

from mptt.models import MPTTModel, TreeForeignKey

from threadedcomments.facebook import post_comment_to_facebook
from threadedcomments.notifier import CommentNotifier

logger = logging.getLogger(__name__)


class ThreadedComment(MPTTModel, BaseCommentAbstractModel):

    # Copied from comments.Comment
    user = models.ForeignKey(User, verbose_name=_('user'),
                             blank=True, null=True,
                             related_name="%(class)s_comments")
    comment = models.TextField(_('comment'), max_length=COMMENT_MAX_LENGTH)
    submit_date = models.DateTimeField(_('date/time submitted'), default=None)
    ip_address = models.IPAddressField(_('IP address'), blank=True, null=True)
    is_public = models.BooleanField(
        _('is public'), default=True,
        help_text=_('Uncheck this box to make the comment effectively '
                    'disappear from the site.'))
    is_removed = models.BooleanField(
        _('is removed'), default=False,
        help_text=_('Check this box if the comment is inappropriate. '
                    'A "This comment has been removed" message will '
                    'be displayed instead.'))
    objects = CommentManager()

    class Meta:
        ordering = ('tree_id', 'submit_date', )

    def __unicode__(self):
        if self.is_removed:
            return u"a deleted comment"
        try:
            name = self.user.username
        except Exception:
            name = None
        return u"%s: %s..." % (name, self.comment[:50])

    def save(self, *args, **kwargs):
        if self.submit_date is None:
            self.submit_date = timezone.now()

        # Forbid more than 2 levels
        if self.parent_id is not None:
            while self.parent.get_level() > 0:
                self.parent = self.parent.parent

        super(ThreadedComment, self).save(*args, **kwargs)

    def get_absolute_url(self, anchor_pattern="#comment-{id}"):
        url_base = self.get_content_object_url()
        return url_base + anchor_pattern.format(**self.__dict__)

    def get_reply_url(self, anchor_pattern="#reply-comment-{id}"):
        url_base = self.get_content_object_url()
        return url_base + anchor_pattern.format(**self.__dict__)

    def get_toplevel(self):
        if self.get_level() == 0:
            return self
        return self.parent.get_toplevel()

    # My stuff
    parent = TreeForeignKey('self', null=True, blank=True,
                            related_name='children')
    post_to_facebook = models.BooleanField(default=False)

    class MPTTMeta:
        # comments on one level will be ordered by date of creation
        order_insertion_by = ['submit_date']


class ThreadedCommentFlag(models.Model):

    # Copied from comments.CommentFlag
    user = models.ForeignKey(User, verbose_name=_('user'),
                             related_name="threaded_comment_flags")
    flag = models.CharField(_('flag'), max_length=30, db_index=True)
    flag_date = models.DateTimeField(_('date'), default=None)

    class Meta:
        unique_together = [('user', 'comment', 'flag')]

    def __unicode__(self):
        return "%s flag of comment ID %s by %s" % \
            (self.flag, self.comment_id, self.user.username)

    def save(self, *args, **kwargs):
        if self.flag_date is None:
            self.flag_date = timezone.now()
        super(ThreadedCommentFlag, self).save(*args, **kwargs)

    # My stuff
    comment = models.ForeignKey(ThreadedComment, related_name="flags")


@receiver(comment_was_flagged)
def delete_linked_actions(sender, comment, flag, **kwargs):
    if flag.flag == CommentFlag.MODERATOR_DELETION and comment.is_removed:
        comment.action_object_actions.all().delete()


@receiver(comment_was_posted)
def maybe_post_to_facebook(sender, comment, request, **kwargs):
    if not comment.post_to_facebook:
        return
    if not comment.user.get_profile().has_facebook_auth:
        return False
    try:
        post_comment_to_facebook(request, comment.user, comment)
    except Exception, e:
        logger.error(e, exc_info=True)


@receiver(comment_was_posted)
def maybe_send_email(sender, comment, request, **kwargs):
    try:
        notifier = CommentNotifier.get_notifier(request, comment)
    except KeyError:
        # Notifier does not exist for this type of object
        return
    try:
        notifier.send_all()
    except Exception, e:
        logger.error(e, exc_info=True)
