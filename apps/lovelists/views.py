from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.views.generic import (
        DeleteView as DeleteViewBase, FormView, UpdateView, View)

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
import django.utils.simplejson as json

from marketplace.models import Product

from lovelists.exceptions import TooManyOwnProductsLoved
from lovelists.models import LoveList, LoveListProduct
import lovelists.forms as forms


class JsonResponse(HttpResponse):

    default_content_type = "application/json; charset=%s" % \
        settings.DEFAULT_CHARSET

    def __init__(self, content=None, **kwargs):
        content_type = kwargs.pop("content_type", self.default_content_type)
        return super(JsonResponse, self).__init__(
            content=json.dumps(content), content_type=content_type, **kwargs)


@login_required
def main(request):
    return redirect("lovelist:lists", request.user.username)


def user_lists(request, user, template_name):
    if request.user == user:
        lists = user.love_lists.all()
    else:
        lists = user.love_lists.filter(is_public=True).exclude(products=None)
    if not lists.count():
        template_name = "lovelists/no_lists.html"
    return render(request, template_name, {
        "owner": user,
        "lists": lists,
    })


def product_lists(request, product, template_name):
    lists = product.love_lists.filter(is_public=True)
    if not lists.count():
        raise Http404("No love list found for this product")
    return render(request, template_name, {
        "product": product,
        "lists": lists,
    })


def lists(request, identifier, template_name="lovelists/lists.html"):
    try:
        user = User.objects.get(username=identifier)
    except User.DoesNotExist:
        product = get_object_or_404(Product, slug=identifier)
        return product_lists(request, product, template_name)
    return user_lists(request, user, template_name)


def view(request, identifier, category=None, slug=None,
         template_name="lovelists/love_list.html"):
    love_list = None
    if request.user.is_authenticated():
        try:
            # Include private lists for the current user
            love_list = request.user.love_lists.get(identifier=identifier)
        except LoveList.DoesNotExist:
            pass
    if love_list is None:
        love_list = get_object_or_404(LoveList, identifier=identifier,
                                      is_public=True)
    needs_redirect = (category is None or slug is None
                      or love_list.primary_category.slug != category
                      or love_list.slug != slug)
    if needs_redirect:
        return redirect(love_list.get_absolute_url(), permanent=True)
    if love_list.products.count() == 0 and request.user != love_list.user:
        raise Http404("No products in love list")
    return render(request, template_name, {
        "love_list": love_list,
    })


class EditView(UpdateView):

    form_class = forms.LoveListForm
    template_name = "lovelists/edit.html"

    def get_object(self):
        return get_object_or_404(self.request.user.love_lists,
                                 identifier=self.kwargs["identifier"])

    def get_context_data(self, **kwargs):
        original_context = super(EditView, self).get_context_data(**kwargs)
        return {
            "love_list": original_context["lovelist"],
            "form": original_context["form"],
        }

edit = login_required(EditView.as_view())


class DeleteView(DeleteViewBase):

    def get_object(self):
        return get_object_or_404(self.request.user.love_lists,
                                 identifier=self.kwargs["identifier"])

    def get_success_url(self):
        return reverse("lovelist:main")

delete = login_required(DeleteView.as_view())


def _check_own_products_loved(user, love_list):
    """Verify that the list does not contain over 50% products from the user
    """
    limit = love_list.products.count() // 2
    owned_count = love_list.products.filter(stall=user.stall).count()
    if owned_count > limit:
        raise TooManyOwnProductsLoved(limit)


def add_product_to_list(request, product_slug, identifier=None):
    product = get_object_or_404(Product, slug=product_slug)
    lists = request.user.love_lists
    if identifier is None:
        love_list = lists.all()[0]
    else:
        love_list = get_object_or_404(lists, identifier=identifier)
    if (request.user.get_profile().is_seller
            and product in request.user.stall.products.all()):
        _check_own_products_loved(request.user, love_list)
    rel, created = LoveListProduct.objects.get_or_create(
        product=product, love_list=love_list)
    if not created:
        rel.weight = 0
    rel.save()  # Set the weight
    love_list.save()  # Set the updated date
    return created, product


class JsonTemplateResponse(FormView.response_class):

    def __init__(self, *args, **kwargs):
        self.response_data = kwargs.pop("response_data", {})
        if not "content_type" in kwargs:
            kwargs["content_type"] = JsonResponse.default_content_type
        super(JsonTemplateResponse, self).__init__(*args, **kwargs)

    @property
    def rendered_content(self):
        context = self.resolve_context(self.context_data)
        content = render_to_string(self.template_name,
                                   context_instance=context)
        data = self.response_data.copy()
        data["html"] = content
        return JsonResponse(data)


def _get_mixpanel_data_for_product(product):
    def get_value(manager, attr_name):
        return [value for value, in manager.values_list(attr_name)]

    return {
        "Title": product.title,
        "Description": product.description,
        "Main Category": (product.primary_category.slug
                          if product.primary_category else None),
        "Secondary Category": (product.secondary_category.slug
                               if product.secondary_category else None),
        "Product Causes": get_value(product.causes, "slug"),
        "Photos": product.images.count(),
        "Main Colours": get_value(product.colors, "slug"),
        "Keywords": get_value(product.keywords, "slug"),
        "Recipients": get_value(product.recipients, "slug"),
        "Price": product.price.amount.amount,
        "Unlimited Stock": product.stock is None,
        "Number in Stock": product.stock,
        "Product Ships From": product.ships_from_country,
        "Ships Worldwide": product.shipping_profile.ships_worldwide(),
    }


class AjaxLoveListSelectView(FormView):

    template_name = "lovelists/fragments/love_list_select.html"
    form_class = forms.LoveListForm
    response_class = JsonTemplateResponse

    def get_initial(self):
        initial = super(AjaxLoveListSelectView, self).get_initial()
        if "is_public" not in initial:
            initial["is_public"] = self.request.user.privacy.love_list_public
        return initial

    def get_context_data(self, **kwargs):
        context = \
            super(AjaxLoveListSelectView, self).get_context_data(**kwargs)
        product_slug = self.request.POST.get("product_slug",
                       self.kwargs["product_slug"])
        context.update({
            "lists": self.request.user.love_lists.all(),
            "product_slug": product_slug,
        })
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        love_list = form.save()
        product_slug = self.request.POST.get("product_slug", None)
        data = {
            "success": True,
            "product_slug": product_slug,
        }
        if product_slug is not None:
            try:
                created, product = add_product_to_list(
                    self.request, product_slug=product_slug,
                    identifier=love_list.identifier)
            except TooManyOwnProductsLoved, e:
                return JsonResponse({
                    "reason": e.error_dialog_text,
                }, status=403)
            data["created"] = created
            data["product_mixpanel_data"] = \
                _get_mixpanel_data_for_product(product)
        return JsonResponse(data)

    def post(self, request, *args, **kwargs):
        love_list_identifier = request.POST.get("lovelist_choice", "new")
        if love_list_identifier != "new" \
           and "product_slug" in self.request.POST:
            product_slug = self.request.POST["product_slug"]
            try:
                created, product = add_product_to_list(
                    self.request, product_slug=product_slug,
                    identifier=love_list_identifier)
            except TooManyOwnProductsLoved, e:
                return JsonResponse({
                    "reason": e.error_dialog_text,
                }, status=403)
            return JsonResponse({
                "success": True,
                "product_slug": product_slug,
                "created": created,
                "product_mixpanel_data":
                    _get_mixpanel_data_for_product(product),
            })
        return super(AjaxLoveListSelectView, self).post(
            request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        if settings.DEBUG and request.GET.get("html") == "true":
            # Return HTML instead of JSON, for debugging
            self.response_class = FormView.response_class
        return super(AjaxLoveListSelectView, self).dispatch(
            request, *args, **kwargs)


ajax_love_list_select = login_required(AjaxLoveListSelectView.as_view())


def ajax_current_love_list(request, product_slug=None):
    if request.user.is_authenticated():
        lists = request.user.love_lists.all()
        if lists.count():
            love_list = lists[0]
            data = {
                "action": "show_menu",
                "list_name": love_list.title,
            }
        else:
            data = {"action": "create_new"}
    else:
        data = {"action": "login"}
    try:
        product = Product.objects.get(slug=product_slug)
    except Product.DoesNotExist:
        pass
    else:
        data["product_mixpanel_data"] = _get_mixpanel_data_for_product(product)
    return JsonResponse(data)


class AjaxAddToListView(View):

    def post(self, request, **kwargs):
        try:
            created, product = add_product_to_list(request, **kwargs)
        except TooManyOwnProductsLoved, e:
            return JsonResponse({
                "reason": e.error_dialog_text,
            }, status=403)
        return JsonResponse({
            "created": created,
            "product_mixpanel_data": _get_mixpanel_data_for_product(product),
        })

ajax_add_to_list = login_required(AjaxAddToListView.as_view())


class AjaxRemoveFromListView(View):

    def post(self, request, product_slug, identifier):
        product = get_object_or_404(Product, slug=product_slug)
        love_list = get_object_or_404(LoveList, identifier=identifier)
        try:
            relationship = love_list.product_relationships.get(product=product)
        except LoveList.DoesNotExist:
            return HttpResponseBadRequest()
        relationship.delete()
        return JsonResponse({"products_count": love_list.products.count()})


ajax_remove_from_list = login_required(AjaxRemoveFromListView.as_view())
