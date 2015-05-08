# encoding: utf-8
from datetime import timedelta

from django import template
from django.template.defaultfilters import slugify
from django.contrib.contenttypes.models import ContentType

from actstream.models import Action

from main.utils.actions import related_actions

register = template.Library()


class TemplateForAction(template.Node):
    def __init__(self, action, var_name, *args, **kwargs):
        super(TemplateForAction, self).__init__(*args, **kwargs)
        self.action = template.Variable(action)
        self.var_name = var_name

    def render(self, context):
        base = 'accounts/profile/fragments/_activity_%s_%s.html'
        action = self.action.resolve(context)
        model = slugify(action.action_object_content_type.name)
        verb = slugify(action.verb)
        context[self.var_name] = base % (model, verb)
        return ''


@register.tag
def get_template_for_action(parser, token):
    parts = token.split_contents()
    if len(parts) != 4:
        tag_name = parts[0]
        raise template.TemplateSyntaxError(
                "%r tag usage: %r action as var "
                % (tag_name, tag_name))

    _, action, _, var_name = token.split_contents()
    return TemplateForAction(action, var_name)


@register.assignment_tag(takes_context=True)
def get_related_actions(context, action):
    """
    A templatetag to optionally show a button to follow a given user only if
    the user does not follow the other.

        Usage::

        {% load action_filters %}
        {% get_related_actions action as actions %}
    """
    related_actions_list = related_actions(action)
    total_actions = related_actions_list.count() + 1
    context['total_actions'] = total_actions
    return related_actions_list


register.assignment_tag(takes_context=True)(get_related_actions)


@register.assignment_tag
def get_ctype_and_id(action):
    """
    For every action, we take out the needed action_object or target ids
    and their content type ids. These are needed for comments system.
    """
    action_object_ctype = ContentType.objects.get_for_model(action.action_object)
    data = dict(
        action_object_ctype_id=action_object_ctype.id,
        action_object_id=action.action_object.id
    )
    if str(action.verb) == 'wrote':
        data.update(dict(
            ctype_id=action_object_ctype.id,
            object_id=action.action_object.id
        ))
        return data
    elif str(action.verb) == 'listed a new product on':
        ctype = ContentType.objects.get_for_model(action.target.user.get_profile())
        data.update(dict(
            ctype_id=ctype.id,
            object_id=action.target.user.get_profile().id
        ))
        return data
    elif str(action.verb) == 'created the love list':
        data.update(dict(
            ctype_id=action_object_ctype.id,
            object_id=action.action_object.id
        ))
        return data
    elif str(action_object_ctype) == 'threaded comment':
        data.update(dict(
            ctype_id=action_object_ctype.id,
            object_id=action.action_object.id
        ))
        return data
    elif action.target:
        ctype = ContentType.objects.get_for_model(action.target)
        data.update(dict(
            ctype_id=ctype.id,
            object_id=action.target.id
        ))
        return data
    else:
        data.update(dict(
            ctype_id=action_object_ctype.id,
            object_id=action.action_object.id
        ))
        return data