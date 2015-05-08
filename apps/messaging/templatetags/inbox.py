from django.template import Library, Node, TemplateSyntaxError
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe

from messaging.utils import message_to_reply

class InboxOutput(Node):
    def __init__(self, varname=None):
        self.varname = varname
        
    def render(self, context):
        try:
            user = context['user']
            count = user.received_messages.filter(read_at__isnull=True, recipient_deleted_at__isnull=True).count()
        except (KeyError, AttributeError):
            count = ''
        if self.varname is not None:
            context[self.varname] = count
            return ""
        else:
            return "%s" % (count)        
        
def do_print_inbox_count(parser, token):
    """
    A templatetag to show the unread-count for a logged in user.
    Returns the number of unread messages in the user's inbox.
    Usage::
    
        {% load inbox %}
        {% inbox_count %}
    
        {# or assign the value to a variable: #}
        
        {% inbox_count as my_var %}
        {{ my_var }}
        
    """
    bits = token.contents.split()
    if len(bits) > 1:
        if len(bits) != 3:
            raise TemplateSyntaxError, "inbox_count tag takes either no arguments or exactly two arguments"
        if bits[1] != 'as':
            raise TemplateSyntaxError, "first argument to inbox_count tag must be 'as'"
        return InboxOutput(bits[2])
    else:
        return InboxOutput()


register = Library()

@register.simple_tag
def thread_read_subject(thread, user):
    """
    Returns the class for unread thread, else ""
    """
    return "" if thread.read(user) else "dark-link"


@register.simple_tag
def thread_read_row(thread, user):
    """
    Returns the class for unread thread, else ""
    """
    return "answered" if thread.read(user) else "unanswered"


@register.simple_tag
def reply_url(thread, user):
    """
    Making the url to reply for each thread, 
    we must reply the last message sent
    to logged user.
    """
    message_reply = message_to_reply(thread, user)
    return reverse("messaging_reply", kwargs={'message_id': message_reply.pk}) if message_reply else ""

register.tag('inbox_count', do_print_inbox_count)
