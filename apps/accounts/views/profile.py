import logging

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType

from django.core.urlresolvers import reverse
from django.http import HttpResponseBadRequest
from django.shortcuts import render, redirect


from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext

from accounts.forms import DetailedUserProfileForm
from accounts.models import UserProfile

from main.utils.decorators import view_dispatch_decorator
from main.utils.actions import get_excluded_action_list

from image_crop.views import FileUploaderAjax
from image_crop.utils import validate_uploaded_image
from image_crop.exceptions import ImageUploadError

from apps.social_network.models import UserFollow

from actstream.models import Action


logger = logging.getLogger(__name__)

NEW_USER_MESSAGE = 'Super! You are now signed up to Eco Market, ' \
    + 'its a pleasure to have you on board! Before you go off to celebrate, ' \
    + 'now is a great time to fill out your profile and ' \
    + 'upload a nice picture of yourself. We hope you enjoy our marketplace.'
NEW_SELLER_MESSAGE = 'Super! You are now a stall owner on Eco Market, ' \
    + 'its a pleasure to have you on board! Before you go off to celebrate, ' \
    + 'now is a great time to fill out your profile and upload ' \
    + 'a nice friendly picture of yourself for your customers. ' \
    + 'Our customers love a personal experience so do spend some time ' \
    + 'in this my account area as we find that stall owners who do this ' \
    + 'normally tend to sell more products!'


@login_required
def profile(request, template_name='accounts/profile/profile.html'):
    if hasattr(request.user, "stall") and request.user.stall.is_closed:
        return redirect('home')
    try:
        user_profile = request.user.get_profile()
    except UserProfile.DoesNotExist:
        user_profile = UserProfile.objects.create(user=request.user)

    user_profile_form = DetailedUserProfileForm(instance=user_profile)
    if request.POST:
        user_profile_form = DetailedUserProfileForm(
            request.POST, request=request, instance=user_profile)
        if user_profile_form.is_valid():
            user_profile_form.save()
            return redirect(reverse('profile'))

    # was set in register, may be removed in create_stall
    new_user = request.session.pop('new_user', False)

    # was set in create_stall
    new_seller = request.session.pop('new_seller', False)

    if new_user:
        messages.success(request, NEW_USER_MESSAGE)
    if new_seller:
        messages.success(request, NEW_SELLER_MESSAGE)

    context = {
        'user_profile_form': user_profile_form,
        'new_user': new_user,
        'new_seller': new_seller,
        'hold_fire': request.GET.get('add-product') is not None
    }
    return render(request, template_name, context)


def public_profile(request, username):
    profile_user = get_object_or_404(User, username=username)

    if hasattr(profile_user, 'stall') and profile_user.stall.is_closed:
        return redirect('home')

    if profile_user.username != username:
        return redirect(reverse('public_profile', kwargs={
            'username': profile_user.username}), permanent=True)

    show_follow_login = False
    follow_url = None
    follow = bool(request.GET.get('follow', False))
    if follow:
        if request.user.is_anonymous():
            follow_url = "%s?next=%s?follow=%s" % (reverse('login'),
                                                   reverse('try_become_friends_with', args=[profile_user.pk]),
                                                   request.path)
            show_follow_login = True
        else:
            follow_url = "%s?follow=%s" % (reverse('try_become_friends_with', args=[profile_user.pk]),
                                           request.path)
            return redirect(follow_url)

    profile = profile_user.get_profile()
    content_type = ContentType.objects.get_for_model(profile)
    actions = (Action.objects.filter(actor_object_id=profile_user.id)
               | Action.objects.filter(target_object_id=profile.id,
                                       target_content_type_id=content_type.id))
    actions = actions.prefetch_related('actor_content_type',
                                       'target_content_type',
                                       'action_object_content_type',
                                       'action_object', 'actor', 'target')

    excluded_action_pks = get_excluded_action_list(actions)
    user_bulked_actions = actions.exclude(pk__in=excluded_action_pks)

    followers = UserFollow.user_following(profile_user)
    followers_count = followers.count()
    following = UserFollow.user_follow(profile_user)
    following_count = following.count()

    love_lists = (profile_user.love_lists
                  .filter(is_public=True)
                  .exclude(products=None)
                  .select_related('primary_category__slug'))

    return render_to_response('accounts/profile/public_profile.html', {
        'profile_user': profile_user,
        'love_lists': love_lists,
        'activities': user_bulked_actions,
        'followers': followers[:6],
        'followers_count': followers_count,
        'following': following[:6],
        'following_count': following_count,
        'show_follow_login': show_follow_login,
        'follow_url': follow_url
    }, context_instance=RequestContext(request))


@view_dispatch_decorator(login_required)
class AvatarUploaderAjax(FileUploaderAjax):

    def post(self, request):
        try:
            filename, upfile = self._posted_image(request)
        except KeyError:
            return HttpResponseBadRequest("AJAX request not valid")

        try:
            validate_uploaded_image(
                upfile, min_width=228, min_height=228)
        except ImageUploadError, e:
            return self._fail_response(e)

        try:
            return self._success_response(
                filename,
                self._save_temp_image(request, filename, upfile))
        except:
            return HttpResponseBadRequest("AJAX request not valid")
