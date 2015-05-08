ACTIVITIES_PAGE_SIZE = 10

import datetime
import json
import random

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django.core.cache import cache
from django.db.models import Q

from actstream.models import Action

from notifications import Events

from apps.main.utils.actions import get_excluded_action_list
from apps.social_network.models import UserFollow


class JsonResponse(HttpResponse):

    default_content_type = "application/json; charset=%s" % \
        settings.DEFAULT_CHARSET

    def __init__(self, content=None, **kwargs):
        content_type = kwargs.pop("content_type", self.default_content_type)
        super(JsonResponse, self).__init__(
            content=json.dumps(content), content_type=content_type, **kwargs)

@login_required
def follow(request, user_id):
    if request.method == "POST":
        follow_user = User.objects.get(pk=user_id)

        if follow_user == request.user:
            return JsonResponse({"status": "KO",
                                 "error_message": "You cannot become friends with yourself",
                                 'user': request.user.pk,
                                'other_user': follow_user.pk
            })

        relation_exists = UserFollow.relation_exists(request.user, follow_user)

        if relation_exists:
            return JsonResponse({"status": "KO", "error_message": "You cannot become friends with a user you follow."})
        follow = UserFollow(user=request.user, target=follow_user)
        follow.save()
        Events(request).user_followed(follow)
        return JsonResponse({"status": "OK"})

@login_required
def unfollow(request, user_id):
    if request.is_ajax() and request.method == "POST":
        unfollow_user = User.objects.get(pk=user_id)

        if unfollow_user == request.user:
            error_message = "You cannot stop being friends with yourself " \
                            "because you cannot be friends with yourself"
            return JsonResponse({"status": "KO", "error_message": error_message})

        relation_exists = UserFollow.relation_exists(request.user, unfollow_user)

        if not relation_exists:
            error_message = "You cannot stop being friends with someone you are not friends with."
            return JsonResponse({"status": "KO", "error_message": error_message})

        relation = UserFollow.objects.get(user=request.user, target=unfollow_user)
        Events(request).user_unfollowed(relation)
        relation.delete()

        return JsonResponse({"status": "OK"})

@login_required
def try_become_friends(request, user_id):
    redirect_url = request.GET.get('follow')
    follow_user = get_object_or_404(User, pk=user_id)

    if follow_user != request.user:
        relation_exists = UserFollow.relation_exists(request.user, follow_user)
        if not relation_exists:
            follow = UserFollow(user=request.user, target=follow_user)
            follow.save()
            Events(request).user_followed(follow)
            messages.success(request, 'Thanks, you have been logged in and you are '
                                      'now following %s' % follow_user.username)

    return HttpResponseRedirect(redirect_url)


@login_required
def activities(request):
    cache.delete(settings.CACHE_KEY_ACTIVITIES_COUNT % request.user.id)
    context = dict()
    user_profile = request.user.get_profile()
    user_profile.last_activities_update = datetime.datetime.now()
    user_profile.save()

    user_follows = list(UserFollow.objects.filter(user=request.user))
    profile_follows_ids = [follow.target.id for follow in user_follows]

    content_type = ContentType.objects.get_for_model(request.user)

    user_actions = Action.objects.filter(
        Q(public=True),
        Q(actor_object_id__in=profile_follows_ids) | Q(target_object_id__in=profile_follows_ids,
                                                        target_content_type_id=content_type.id)
    ).exclude(actor_object_id=request.user.id).order_by('-id')
    context = {'request': request}

    if not user_follows:
        context.update({
            'follow_suggestions': list(UserFollow.get_follow_candidates(request.user))
        })
        request_context = RequestContext(request, context)
        return render_to_response('no_activity.html',
                                  context_instance=request_context)

    excluded_action_pks = get_excluded_action_list(user_actions)
    user_bulked_actions = user_actions.exclude(pk__in=excluded_action_pks)

    followers = UserFollow.objects.filter(target=request.user)

    paginator = Paginator(user_bulked_actions, ACTIVITIES_PAGE_SIZE)

    page = request.GET.get('page', 1)
    try:
        user_bulked_actions = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        user_bulked_actions = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        user_bulked_actions = []

    # This user saw their activities right now, take note of that
    user_profile = request.user.get_profile()
    user_profile.activities_last_checked_at = datetime.datetime.now()
    user_profile.save()

    context.update({
        'activities': user_bulked_actions,
        'profile': request.user.get_profile(),
        'followers': followers[:6],
        'followers_count': followers.count(),
        'following': user_follows[:6],
        'following_count': len(user_follows),
        'page_obj': user_bulked_actions,
        'current_page': int(page),
        'page_count': paginator.num_pages,
        'is_activity_page': True,
    })

    request_context = RequestContext(request, context)

    return render_to_response('activity_page.html',
                              context_instance=request_context)


class UserNewActivitiesCount(TemplateView):
    template_name = 'fragments/_new_activities_count.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(UserNewActivitiesCount, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(UserNewActivitiesCount, self).get_context_data(**kwargs)
        context['activities_count'] = 10
        return context
