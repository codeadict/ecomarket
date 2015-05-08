import re
import datetime

from django.utils.text import wrap
from django.utils.translation import ugettext, ugettext_lazy as _
from django.contrib.sites.models import Site
from django.template.loader import render_to_string
from django.conf import settings

from .models import MessageThread, ThreadUserState

# favour django-mailer but fall back to django.core.mail

if "mailer" in settings.INSTALLED_APPS:
    from mailer import send_mail
else:
    from django.core.mail import send_mail


def format_quote(sender, body):
    """
    Wraps text at 55 chars and prepends each
    line with `> `.
    Used for quoting messages in replies.
    """
    lines = wrap(body, 55).split('\n')
    for i, line in enumerate(lines):
        lines[i] = "> %s" % line
    quote = '\n'.join(lines)
    return ugettext(u"%(sender)s wrote:\n%(body)s") % {
        'sender': sender,
        'body': quote
    }


def recursive_body_text(thread_pk):
    """
    Returns "format_quote" for all thread messages.
    """
    body_text = ""
    try:
        thread = MessageThread.objects.get(pk=thread_pk)
        messages = thread.messages.all()
        for message in messages:
            body_text = "<br>" + format_quote(message.sender, message.body) + body_text
    except MessageThread.DoesNotExist:
        pass
    return body_text


def messages_parent_list(message):
    """
    Returns a list including both "message"
    param and each message's parents.
    """
    result_list = [message]
    while message.parent_msg:
        parent_msg = message.parent_msg
        result_list.insert(0, parent_msg)
        message = parent_msg
    return result_list


def format_subject(subject):
    """
    Prepends 'Re:' to the subject. To avoid multiple 'Re:'s
    a counter is added.
    NOTE: Currently unused. First step to fix Issue #48.
    FIXME: Any hints how to make this i18n aware are very welcome.
    """
    subject_prefix_re = r'^Re\[(\d*)\]:\ '
    m = re.match(subject_prefix_re, subject, re.U)
    prefix = u""
    if subject.startswith('Re: '):
        prefix = u"[2]"
        subject = subject[4:]
    elif m is not None:
        try:
            num = int(m.group(1))
            prefix = u"[%d]" % (num + 1)
            subject = subject[6 + len(str(num)):]
        except:
            # if anything fails here, fall back to the old mechanism
            pass

    return ugettext(u"Re%(prefix)s: %(subject)s") % {
        'subject': subject,
        'prefix': prefix
    }



def mark_action_thread(user, thread, action, tab=None):
    """
    Marks and returns True/False if the thread was marked as "action".
    i.e
    "action" can be "read"|"unread"|"resolved"|"unresolved"|"delete"
    so if we call:
       mark_action_thread(message_instance, user_instance, "read", "inbox")
    The "thread_instance" is marked as read (read_at attr of MessageThread takes value "now")
    """
    marked = False
    now = datetime.datetime.now()
    # When the user marks threads for being resolved/unresolved
    if 'resolved' in action:
        resolved_at = now if action == 'resolved' else None
        thread.resolved_at = resolved_at
        marked = True
        thread.save()
    # When the user marks threads for being read/unread
    elif 'read' in action:
        read_at = now if action == 'read' else None
        user_thread = ThreadUserState.objects.get(thread=thread, user=user)
        user_thread.read_at = read_at
        user_thread.save()
        marked = True
    # When the user marks threads for being deleted/undeleted
    elif action == 'delete':
        user_thread = ThreadUserState.objects.get(thread=thread, user=user)
        user_thread.deleted_at = now
        user_thread.save()
        marked = True
    return marked


def message_to_reply(thread, user):
    messages = thread.messages.exclude(sender=user)
    if not messages:
        # Fixes outbox irregularity.
        messages = thread.messages.all()
    if messages:
        message_to_reply = messages[0]
    else:
        message_to_reply = None
    return message_to_reply
