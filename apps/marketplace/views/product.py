import logging
from discounts.models import FreeShipping
import re

from django.utils.decorators import method_decorator
from django.db import transaction
from django.utils.functional import allow_lazy
from django.utils.encoding import force_unicode
from django.utils import simplejson as json
from django.http import Http404
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, DetailView, UpdateView
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.http import \
    HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

from marketplace.forms import \
    ProductCreationForm, ShippingProfileForm, \
    ProductImagesFormset, \
    ProductSuggestedCertificateFormset, ProductPriceForm, \
    ShippingRulesFormset

from marketplace.models import (
    Product, Price, Keyword, ShippingProfile, Stall, Certificate, Country, CurrencyExchangeRate)
from marketplace import CURRENCY_CHOICES

from mailing_lists.integrations.sailthru import Sailthru
from main.utils.decorators import view_dispatch_decorator
from main.utils import mixpanel_track, mixpanel_engage

from image_crop.views import FileUploaderAjax
from image_crop.utils import validate_uploaded_image
from image_crop.exceptions import ImageUploadError

logger = logging.getLogger(__name__)


def strip_empty_lines(value):
    """Return the given HTML with empty and all-whitespace lines removed."""
    return re.sub(r'\n[ \t]*(?=\n)', '', force_unicode(value))
strip_empty_lines = allow_lazy(strip_empty_lines, unicode)


def product_credentials(request, stall_identifier, product_name):
    try:
        stall = Stall.objects.get(identifier=stall_identifier)
        product = Product.objects.get(stall=stall, slug=product_name)
    except ObjectDoesNotExist:
        raise Http404

    context = {
        'causes': product.causes.all(),
        'certificates': product.certificates_by_cause
    }
    template = 'marketplace/product_view/credentials_ajax.html'
    return render(request, template, context)


def strip_tags(value):
    """Returns the given HTML with all tags stripped."""
    return re.sub(r'<[^>]*?>', '', force_unicode(value))

# Product views
# ============
class ProductDetailView(DetailView):
    model = Product
    context_object_name = 'product'
    queryset = Product.objects.all()
    template_name = 'marketplace/product_page.html'

    def get_object(self, *la, **kwa):
        return self.product

    def dispatch(self, request, *args, **kwargs):
        self.request = request
        return super(
            ProductDetailView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        context['self_url'] = self.request.path
        context['recommended_products'] = self.recommended_products
        context['recommended_title'] = self.recommended_category_name
        context['love_lists'] = self.love_lists
        context['stall_products_live'] = self.stall_products_live
        context['ask_question_popup'] = self.ask_question_popup
        context['request_delivery_country_popup'] = self.request_delivery_country_popup
        context['ecomm_prodid'] = self.product.id
        context['ecomm_pagetype'] = 'product'
        context['ecomm_totalvalue'] = self.product.price.amount
        context['free_shippings'] = self.free_shippings

        # CloudFlare detects current country of user.
        # If we cannot deliver there, we warn the user.
        # In case we cannot deliver, we give users the link to 2nd top level
        # Category to this particular product.
        index = 1
        cats = self.product.category_objs()
        i = 0
        related_search_category = None
        for v in cats:
            if i == index:
                related_search_category = v
            i = i + 1
        context['related_search_category'] = related_search_category

        # We use this to show the message to User that we cannot deliver.
        context['user_country_title'] = self.request.country
        user_country = Country.objects.filter(code=self.request.country)
        if user_country:
            context['user_country_title'] = user_country[0].title

        countries = set()
        delivery_countries = set()
        for rule in self.product.shipping_profile.shipping_rules.all():
            for country in rule.countries.all():
                countries.add(country.code)
                delivery_countries.add(country)
        # If this product delivers to "Rest of the world", then it certainly
        # delivers to this User's country
        if self.product.shipping_profile.others_price:
            context['can_deliver_to_user_country'] = True
            if self.request.country not in countries and user_country:
                delivery_countries.add(user_country[0])
        else:
            context['can_deliver_to_user_country'] = bool(self.request.country in countries)
        context['delivery_countries'] = delivery_countries

        if self.kwargs.get('currency', None):
            requested_currency = self.kwargs.get('currency', None)
            currency_symbol = None
            for (k, v) in CURRENCY_CHOICES:
                if k == requested_currency:
                    currency_symbol = v
                    break
            if currency_symbol:
                price_in_requested_currency = self.product.get_price_instance()
                context['price_in_requested_currency'] = CurrencyExchangeRate.convert(price_in_requested_currency.amount, self.kwargs.get('currency', None))
                context['requested_currency'] = self.kwargs.get('currency', None)
                context['requested_currency_symbol'] = currency_symbol
        return context

    def get(self, request, *la, **kwa):
        # if the product is unpublished
        # and its not the product owner or a superuser
        # return a 404

        product_name = kwa.get('product_name')
        try:
            stall_ident = int(kwa.get('stall_identifier'))
        except (ValueError, TypeError):
            raise Http404
        try:
            self.product = (Product.objects.filter(
                                stall__identifier=stall_ident,
                                slug=product_name)
                            .select_related('primary_category', 'stall',
                                            'stall__user', 'shipping_profile',
                                            'shipping_profile__shipping_country')
                            .prefetch_related('keywords', 'causes', 'prices',
                                              'product_images', 'certificates',
                                              'shipping_profile__shipping_rules',
                                              'shipping_profile__shipping_rules__countries')
                            .get())
            self.stall = self.product.stall
        except ObjectDoesNotExist:
            return HttpResponseRedirect("%s?product=notfound" % (reverse('product_search',)))

        if self.product.num_hearts == 0:
            self.recommended_products = self.product.primary_category.products.filter(status=Product.PUBLISHED_LIVE).order_by('-number_of_recent_sales','-number_of_sales')
            if len(self.recommended_products) == 0:
                self.recommended_products = None
        else:
            self.recommended_products = None

        # Strip out 'Other' from category name
        recommended_category_name = self.product.primary_category.name
        if recommended_category_name.startswith('Other '):
            recommended_category_name = recommended_category_name[6:]
        self.recommended_category_name = recommended_category_name

        self.stall_products_live = (self.stall.products
                                        .live()
                                        .select_related('stall__identifier'))
        self.love_lists = (self.product.love_lists
                               .order_by('-promoted', '-updated')
                               .select_related('user__username'))

        free_shippings_raw = FreeShipping.objects.all()
        free_shippings = []
        for entry in free_shippings_raw:
            free_shippings.append({
                #'origin': [c.to_json() for c in entry.shipping_from.all()],
                'destination': [c.to_json() for c in entry.shipping_to.all()],
                'discount': entry.percent_discount,
            })

        self.free_shippings = free_shippings

        # When an anonymous user clicks 'Ask Question' they will be redirected
        # back with the 'ask-question' flag - this will popup the ask question
        # box on page-load so the user doesn't have to click it again.
        self.ask_question_popup = bool(request.GET.get('ask-question', False))
        self.request_delivery_country_popup = bool(request.GET.get('request-delivery-country', False))

        if self.product.status == self.product.PUBLISHED_LIVE:
            return super(ProductDetailView, self).get(request, *la, **kwa)

        try:
            stall = request.user.stall
        except:
            stall = None

        if request.user.is_superuser or (stall and stall == self.product.stall):
            return super(ProductDetailView, self).get(request, *la, **kwa)

        cat = self.product.primary_category.slug
        return HttpResponseRedirect('%s?product=notfound' % (
            reverse('category_discover', kwargs={"category": cat})))


class ProductBaseEdit(object):
    def _render(self, context):
        rendered = render(self.request, self.template_name, context)
        rendered.content = strip_empty_lines(rendered.content)
        return rendered

    def _parse_int_list(self, _params, k):
        try:
            _params.setlist(k, [int(x) for x in _params.getlist(k)])
        except:
            pass

    def _create_suggested(self, params, key, model):
        ids = []
        for title in params.getlist(key):
            try:
                ob = model.objects.get(title__iexact=title)
            except model.DoesNotExist:
                ob = model.objects.create(title=title)
            ids.append(ob.id)
        params.setlist(key, ids)

    def _shipping_form(self, stall, params):
        request = self.request
        profile_select = params['id_shipping_profile']
        self._parse_int_list(params, 'ship_profile-shipping_country')

        profile = None
        if profile_select:
            # an existing shipping profile has been selected
            # try and retrieve it
            try:
                profile = ShippingProfile.objects.get(
                    stall=stall,
                    id=profile_select)
            except ObjectDoesNotExist:
                print profile_select
                pass

        # grrr - this may indicate a prob with templates
        if params['id_ship_profile-shipping_country']:
            params['ship_profile-shipping_country'] = int(
                params['id_ship_profile-shipping_country'])

        params['ship_profile-stall'] = stall.id
        params['ship_profile-others_price_1'] = 'GBP'
        params['ship_profile-others_price_extra_1'] = 'GBP'

        shipping_form = ShippingProfileForm(params,
                                   request=request,
                                   stall=stall,
                                   instance=profile,
                                   prefix='ship_profile')

        if shipping_form.is_valid():
            shipping_form.save()

        return shipping_form

    def _get_profile(self, stall, params):
        try:
            profile = ShippingProfile.objects.get(
                stall=stall, title=params['ship_profile-title'])
        except:
            profile = None
        return profile

    def _product_form(self, stall, params, instance=None):
        product_params = self.request.POST.copy()
        product_params['stall_id'] = stall.id
        if 'save-publish' in self.request.POST and stall.is_suspended == False:
            product_params['status'] = Product.PUBLISHED_LIVE
        elif 'save-draft' in self.request.POST:
            product_params['status'] = Product.PUBLISHED_DRAFT

        certificate_ids = product_params.getlist('id_certificates')
        for cert in certificate_ids:
            try:
                cert_id = int(cert.split('__').pop())
                product_params.appendlist('certificates', cert_id)
            except ValueError:
                pass

        self._parse_int_list(product_params, 'causes')
        self._create_suggested(product_params, 'keywords', Keyword)

        self._parse_int_list(product_params, 'recipients')

        # remove stock level if set to unlimited
        if product_params['stock_level'] == 'unlimited':
            product_params['stock'] = None

        # set the profile id if possible
        profile = self._get_profile(stall, params)
        if profile:
            product_params['shipping_profile'] = profile.id

        return ProductCreationForm(
            product_params, self.request.FILES or None,
            request=self.request, stall=stall, instance=instance)

    @property
    def _cert_params(self):
        cert_params = {}
        [cert_params.__setitem__(x, y)
         for x, y in self.request.POST.items()
         if x.startswith('suggest_cert')
         or x.startswith('id_suggest_cert')]
        return cert_params

    def _cert_form(self, params, instance=None):
        return ProductSuggestedCertificateFormset(
            self._cert_params,
            prefix='suggest_cert', instance=instance)

    def _rules_formset(self, prefix, params=None, instance=None):
        # hardcode the price currencies for rule forms
        if params:
            price_rules = filter(
                lambda (x, y): y and x.startswith(
                    '%s-' % prefix) and x.endswith('rule_price_0'),
                params.items())

            map(lambda (x, y): params.__setitem__('%s1' % x[:-1],
                                                  'GBP'),
                price_rules)
            map(lambda (x, y): params.__setitem__('%s_extra_1' % x[:-2],
                                                  'GBP'),
                price_rules)

            # read the countries and convert to ints
            country_rules = filter(
                lambda (x, y): y and x.startswith(
                    '%s-' % prefix) and x.endswith('countries'),
                params.items())
            [self._parse_int_list(params, c)
             for c, x in country_rules]

        rules_formset = ShippingRulesFormset(
            params,
            instance=instance,
            prefix="ship_rules")

        rules_formset[0].empty_permitted = False

        return rules_formset


@view_dispatch_decorator(login_required)
class ProductCreateView(CreateView, ProductBaseEdit):
    model = Product
    template_name = 'marketplace/create_product.html'

    def get_context_data(self, **kwargs):
        context = super(ProductCreateView, self).get_context_data(**kwargs)
        context['product_form_type'] = 'create'
        context['form_errors'] = self.form_errors
        context['product_form'] = self.product_form
        context['price_form'] = self.price_form
        context['cert_form'] = self.cert_form
        context['images_formset'] = self.images_formset
        context['rules_formset'] = self.rules_formset
        context['shipping_form'] = self.shipping_form
        context['existing_keywords'] = self.existing_keywords

        return context

    #noinspection PyAttributeOutsideInit
    def get(self, request, *la, **kwa):
        """
        Handles the creation of a product.
        """
        try:
            stall = self.request.user.stall
        except:
            return redirect('create_stall')

        self.form_errors = {}
        self.existing_keywords = []

        #if stall.user.user_profile.avatar == '':
            #return HttpResponseRedirect(
                #u'/accounts/profile/?add-product=1')

        if stall.paypal_email == '':
            return HttpResponseRedirect(
                u'/accounts/stall/payment/?add-product=1')

        params = None
        shipping_params = None

        # render the forms
        self.images_formset = ProductImagesFormset(
            prefix='thumbs')

        self.cert_form = ProductSuggestedCertificateFormset(
            prefix='suggest_cert')

        self.shipping_form = ShippingProfileForm(
            shipping_params, request=request, stall=stall,
            prefix='ship_profile')

        self.rules_formset = self._rules_formset("ship_rules")

        self.product_form = ProductCreationForm(
            params, request.FILES or None,
            request=request, stall=stall)

        self.price_form = ProductPriceForm(params, prefix='price')

        return super(ProductCreateView, self).get(request, *la, **kwa)

    #noinspection PyAttributeOutsideInit
    @method_decorator(transaction.commit_on_success)
    def post(self, request, *la, **kwa):
        try:
            stall = self.request.user.stall
        except:
            return redirect('create_stall')

        form_valid = True
        self.form_errors = {}
        params = request.POST.copy()

        self.cert_form = self._cert_form(params)

        params['price-amount_1'] = 'GBP'
        self.price_form = ProductPriceForm(params, prefix='price')

        self.images_formset = ProductImagesFormset(
            params,
            prefix='thumbs')

        self.shipping_form = self._shipping_form(stall, params)

        self.product_form = self._product_form(stall, params)

        if not self.shipping_form.is_valid():
            form_valid = False
            self.form_errors['shipping_form'] = 'invalid'
            self.rules_formset = self._rules_formset(
                "ship_rules",
                params)
        else:
            self.rules_formset = self._rules_formset(
                "ship_rules",
                params,
                instance=self.shipping_form.instance)
            if self.rules_formset.is_valid():
                self.rules_formset.save()
            else:
                form_valid = False

        if not self.product_form.is_valid():
            form_valid = False
            self.form_errors['product_form'] = 'invalid'

        if not self.images_formset.is_valid():
            form_valid = False
            self.form_errors['images_formset'] = 'invalid'

        if not self.price_form.is_valid():
            form_valid = False
            self.form_errors['price_form'] = 'invalid'

        if self._cert_params and not self.cert_form.is_valid():
            form_valid = False

        if form_valid:
            product = self.product_form.save()
            self.product_form.save_m2m()

            ProductImagesFormset(
                params,
                instance=self.product_form.instance,
                prefix='thumbs').save()

            if self._cert_params:
                self.cert_form = self._cert_form(
                    params, instance=self.product_form.instance)
                self.cert_form.save()

            self.price_form = ProductPriceForm(
                params,
                prefix='price',
                product=self.product_form.instance)

            self.price_form.save()
            # Track that this product was created successfully
            try:
                from apps.analytics.models import ProductFormErrors
                init_params = dict(
                    stall=stall,
                    product=self.product_form.instance
                )
                log_errors = ProductFormErrors(**init_params)
                log_errors.save()
            except Exception:
                pass

            save_publish = 'save-publish' in self.request.POST
            save_draft = 'save-draft' in self.request.POST # XXX: unused


            # XXX: move into notifications.events
            mixpanel_engage(self.request, {'$set': {
                'Products Published': request.user.stall.products.live().count(),
            }})
            if save_publish:
                # XXX: move into notifications.events
                mixpanel_track(self.request, "Created a Product", product.mixpanel_record())
                return redirect('product_page', stall.identifier, self.product_form.instance.slug)
            else:
                # XXX: move into notifications.events
                mixpanel_track(self.request, "Created a Draft Product", product.mixpanel_record())
                return redirect('selling_unpublished')

        transaction.rollback()

        #self.existing_keywords = self.product_form.get_keywords_from_names(
        #    self.product_form.data["keywords_field"]
        #)
        self.existing_keywords = params.getlist("keywords_field")

        try:
            from apps.analytics.models import ProductFormErrors
            init_params = dict(
                stall=stall,
                had_error=True
            )
            for k, v in self.form_errors.items():
                init_params['%s_error' % k] = True
            for k, v in self.product_form.errors.items():
                init_params['%s_error' % k] = True
            for k, v in self.price_form.errors.items():
                init_params['%s_error' % k] = True
            log_errors = ProductFormErrors(**init_params)
            log_errors.save()
        except Exception:
            pass

        return super(ProductCreateView, self).post(request, *la, **kwa)


@login_required
def product_taxonomy(request, *la, **kwa):
    """
    Handles the creation of a product.
    """
    attr = None
    attrs = {'keywords': Keyword.objects}

    results = []

    try:
        attr = request.GET['attr'].lower()
        query = request.GET['q']
    except AttributeError:
        attr = None
        query = None

    field = attr and attrs.get(attr) or None
    if field:
        results = [
            f.title.title() for f in
            field.filter(title__icontains=query)]

    return HttpResponse(
        json.dumps(results, cls=DjangoJSONEncoder),
        content_type='application/json; charset=utf-8')


@login_required
def certificate_search(request, *la, **kwa):
    """
    Handles the creation of a product.
    """
    # this doesnt seem right
    causes = request.GET.getlist('causes[]')
    certificates = []
    for cause in causes:
        [certificates.append(dict(term=c.title,
                                  value=c.title+'__'+str(c.id)))
         for c
         in Certificate.objects.filter(cause_id=cause)]

    return HttpResponse(
        json.dumps(certificates, cls=DjangoJSONEncoder),
        content_type='application/json; charset=utf-8')


@view_dispatch_decorator(login_required)
class ProductUpdate(UpdateView, ProductBaseEdit):
    model = Product
    template_name = 'marketplace/product_form.html'

    def get_object(self, *la, **kwa):
        return self.product

    def get_context_data(self, **kwargs):
        context = super(ProductUpdate, self).get_context_data(**kwargs)
        context.update()
        context['product_form_type'] = 'update'
        context['form_errors'] = self.form_errors
        context['product_form'] = self.product_form
        context['price_form'] = self.price_form
        context['images_formset'] = self.images_formset
        context['rules_formset'] = self.rules_formset
        context['cert_form'] = self.cert_form
        context['shipping_form'] = self.shipping_form
        context['existing_keywords'] = self.product.keywords.all()

        return context

    #noinspection PyAttributeOutsideInit
    def get(self, request, *la, **kwa):
        # if the product is unpublished
        # and its not the product owner or a superuser
        # return a 404

        product_name = kwa.get('product_name')
        try:
            stall_ident = int(kwa.get('stall_identifier'))
        except (ValueError, TypeError):
            raise Http404
        try:
            self.stall = Stall.objects.get(identifier=stall_ident)
            self.product = Product.objects.get(
                stall=self.stall, slug=product_name)
        except:
            raise Http404

        if not request.user.is_superuser:
            if getattr(request.user, 'stall') != self.stall:
                raise Http404

        self.form_errors = {}

        params = None
        shipping_params = None

        # render the forms
        self.images_formset = ProductImagesFormset(
            params, prefix='thumbs', instance=self.product)

        self.cert_form = ProductSuggestedCertificateFormset(
            prefix='suggest_cert')

        self.shipping_form = ShippingProfileForm(
            shipping_params, request=request, stall=self.stall,
            prefix='ship_profile',
            instance=self.product.shipping_profile)

        self.rules_formset = self._rules_formset(
            "ship_rules",
            params,
            instance=self.product.shipping_profile)

        self.product_form = ProductCreationForm(
            params, request.FILES or None,
            request=request,
            stall=self.stall,
            instance=self.product)

        self.price_form = ProductPriceForm(
            params, prefix='price', instance=self.product.price)

        return super(ProductUpdate, self).get(request, *la, **kwa)

    #noinspection PyAttributeOutsideInit
    @method_decorator(transaction.commit_on_success)
    def post(self, request, *la, **kwa):
        product_name = kwa.get('product_name')
        try:
            stall_ident = int(kwa.get('stall_identifier'))
        except (ValueError, TypeError):
            raise Http404
        try:
            self.stall = Stall.objects.get(identifier=stall_ident)
            self.product = Product.objects.get(
                stall=self.stall, slug=product_name)
        except:
            raise Http404

        form_valid = True
        self.form_errors = {}
        params = request.POST.copy()

        self.cert_form = self._cert_form(params)

        params['price-amount_1'] = 'GBP'
        self.price_form = ProductPriceForm(params, prefix='price')

        self.shipping_form = self._shipping_form(self.stall, params)

        self.rules_formset = self._rules_formset(
            "ship_rules",
            params,
            instance=self.product.shipping_profile)

        self.images_formset = ProductImagesFormset(
            params, prefix='thumbs', instance=self.product)

        self.product_form = self._product_form(
            self.stall, params, instance=self.product)

        if not self.shipping_form.is_valid():
            form_valid = False
            self.form_errors['shipping_form'] = 'invalid'
        elif self.rules_formset.is_valid():
            self.rules_formset.save()
        else:
            form_valid = False

        if not self.product_form.is_valid():
            form_valid = False
            self.form_errors['product_form'] = 'invalid'

        if not self.price_form.is_valid():
            form_valid = False
            self.form_errors['price_form'] = 'invalid'

        if not self.images_formset.is_valid():
            form_valid = False
            self.form_errors['images_formset'] = 'invalid'

        if self._cert_params and not self.cert_form.is_valid():
            form_valid = False
            self.form_errors['cert_params'] = 'invalid'
            [self.form_errors.update(f.errors)
             for f in self.cert_form]

        if form_valid:
            product = self.product_form.save()
            self.product_form.save_m2m()
            self.images_formset.save()

            if product.status == Product.PUBLISHED_LIVE:
                try:
                    Sailthru(request).update_product(product)
                except Exception, e:
                    # Don't blow up on an error from Sailthru
                    logger.error(e, exc_info=True)

            if self._cert_params:
                self.cert_form = self._cert_form(
                    params, instance=self.product)
                self.cert_form.save()

            try:
                price = Price.objects.get(product=self.product)
            except MultipleObjectsReturned:
                # TODO: cleanup?
                price = Price.objects.filter(product=self.product)[0]
            except ObjectDoesNotExist:
                price = None

            self.price_form = ProductPriceForm(
                params,
                prefix='price',
                product=self.product,
                instance=price)

            self.price_form.save()
            try:
                from apps.analytics.models import ProductFormErrors
                init_params = dict(
                    stall=self.stall,
                    product=self.product
                )
                log_errors = ProductFormErrors(**init_params)
                log_errors.save()
            except Exception:
                pass

            save_publish = 'save-publish' in self.request.POST
            # XXX: move into notifications.events
            mixpanel_engage(self.request, {'$set': {
                'Products Published': request.user.stall.products.live().count(),
            }})
            if save_publish:
                # XXX: move into notifications.events
                mixpanel_track(self.request, "Published a Product", product.mixpanel_record())
                return redirect(
                    'product_page',
                    self.stall.identifier,
                    self.product.slug
                )

            # XXX: move into notifications.events
            mixpanel_track(self.request, "Unpublished a Product", product.mixpanel_record())
            return redirect('selling_unpublished')

        # Form not valid
        transaction.rollback()
        # Track the errors so they can be drilled down later on.
        try:
            from apps.analytics.models import ProductFormErrors
            init_params = dict(
                stall=self.stall,
                product=self.product,
                had_error=True
            )
            for k, v in self.form_errors.items():
                init_params['%s_error' % k] = True
            for k, v in self.product_form.errors.items():
                init_params['%s_error' % k] = True
            for k, v in self.price_form.errors.items():
                init_params['%s_error' % k] = True
            log_errors = ProductFormErrors(**init_params)
            log_errors.save()
        except Exception:
            pass

        return super(ProductUpdate, self).post(request, *la, **kwa)


@view_dispatch_decorator(login_required)
class ProductImageUploaderAjax(FileUploaderAjax):

    def post(self, request):
        try:
            filename, upfile = self._posted_image(request)
        except KeyError:
            return HttpResponseBadRequest("AJAX request not valid")

        #try:
        #    spamish_validators(filename)
        #except ValidationError, e:
        #    return self._fail_response(e.messages[0])

        try:
            validate_uploaded_image(upfile, min_width=800, min_height=800)
        except ImageUploadError, e:
            return self._fail_response(e)

        try:
            return self._success_response(
                filename,
                self._save_temp_image(request, filename, upfile))
        except:
            raise
            return HttpResponseBadRequest("AJAX request not valid")
