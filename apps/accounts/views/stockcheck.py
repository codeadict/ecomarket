# coding=utf-8
from datetime import datetime
import pytz
import logging

from accounts.context_processors import _get_days_to_next_stockcheck
from accounts.forms import LoginForm
from accounts.views import SESSION_EXPIRY
from django.contrib.auth import authenticate, login

from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.views.generic.base import TemplateView
from django.db.models import Q
from django.contrib import messages

from main.utils.decorators import view_dispatch_decorator
from main.utils import mixpanel_track
from marketplace.models import Product, StallStatusLog

from accounts.utils import seller_account_required
from apps.accounts.views.selling import SellingBaseView
from notifications import Events


logger = logging.getLogger(__name__)


def stockcheck_start(request, template_name='accounts/stockcheck/landing.html'):
    """
    Allow a user to log in with either username/email and password.

    """
    next_url = reverse('stockcheck_update')
    context = {
        'next': next_url,
        'social_login_error': int(request.GET.get('social-login-error', 0)),
    }

    mixpanel_track(
        request,
        'Clicked CTA In Renewal Email'
    )

    data = request.POST or None
    login_form = LoginForm(data=data)

    if request.user.is_authenticated():
        return HttpResponseRedirect(next_url)

    if login_form.is_valid():
        username = login_form.cleaned_data.get('username', None)
        password = login_form.cleaned_data.get('password', None)

        user = authenticate(username=username, password=password)
        login_success = user and not user.is_anonymous()
        if login_success:
            login(request, user)
            Events(request).logged_in(user)
            if not request.POST.get('remember_me', None):
                expiry = 0
            else:
                expiry = SESSION_EXPIRY

            request.session.set_expiry(expiry)
            return HttpResponseRedirect(next_url)

    context.update({'login_form': login_form})

    return render(request, template_name, context)


@view_dispatch_decorator(seller_account_required)
class StockcheckUpdateView(SellingBaseView):
    model = Product
    template_name = 'accounts/stockcheck/update.html'
    paginate_by = 10000

    def get_queryset(self):
        """
        It is important that the page is sorted by a field that does not change.
        "id" in this case. Pagination would not work correctly if we used "updated"
        as it is used in parent.
        """
        return Product.objects.filter(
            Q(status=Product.PUBLISHED_LIVE) | Q(status=Product.PUBLISHED_SUSPENDED),
            stall=self.stall,
        ).order_by("title")

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return HttpResponseRedirect(
                reverse('stockcheck_landing')
            )

        # Handle stall owners who have no products at all
        # https://app.asana.com/0/8319277024263/8336587616129
        if not request.user.stall.products.count():
            messages.info(request, 'It seems like you are trying to do a stock '
                'check but you have no products listed. You are not required to do '
                'a stock check at the moment.')
            return HttpResponseRedirect(
                reverse('selling')
            )

        # Handle stall owners with just unpublished products
        # https://app.asana.com/0/8319277024263/8336587616134
        if (not request.user.stall.products.filter(status=Product.PUBLISHED_LIVE).count() and
            not request.user.stall.products.filter(status=Product.PUBLISHED_SUSPENDED).count()):
            messages.info(request, 'It seems like you are trying to do a stock '
                'check but you have no live or out of stock products. You cannot '
                'do a stock check on unpublished products (since they are '
                'completely removed from Eco Market) so first you must republish '
                'them, then you may do a stock check on these items. You can '
                '<a href="%(url)s" target="_blank">read more</a> about the difference between '
                'unpublishing items and editing stock.' % dict(
                    url='http://help.ecomarket.com/customer/portal/articles/1346382'
                ))
            return HttpResponseRedirect(
                reverse('selling')
            )

        mixpanel_track(
            request,
            'Viewed Stockcheck Page'
        )

        messages.success(self.request, 'Thanks for helping us keep your items up to date on Eco Market. '
            'To find out more on what this stock check is and a video tutorial explaining how '
            'to use them you can see this <a href="%(url)s" target="_blank">help centre article</a>.' % dict(
                url='http://help.ecomarket.com/customer/portal/articles/1342284'
            ))

        return super(StockcheckUpdateView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """
        ListView by default doesn't automatically handle POST via FormMixin etc.
        Hence over-riding it to handle bulk-edits + success redirect.
        """
        current_page = int(request.POST.get('page', 1))
        ids = request.POST.getlist('ids')
        action = request.POST.get('action')
        if ids and action == self.Action.STOCK:
            queryset = self.get_queryset().filter(pk__in=ids).order_by('title')
            stock_data = request.POST.getlist('stock_data')
            self._update_stock(queryset, stock_data)

            paginator, page, queryset, is_paginated = self.paginate_queryset(self.get_queryset(), self.paginate_by)

            if current_page < paginator.num_pages:
                next_page = current_page + 1
                return HttpResponseRedirect(
                    '%s?page=%d' % (reverse('stockcheck_update'), next_page)
                )
            else:
                self._confirm_stock_check()
                return HttpResponseRedirect(
                    reverse('selling_published_live')
                )

    def _update_stock(self, queryset, stock_data):
        """
        Updates a stalls stock

        :param queryset:
        :param stock_data:
        :return:
        """
        counter = 0
        for product in queryset.iterator():
            raw_stock = stock_data[counter]
            if raw_stock == "-1":
                stock = None
            else:
                stock = int(raw_stock)

            if product.stock != stock:
                Product.objects.filter(id=product.id).update(stock=stock)

            counter += 1

    def _confirm_stock_check(self):
        """
        Updates the stalls last stock check datetime.

        :return:
        """
        now = datetime.now(tz=pytz.utc)
        self.stall.last_stock_checked_at = now

        # If the stall is at a very frequent stock check level,
        # then move them to a 30 day level after a successful
        # stock check is complete.
        if self.stall.renewal_tier < 3:
            self.stall.renewal_tier = 3
        
        if self.stall.is_suspended:
            self.stall.products.filter(
                status=Product.PUBLISHED_SUSPENDED
            ).update(
                status=Product.PUBLISHED_LIVE,
                updated=now
            )
            self.stall.is_suspended = False

            status = StallStatusLog()
            status.stall = self.stall
            status.renewal_tier = self.stall.renewal_tier
            status.is_suspended = False
            status.reason_for_suspension = None
            status.updated_at = now
            status.save()
        self.stall.save()

        mixpanel_track(
            self.request,
            'Renewed Products',
        )

        messages.success(self.request, 'Thanks! Your stock check is done. '
           'You will need to do another stock check within the next %d days. '
           'We do however suggest that if your inventory changes frequently '
           'that you log in to Eco Market and and do these stock checks more often. '
           'You can do a stock check as many times as you like at any time, '
           'but at the moment you as required to do one every 30 days to keep '
           'your products live in our marketplace.'
           % _get_days_to_next_stockcheck(self.request))