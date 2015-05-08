BULK_ACTION_VERBS = (
    'listed a new product on',
    'added product to love list',
)

from datetime import timedelta

from actstream.models import Action


def get_excluded_action_list(actions):
    """
    Returns a list with all of the pks of the actions to exclude due
    the action verbs, as sometimes some activities need to be bulked
    :param actions: The actions queryset
    :return: A list of int with all of the primary keys of the actions to exclude
    """
    excluded_actions_pks = []
    for action in actions:
        if action.verb == 'created the love list':
            excluded_actions_pks.append(action.pk)
            continue
        related_actions_list = related_actions(action)
        if action.verb in BULK_ACTION_VERBS and action.pk not in excluded_actions_pks:
            for related_action in related_actions_list:
                if related_action.pk not in excluded_actions_pks:
                    excluded_actions_pks.append(related_action.pk)
    return excluded_actions_pks


def related_actions(action):
    """
    Gets the related actions of a single action
    :param action: The action to look relationships on.
    :return: A queryset containing the related actions
    """
    action_day = action.timestamp
    day_before_action = action_day - timedelta(days=1)
    return Action.objects.filter(
        actor_content_type=action.actor_content_type,
        actor_object_id=action.actor_object_id,
        verb=action.verb,
        timestamp__lte=action_day,
        timestamp__gt=day_before_action,
        target_content_type=action.target_content_type,
        target_object_id=action.target_object_id,
    ).exclude(pk=action.pk)