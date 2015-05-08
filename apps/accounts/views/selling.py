from datetime import datetime
import logging

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic.base import TemplateView, RedirectView
from django.views.generic.edit import UpdateView
from django.views.generic.list import ListView
from django.contrib import messages

from main.utils.decorators import view_dispatch_decorator
from main.utils import DynamicPaginationMixin
from marketplace.models import Product, Stall

from accounts.utils import seller_account_required

logger = logging.getLogger(__name__)


class SellingRedirectView(RedirectView):
    permanent = False
    query_string = True

    def get_redirect_url(self):
        return reverse('selling_published_live')


@view_dispatch_decorator(seller_account_required)
class SellingBaseView(DynamicPaginationMixin, ListView):
    model = Product
    template_name = "accounts/selling/product_list.html"
    paginate_by = 10

    def __init__(self):
        super(SellingBaseView, self).__init__()
        self.publish_errors = 0
        self.ids = []

    @property
    def stall(self):
        try:
            return self.request.user.stall
        except Stall.DoesNotExist:
            return None

    class Action:
        PUBLISH = 'publish'
        UNPUBLISH = 'unpublish'
        CHANGE_SHIPPING = 'change_shipping'
        STOCK = 'stock'
        PRICE = 'price'
        DELETE = 'delete'
        SUSPEND = 'suspend'

    def get_queryset(self):
        return Product.objects.filter(
            stall=self.stall).order_by("-updated")

    def get_context_data(self, **kwargs):
        context = super(SellingBaseView, self).get_context_data(**kwargs)

        # Get the unfiltered queryset
        # for current user: TODO::;;;;;;;;;;;;;;;;;;;;;
        queryset = Product.objects.filter(stall=self.request.user.stall)
        #queryset = super(SellingBaseView, self).get_queryset()
        context.update({
            'live_count': queryset.live().exclude(stock=0).count(),
            'unpublished_count': queryset.unpublished().count(),
            'sold_out_count': queryset.sold_out().count(),
            'suspended_count': queryset.suspended().count(),
            'Action': self.Action,
        })
        return context

    def get_success_url(self):
        if self.success_url:
            url = self.success_url
        else:
            raise ImproperlyConfigured(
                "No URL to redirect to. Provide a success_url.")
        return url

    def post(self, request, *args, **kwargs):
        """
        ListView by default doesn't automatically handle POST via FormMixin etc.
        Hence over-riding it to handle bulk-edits + success redirect.
        """
        ids = request.POST.getlist('ids')
        self.ids = ids
        action = request.POST.get('action')
        if ids:
            queryset = self.get_queryset().filter(pk__in=ids)
            timestamp = datetime.now()
            if action == self.Action.PUBLISH:
                # If stall is suspended, do not publish live, be silent.
                if not self.stall.is_suspended:
                    for obj in queryset:
                        if obj.flag is not None:
                            self._found_flagged_product()
                            continue

                        obj.status = Product.PUBLISHED_LIVE
                        obj.updated = timestamp
                        obj.save()
            elif action == self.Action.UNPUBLISH:
                for obj in queryset:
                    obj.status = Product.PUBLISHED_UNPUBLISHED
                    obj.updated = timestamp
                    obj.save()
            elif action == self.Action.DELETE:
                for obj in queryset:
                    obj.status = Product.PUBLISHED_DELETED
                    obj.updated = timestamp
                    obj.save()
            elif action == self.Action.STOCK:
                value = request.POST.get('stock') or None
                if 'stock' in request.POST or value:  # stock=None means unlimited
                    if value:
                        value = int(value)
                    for obj in queryset:
                        obj.stock = value
                        obj.updated = timestamp
                        obj.save()
            elif action == self.Action.PRICE:
                value = request.POST.get('price') or None
                if value:
                    value = int(value)
                    for product in queryset:
                        price = product.get_price_instance()
                        price.amount = value
                        price.save()
                    #queryset.update(price=price, updated=timestamp)
            else:
                raise Exception('Invalid action')

        if self.publish_errors:
            self._add_flag_message()

        return HttpResponseRedirect(self.get_success_url())

    def render_to_response(self, request, *args, **kwargs):
        if not self.stall:
            return redirect('create_stall')

        return super(SellingBaseView, self).render_to_response(request, *args, **kwargs)

    def _found_flagged_product(self):
        self.publish_errors += 1

    def _add_flag_message(self):
        msg = """Sorry we could not publish %d of your products.
 We have listed the reasons below so just scroll down to fix these
 problems and try again.""" % self.publish_errors

        remaining_ids = len(self.ids) - self.publish_errors
        if remaining_ids > 0:
            msg += " [%d of your products however did get published successfully]" % remaining_ids

        messages.error(
            self.request,
            msg
        )


class SellingPublishedLiveView(SellingBaseView):

    def get_queryset(self):
        queryset = super(SellingPublishedLiveView, self).get_queryset()
        queryset = queryset.live().exclude(stock=0)
        return queryset

    def get_success_url(self):
        return reverse('selling_published_live')


class SellingUnpublishedView(SellingBaseView):

    def get_queryset(self):
        queryset = super(SellingUnpublishedView, self).get_queryset()
        queryset = queryset.unpublished()
        return queryset

    def get_success_url(self):
        return reverse('selling_unpublished')


class SellingSoldOutView(SellingBaseView):

    def get_queryset(self):
        queryset = super(SellingSoldOutView, self).get_queryset()
        queryset = queryset.sold_out()
        return queryset

    def get_success_url(self):
        return reverse('selling_sold_out')
