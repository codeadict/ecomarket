from django import template

from apps.social_network.models import UserFollow


class FollowUserButtonOutput(template.Node):
    def __init__(self, user=None):
        self.user_variable = template.Variable(user)

    def render(self, context):
        t = template.loader.get_template('user_follow_button.html')
        user = self.user_variable.resolve(context)
        return t.render(template.Context(
            {'user': user},
            autoescape=context.autoescape)
        )


class ShowOptionalFollowButtonOutput(template.Node):
    def __init__(self, user,user_to_follow):
        self.user_variable = template.Variable(user)
        self.user_to_follow_variable = template.Variable(user_to_follow)

    def render(self, context):
        t = template.loader.get_template('user_follow_button.html')
        user = self.user_variable.resolve(context)
        user_to_follow = self.user_to_follow_variable.resolve(context)

        not_friends = user != user_to_follow and not UserFollow.relation_exists(user, user_to_follow)
        t = template.loader.get_template('user_follow_button.html')
        return t.render(template.Context(
            {
                'user': user_to_follow,
                'not_friends': not_friends
            },
            autoescape=context.autoescape)
        )
        return ''


def show_follow_button(parser, token):
    """
    A templatetag to show a follow button to a given user.
    
    Usage::
    
        {% load follow_utils %}
        {% show_follow_button user%}
    """
    bits = token.contents.split()
    if len(bits) != 2:
        raise template.TemplateSyntaxError, "inbox_count tag takes exactly two arguments"
    user = bits[1]
    return FollowUserButtonOutput(user)


def show_follow_or_following_button(parser, token):
    """
    A templatetag to optionally show a button to follow a given user only if
    the user does not follow the other.

        Usage::

        {% load follow_utils %}
        {% show_follow_or_following_button user canditate_user_to_follow %}
    """
    bits = token.contents.split()
    if len(bits) != 3:
        raise template.TemplateSyntaxError, "inbox_count tag takes exactly three arguments"
    user = bits[1]
    candidate_user = bits[2]
    return ShowOptionalFollowButtonOutput(user, candidate_user)


register = template.Library()

register.tag('show_follow_button', show_follow_button)
register.tag('show_follow_or_following_button', show_follow_or_following_button)
