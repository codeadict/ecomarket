import logging

from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import login, user_logged_in
from django.contrib.auth.models import User, update_last_login
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt


logger = logging.getLogger(__name__)


IMPERSONATED_BY_KEY = 'impersonated_by'
IMPERSONATING_KEY = 'impersonating'

@staff_member_required
def impersonate(request, user_id):
    """ Allows a superuser to impersonate another user. """
    admin_user = request.user
    user = User.objects.get(id=user_id)

    # Login as the specified user
    user.backend = 'django.contrib.auth.backends.ModelBackend'
    user_logged_in.disconnect(update_last_login)
    login(request, user)
    user_logged_in.connect(update_last_login)

    request.session[IMPERSONATED_BY_KEY] = admin_user.id
    request.session[IMPERSONATING_KEY] = user.id
    messages.success(request, 'Impersonation successful.')
    return HttpResponseRedirect(reverse('home'))


def deimpersonate(request):
    """ Allows a superuser to stop impersonating a user. """
    if not (request.session.get(IMPERSONATING_KEY, None) and request.session.get(IMPERSONATED_BY_KEY, None)):
        return HttpResponseRedirect('/admin')

    user = User.objects.get(id=request.session[IMPERSONATING_KEY])
    admin_user = User.objects.get(id=request.session[IMPERSONATED_BY_KEY])

    # Login back as the admin user
    admin_user.backend = 'django.contrib.auth.backends.ModelBackend'
    login(request, admin_user)
    messages.success(request, 'Impersonation successfully removed.')

    if request.session.has_key(IMPERSONATING_KEY):
        del request.session[IMPERSONATING_KEY]
    if request.session.has_key(IMPERSONATED_BY_KEY):
        del request.session[IMPERSONATED_BY_KEY]

    return HttpResponseRedirect('/admin')
