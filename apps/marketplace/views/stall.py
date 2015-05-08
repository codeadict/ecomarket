import logging
from accounts.models import Video

from notifications import Events

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core.urlresolvers import reverse
from django.conf import settings
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, redirect

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.translation import ugettext as _

from main.utils import absolute_uri
from marketplace.forms import StallForm, StallOwnerProfileForm

from marketplace.models import Category, Stall

logger = logging.getLogger(__name__)

STALL_CREATE_MESSAGE = "Great choice becoming a stall owner. " \
    + "We just need to ask a few tiny questions and you'll be on your way..."

RESULTS_PER_PAGE = getattr(settings, "STALL_PAGINATION",
                           settings.PAGINATION_DEFAULT_PAGINATION)


# Stall views
# ============
@login_required
def create_stall(request, template_name='marketplace/create_stall.html'):
    """
    Handles the first time creation of a stall.
    Also handles some stall owner details which goto UserProfile models.
    """
    context = {}
    user = request.user

    # If stall exists, redirect to edit version
    try:
        stall = user.stall
        if stall:
            return redirect('edit_stall', stall.slug)
    except:
        stall = None

    profile_form = StallOwnerProfileForm(
        request.POST or None, instance=user.get_profile())
    creation_form = StallForm(request.POST or None)

    if request.method == "POST":
        # Forcing all to validate to populate errors
        profile_form.is_valid() or creation_form.is_valid()

        if profile_form.is_valid() and creation_form.is_valid():
            profile_form.save()
            stall = creation_form.save(commit=False)
            stall.user = request.user
            stall.save()
            user_email = request.user.email_notification

            if stall.email_opt_in:
                user_email.stall_owner_tips = True
            else:
                user_email.stall_owner_tips = False
            user_email.save()

            if not stall.user.get_profile().is_activated():
                stall.user.todos.create(view_name="validate_email")

            Events(request).stall_opened(stall)

            request.session.pop('new_user', None)
            request.session['new_seller'] = True
            return HttpResponseRedirect(reverse('profile') + '?openStallSuccess=true')
    else:
        if not (profile_form.is_valid() or creation_form.is_valid()):
            messages.info(request, STALL_CREATE_MESSAGE)

    context.update({
        'profile_form': profile_form,
        'creation_form': creation_form})

    return render(request, template_name, context)


@login_required
def edit_stall(request, slug, template_name='marketplace/edit_stall.html'):
    """
    Handles the edit page for a stall.
    The stall owner edit is handled via another dashboard tab.
    """
    context = {}
    stall = get_object_or_404(Stall, slug=slug, user=request.user, is_closed=False)
    edit_form = StallForm(request.POST or None, instance=stall)

    if request.method == "POST":
        if edit_form.is_valid():
            stall = edit_form.save()
            messages.success(request, _(u"Stall was updated successfully!"))
            return redirect('edit_stall', stall.slug)

    context.update({
        'stall': stall,
        'edit_form': edit_form})

    return render(request, template_name, context)


def my_stall(request, slug):
    stall = get_object_or_404(Stall, slug=slug)
    if stall.is_closed:
        messages.info(
            request,
            'Oops - it looks like the stall you are trying to find '
            'has closed down. We\'re sorry about that, but we have good news, there '
            'are plenty more to pick from and we have thousands of stall owners on '
            'Eco Market. Try discovering products below or you can use our search in '
            'the top of the page to search for items directly.'
        )
        return HttpResponseRedirect(reverse('category_discover'))
    if stall.slug != slug:
        return redirect(stall, permanent=True)

    products = (stall.products.live()
                .select_related('stall__identifier')
                .prefetch_related('prices'))
    suggested_categories = Category.sort_by_popularity(
            Category.objects.filter(products__in=products)
                    .distinct())[:5]

    product_count = products.count()
    paginator = Paginator(products, RESULTS_PER_PAGE)

    def redirect_me(page):
        return HttpResponseRedirect(
            "{url}?page={page}".format(url=reverse("my_stall", args=(slug, )), page=page)
        )

    try:
        current_page = request.GET.get('page', 1)
        products = paginator.page(current_page)
    except PageNotAnInteger:
        return redirect_me(page=1)
    except EmptyPage:
        products = []

    try:
        video = stall.user.videos.all()[0]
    except IndexError:
        video = None

    context = {
        'self_url': request.path,
        'stall': stall,
        'object': stall,
        'suggested_categories': suggested_categories,
        'product_count': product_count,
        'current_page': current_page,
        'page_count': paginator.num_pages,
        'products': products,
        'video': video,
    }
    return render(request, 'marketplace/my_stall.html', context)
