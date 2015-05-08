# encoding: utf-8
from datetime import timedelta

from django import template
from django.template.defaultfilters import slugify

from actstream.models import Action

from main.utils.actions import related_actions

register = template.Library()


class RemoveSessionMessageNode(template.Node):
    def __init__(self, *args, **kwargs):
        super(RemoveSessionMessageNode, self).__init__(*args, **kwargs)
        self.request_variable = template.Variable('request')

    def render(self, context):
        request = self.request_variable.resolve(context)
        request.session['messages'] = []
        return ''


@register.tag
def remove_session_messages(parser, token):
    parts = token.split_contents()
    if len(parts) != 1:
        raise template.TemplateSyntaxError("%r tag requires exactly one arguments" % token.contents.split()[0])
    return RemoveSessionMessageNode()
