from django.contrib.auth.models import User
from django.db import models
from django.db.models import permalink
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

from accounts.models import UserProfile


class MessageManager(models.Manager):

    def inbox_for(self, user):
        """
        Returns all messages that were received by the given user and are not
        marked as deleted.
        """
        return self.filter(
            recipient=user,
            recipient_deleted_at__isnull=True,
        )

    def outbox_for(self, user):
        """
        Returns all messages that were sent by the given user and are not
        marked as deleted.
        """
        return self.filter(
            sender=user,
            sender_deleted_at__isnull=True,
        )

    def trash_for(self, user):
        """
        Returns all messages that were either received or sent by the given
        user and are marked as deleted.
        """
        return self.filter(
            recipient=user,
            recipient_deleted_at__isnull=False,
        ) | self.filter(
            sender=user,
            sender_deleted_at__isnull=False,
        )

    def new_messages_count(self, user):
        """
        Returns new messages count this user has in his recipient.
        """
        return self.filter(
            recipient=user,
            read_at__isnull=True,
            recipient_deleted_at__isnull=True
        ).count()


class Message(models.Model):
    """
    A private message from user to user
    """
    thread = models.ForeignKey('MessageThread', related_name="messages")
    subject = models.CharField(_("Subject"), max_length=120)
    body = models.TextField(_("Body"))
    sender = models.ForeignKey(User, related_name='sent_messages', verbose_name=_("Sender"))
    recipient = models.ForeignKey(User, related_name='received_messages', null=True, blank=True, verbose_name=_("Recipient"))
    parent_msg = models.ForeignKey('self', related_name='next_messages', null=True, blank=True, verbose_name=_("Parent message"))
    sent_at = models.DateTimeField(_("sent at"), null=True, blank=True)
    read_at = models.DateTimeField(_("Read at"), null=True, blank=True)
    replied_at = models.DateTimeField(_("replied at"), null=True, blank=True)
    sender_deleted_at = models.DateTimeField(_("Sender deleted at"), null=True, blank=True)
    recipient_deleted_at = models.DateTimeField(_("Recipient deleted at"), null=True, blank=True)

    objects = MessageManager()

    class Meta:
        ordering = ['-sent_at']
        verbose_name = _("Message")
        verbose_name_plural = _("Messages")

    def save(self, **kwargs):
        if not self.id:
            self.sent_at = timezone.now()
        super(Message, self).save(**kwargs)

    @permalink
    def get_absolute_url(self):
        return ('messaging_detail', [self.id])

    def new(self):
        """returns whether the recipient has read the message or not"""
        if self.read_at is not None:
            return False
        return True

    def replied(self):
        """returns whether the recipient has written a reply to this message"""
        if self.replied_at is not None:
            return True
        return False

    def resolved(self):
        """returns whether the message is resolved or not.

        All messages in the thread are marked with the same timestamp.
        """
        if self.resolved_at is not None:
            return True
        return False

    def sender_profile(self):
        """
        Returns the sender profile for showing sender info at inbox.
        """
        try:
            _sender_profile = UserProfile.objects.get(user=self.sender)
        except UserProfile.DoesNotExist:
            _sender_profile = None

        return _sender_profile

    def sender_messages_count(self):
        """
        Returns the sender count messages sent to message user recipient.
        """
        return self.thread.messages.count()

    def __unicode__(self):
        return self.subject


class ThreadManager(models.Manager):

    def inbox_threads_for(self, user):
        """
        Returns all threads that were received by the given user and are not
        marked as deleted.
        """
        inbox_threads = self.filter(threads__deleted_at__isnull=True, threads__user=user, messages__recipient=user).distinct()
        return inbox_threads

    def outbox_threads_for(self, user):
        """
        Returns all threads that were sent by the given user and are not
        marked as deleted.
        """
        outbox_threads = self.filter(threads__deleted_at__isnull=True, threads__user=user, messages__sender=user).distinct()
        return outbox_threads

    def all_threads_for(self, user):
        """
        Returns all threads that were either received or sent by the given
        user and are not marked as deleted.
        """
        qs = (
            self.filter(threads__deleted_at__isnull=True, threads__user=user, messages__sender=user) |
            self.filter(threads__deleted_at__isnull=True, threads__user=user, messages__recipient=user)
        ).distinct()

        # The schema and ORM don't want to place nice and enable us to order
        # the threads by the most recent message date so we have to do this...
        thread_reads = {}
        for thread in qs:
            recent = thread.messages.order_by('-sent_at')[0]
            thread_reads[thread] = recent.sent_at

        return list(sorted(thread_reads, key=thread_reads.__getitem__, reverse=True))

    def new_threads_count(self, user):
        """
        Returns new threads count this user has in his recipient.
        """
        return self.filter(threads__deleted_at__isnull=True,
                           threads__read_at__isnull=True,
                           threads__user=user,
                           messages__recipient=user).distinct().count()


class MessageThread(models.Model):
    """
    Model for managing a list of messages with a common ancestor.
    'null' value for 'read_at' and 'resolved_at' means that Thread
    isn't read or resolved.
    """
    resolved_at = models.DateTimeField(_("resolved at"), null=True, blank=True)

    objects = ThreadManager()

    class Meta:
        verbose_name = _("Thread")
        verbose_name_plural = _("Threads")

    def resolved(self):
        """returns whether the thread is resolved or not.

        All messages in the thread are marked with the same timestamp.
        """
        return self.resolved_at is not None

    def read(self, user):
        try:
            thread_for_user = self.threads.get(user=user)
        except:
            thread_for_user = None

        return thread_for_user.read_at is not None

    def deleted(self, user):
        try:
            thread_for_user = self.threads.get(user=user)
        except:
            thread_for_user = None

        return thread_for_user.deleted_at is not None

    def thread_last_message(self, user, _from):
        """
        Returns the last message to show in user inbox/outbox.
        """
        thread_messages = self.messages.filter(recipient=user) if _from == 'inbox' else self.messages.filter(sender=user)

        return thread_messages[0] if thread_messages else None


class ThreadUserStateManager(models.Manager):

    def available_threads_for(self, user):
        return self.filter(user=user, deleted_at__isnull=True)

    def noread_threads_for(self, user):
        return self.filter(user=user, read_at__isnull=True)


class ThreadUserState(models.Model):
    """
    Models for keeping the state a thread has per user.
    """
    user = models.ForeignKey(User, related_name='thread_users')
    thread = models.ForeignKey(MessageThread, related_name='threads')
    read_at = models.DateTimeField(_("Read at"), null=True, blank=True)
    deleted_at = models.DateTimeField(_("Deleted at"), null=True, blank=True)

    objects = ThreadUserStateManager()

    class Meta:
        unique_together = ('user', 'thread')


def inbox_count_for(user):
    """
    returns the number of unread messages for the given user but does not
    mark them seen
    """
    return Message.objects.filter(recipient=user, read_at__isnull=True, recipient_deleted_at__isnull=True).count()
