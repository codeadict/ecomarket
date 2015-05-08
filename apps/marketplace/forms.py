# encoding: utf-8
import phonenumbers, re
from phonenumbers.phonenumberutil import SUPPORTED_REGIONS

from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import EMPTY_VALUES
from django.forms.models import \
    inlineformset_factory, BaseInlineFormSet

from django.utils import timezone
from django.utils.translation import ugettext as _

from accounts.models import UserProfile
from .models import \
    Stall, Product, Category, Keyword, Recipient, Color

from marketplace.models import \
    ProductImage, Cause, Certificate, ShippingProfile, \
    Country, ShippingRule, SuggestedCertificate, Price

from marketplace.widgets import FixedCurrencyWidget

#from apps.spamish.utils import run_validators

from image_crop.utils import idnormalizer


# Stall forms
# ===============
class StallOwnerProfileForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = (
            'address_1', 'address_2',
            'city', 'state',
            'zipcode', 'country')

    field_requirements = {
        'address_1': True,
        'address_2': True,
        'city': True,
        'state': True,
        'zipcode': True,
        'country': True,
    }

    def __init__(self, *args, **kwargs):
        super(StallOwnerProfileForm, self).__init__(*args, **kwargs)
        self.fields['country'].widget.attrs.update({'class': "select"})

        for k, v in self.field_requirements.items():
            self.fields[k].required = v


class PhoneValidatorMixin(object):

    def _validate_phone_number(self, number):
        if number in EMPTY_VALUES:
            return number
        if "country" in self.data:
            # Assume creation form
            # TODO don't replicate form creation
            # We assume this is valid - this should have already been checked
            # by the view
            country_field = StallOwnerProfileForm().fields["country"]
            country = country_field.clean(self.data.get("country"))
        else:
            # Assume edit form
            country = self.instance.user.get_profile().country
        if country.code not in SUPPORTED_REGIONS:
            # Number must be in international format
            return number
        try:
            parsed = phonenumbers.parse(number, country.code)
        except phonenumbers.NumberParseException:
            raise ValidationError("Unable to parse this number. Please try a "
                                  "different format.")
        number = phonenumbers.format_number(
            parsed, phonenumbers.PhoneNumberFormat.E164)
        return number

        # TODO if there is no value in this check, delete it,
        # otherwise make it less annoying
        if len(number) <= 12:  # 12 chars plus + sign
            missing = 13 - len(number)
            raise ValidationError(
                "This number is a bit on the short side - if this is "
                "definitely correct, please add {missing} additional zero{s} "
                "after your full number.".format(
                    missing=missing, s=("s" if missing > 1 else "")))
        return number

    def clean_phone_landline(self):
        return self._validate_phone_number(self.cleaned_data["phone_landline"])

    def clean_phone_mobile(self):
        return self._validate_phone_number(self.cleaned_data["phone_mobile"])


class StallForm(PhoneValidatorMixin, forms.ModelForm):
    class Meta:
        model = Stall
        fields = (
            'title', 'description_short', 'description_full',
            'phone_landline', 'phone_mobile', 'twitter_username',
            'email_opt_in')

    field_requirements = {
        'title': True,
        'phone_mobile': True,
        'twitter_username': False,
        'description_short': True,
        'description_full': True,
    }

    placeholders = {
        'description_short': _('Keep this to one sentence if you can!'),
        'description_full': _('A short paragraph describing your stall'),
        'twitter_username': _('For example @ecomarket'),
    }

    def __init__(self, *args, **kwargs):
        super(StallForm, self).__init__(*args, **kwargs)

        for k, v in self.field_requirements.items():
            self.fields[k].required = v

        for k, v in self.placeholders.items():
            self.fields[k].widget.attrs['placeholder'] = v

    # Commenting out as part of https://sprint.ly/product/3047/#!/item/750
    # def clean_title(self):
    #     return run_validators(self.cleaned_data['title'])

    # def clean_twitter_username(self):
    #     return run_validators(self.cleaned_data['twitter_username'])

    # def clean_description_short(self):
    #     return run_validators(self.cleaned_data['description_short'])

    # def clean_description_full(self):
    #     return run_validators(self.cleaned_data['description_full'])


class RelaxedMultipleChoiceField(forms.MultipleChoiceField):
    """Subclass of MutlipleChoiceField which allows values which are not in
    the select list to be submitted
    """

    def valid_value(self, value):
        return True


# Product forms
# ===============
class ProductCreationForm(forms.ModelForm):
    title = forms.CharField(
        max_length=45, required=True,
        widget=forms.TextInput(
            attrs={"maxlength": 45}))
    description = forms.CharField(
        max_length=3000, required=True,
        widget=forms.Textarea(
            attrs={"rows": "6", "cols": "30", "maxlength": 3000}))
    # Weird name because otherwise we clash with the 'keywords' field on
    # the model.
    keywords_field = RelaxedMultipleChoiceField(
        required=True,
        widget=forms.SelectMultiple(
            attrs={
                "class": "m2m",
                'placeholder': _('Start typing product keywords...')})
    )

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        self.stall = kwargs.pop('stall', None)
        super(ProductCreationForm, self).__init__(*args, **kwargs)

        photos = self.request.POST.getlist('photos')
        photo_titles = self.request.POST.getlist('photos-title')
        photo_thumbs = self.request.POST.getlist('photos-thumbnail')
        self.photos = []
        for photo in zip(photos, photo_titles, photo_thumbs):
            self.photos.append(photo)

        self.categories_qs = Category.objects.all()
        self.categories2_qs = Category.objects.all()
        self.keywords_qs = Keyword.objects.all()
        self.causes_qs = Cause.objects.all()
        self.certificates_qs = Certificate.objects.all()
        self.recipients_qs = Recipient.objects.all()
        self.colors_qs = Color.objects.all()
        self.shipping_profiles_qs = ShippingProfile.objects.filter(
            stall=self.stall)

        # Category
        self.fields['primary_category'].required = True
        self.fields['primary_category'].widget = forms.Textarea(
            attrs={
                "class": "multiple-dropdown",
                "data-placeholder": "Please select main category"})
        self.fields['primary_category'].queryset = self.categories_qs

        self.fields['secondary_category'].required = False
        self.fields['secondary_category'].widget = forms.Textarea(
            attrs={
                "class": "multiple-dropdown",
                "placeholder": "Please select secondary category"})
        self.fields['secondary_category'].queryset = self.categories2_qs

        self.fields["keywords_field"].choices = [keyword for keyword in self.keywords_qs]
        self.keywords_field = self.fields["keywords_field"]
        # Really horrible hack to make the automcomplete_suggestions template
        # work with a non model field.
        if self.instance and self.instance.id:
            self.keywords_field.value = [k for k in self.instance.keywords.all()]

        # Causes
        self.fields['causes'].widget = forms.SelectMultiple(
            attrs={"class": "m2m"})
        self.fields['causes'].queryset = self.causes_qs
        self.fields['causes'].label = 'Product causes'

        # Certificates
        self.fields['certificates'].widget = forms.SelectMultiple(
            attrs={"class": "m2m"})
        self.fields['certificates'].queryset = self.certificates_qs
        self.fields['certificates'].label = 'Product certificates'

        # Recipients
        self.fields['recipients'].widget = forms.SelectMultiple(
            attrs={"class": "m2m"})
        self.fields['recipients'].queryset = self.recipients_qs
        # Colors
        self.fields['colors'].widget = forms.SelectMultiple(
            attrs={"class": "color-picker-m2m"})
        self.fields['colors'].queryset = self.colors_qs

        self.fields['shipping_profile'].required = True
        self.fields['shipping_profile'].queryset = self.shipping_profiles_qs
        self.fields['shipping_profile'].widget = forms.Select(
            attrs={"class": "select",
                   'placeholder': 'Create a new profile'})

    class Meta:
        model = Product
        fields = (
            'title',
            'description',
            'causes',
            'certificates',
            'colors',
            'recipients',
            'stock',
            'shipping_profile',
            'primary_category',
            'secondary_category',
            'status',
            'publication_date',
        )

    def clean_description(self):
        desc = self.cleaned_data['description'].strip()
        word_count = re.split('\s+', desc)
        if len(word_count) < 30:
            raise forms.ValidationError("You need to use at least 30 words in "
                                        "your product description. Remember the "
                                        "more descriptive you are, the better "
                                        "you will rank in our search and on "
                                        "search engines")
        return desc

    def clean_title(self):
        title = self.cleaned_data['title']
        # Commenting out as part of https://sprint.ly/product/3047/#!/item/750
        # title = run_validators(self.cleaned_data['title'])
        if title:
            allowed_chars = u"AÀÁÂBCDÈÉÊEFGHIJKLMNOPQRSTUVWXYZa" \
                + u"àáâbcdèéêefghijklmnopqrstuvwxyz1234567890()' "
            for c in title:
                if c not in allowed_chars:
                    raise forms.ValidationError(
                        u"Please only include letters, numbers, brackets, "
                        + "the apostrophe and spaces.")
        return title

    def clean_keywords_field(self):
        keywords = self.cleaned_data["keywords_field"]
        for keyword in keywords:
            if "," in keyword:
                raise forms.ValidationError("Commas are not allowed in keywords")
        return keywords

    # Commenting out as part of https://sprint.ly/product/3047/#!/item/750
    # def clean_description(self):
    #     return run_validators(self.cleaned_data['description'])

    def save(self, *args, **kwargs):
        # update the shipping profiles

        # get the name of the profile
        #profile_name = self.request.POST['shipping_profile_name']

        #profiles = ShippingProfile.objects.filter(
         #   title=profile_name, stall=self.request.user.stall)

        #profile = profiles and profiles[0] or None

        kwargs['commit'] = False

        # create the product
        product = super(ProductCreationForm, self).save(*args, **kwargs)
        product.stall = self.stall

        # set the workflow state
        if 'save-publish' in self.request.POST and self.stall.is_suspended == False:
            product.publication_status = Product.PUBLISHED_LIVE
            product.publication_date = timezone.now()
        elif 'save-draft' in self.request.POST:
            product.publication_status = Product.PUBLISHED_DRAFT

        product.flag = None
        product.save()
        product.keywords.clear()
        new_keywords = self.get_keywords_from_names(self.cleaned_data["keywords_field"])
        product.keywords.add(*new_keywords)
        return product

    def get_keywords_from_names(self, names):
        # get_or_create returns a tuple of (object, created)
        return [Keyword.objects.get_or_create(title=name)[0] for name in names]


class ProductPriceForm(forms.ModelForm):
    empty_permitted = False

    def __init__(self, *la, **kwa):
        self.product = kwa.pop('product', None)
        super(ProductPriceForm, self).__init__(*la, **kwa)
        self.fields['amount'].widget = FixedCurrencyWidget(
            attrs={"class": "price input-currency money"})
        self.fields['amount'].required = True

    def clean_amount(self):
        amount = self.cleaned_data['amount']
        try:
            if amount.amount > 0:
                return amount
        except ValueError:
            pass
        raise ValidationError("Price must be above zero")

    def save(self, *la, **kwa):
        if self.product:
            self.instance.product = self.product
        super(ProductPriceForm, self).save(*la, **kwa)

    class Meta:
        model = Price
        fields = ('amount', )


ProductPriceFormset = inlineformset_factory(
    Product, Price,
    form=ProductPriceForm,
    can_delete=False, max_num=1)


class ProductImageForm(forms.ModelForm):
    empty_permitted = False

    class Meta:
        model = ProductImage
        fields = ('image', 'name', 'filename', 'data')

    def __init__(self, *la, **kwa):
        self.product = kwa.pop('product', None)
        super(ProductImageForm, self).__init__(*la, **kwa)
        self.fields['name'].widget.attrs = {
            'class': 'image-name',
            'style': 'display:none;'}
        self.fields['data'].widget = forms.HiddenInput(
            attrs={'class': 'image-data'})
        self.fields['image'].widget = forms.HiddenInput(
            attrs={'class': 'image'})
        self.fields['filename'].widget = forms.HiddenInput(
            attrs={'class': 'image-filename'})

    def save(self, *la, **kwa):
        if self.product:
            self.instance.product = self.product

        file_ext = self.instance.filename.split('.')[-1].lower()

        if self.instance.name.strip():
            basename = self.instance.name
        else:
            basename = self.instance.filename[:-(len(file_ext) + 1)]
            try:
                if basename.index('_') == 36:
                    basename = basename[37:]
            except ValueError:
                pass

        self.instance.filename = '%s.%s' % (
            idnormalizer.normalize(basename),
            file_ext)

        try:
            image_size = self.instance.image.size
        except ValueError:
            image_size = 0

        try:
            thumbnail_size = self.instance.thumbnail.size
        except ValueError:
            thumbnail_size = 0

        if image_size != thumbnail_size:
            if thumbnail_size:
                self.instance.thumbnail.delete()
            self.instance.crop_thumbnail()
        return super(ProductImageForm, self).save(*la, **kwa)

    @property
    def url_100(self):
        filename = self.data.get('%s-image' % self.prefix)
        if filename:
            ext = filename.split('.')[-1]
            return '/media/image_crop/standard/%s100x100.%s' % (
                filename[:-len(ext)], ext)
        return self.instance.url_100

    @property
    def url_100_update(self):
        return self.instance.url_100


class BaseProductImagesFormSet(BaseInlineFormSet):

    def __init__(self, *la, **kwa):
        super(BaseProductImagesFormSet, self).__init__(*la, **kwa)
        if self.forms:
            self.forms[0].empty_permitted = False

ProductImagesFormset = inlineformset_factory(
    Product, ProductImage,
    form=ProductImageForm,
    formset=BaseProductImagesFormSet,
    can_delete=True,
    extra=1)


class ShippingProfileForm(forms.ModelForm):
    title = forms.CharField(
        max_length=45, required=True,
        widget=forms.TextInput(
            attrs={"maxlength": 45}))
    shipping_profile_worldwide = forms.ChoiceField(required=False,
                                                   choices=((0, 'No'),
                                                            (1, 'Yes')))

    def __init__(self, *la, **kwa):
        self.request = kwa.pop('request', None)
        self.stall = kwa.pop('stall', None)
        super(ShippingProfileForm, self).__init__(*la, **kwa)
        self.shipping_country_qs = Country.objects.all()

        self.fields['title'].label = _('Name your profile')
        self.fields['shipping_country'].label = _('Product ships from')
        self.fields['shipping_postcode'].widget = forms.TextInput(
            attrs={"class": "postcode"})
        self.fields['shipping_postcode'].label = _(
            'Postcode or Zip where product ships from')

        self.fields['others_price'].widget = FixedCurrencyWidget(
            attrs={"class": "price input-currency money"})
        self.fields['others_price'].label = _('First item')

        self.fields['others_price_extra'].widget = FixedCurrencyWidget(
            attrs={"class": "price input-currency money"})
        self.fields['others_price_extra'].label = _('Subsequent items')

        self.fields['others_delivery_time'].widget = forms.TextInput(
            attrs={"class": "number input-number"})
        self.fields['others_delivery_time_max'].widget = forms.TextInput(
            attrs={"class": "number input-number"})

    def clean(self, *la, **kwa):
        cleaned_data = super(ShippingProfileForm, self).clean(*la, **kwa)        
        try:
            # XXX: this is only in self.data no self.cleaned_data.. why?
            worldwide = int(self.data['shipping_profile_worldwide']) == 1
        except ValueError:
            worldwide = False

        if not worldwide:
            cleaned_data.update({
                'shipping_profile_worldwide': None,
                'others_price': None,
                'others_price_extra': None,
                'others_delivery_time': None,
                'others_delivery_time_max': None
            })
        return cleaned_data

    def save(self, *la, **kwa):        
        return super(ShippingProfileForm, self).save(*la, **kwa)

    class Meta:
        model = ShippingProfile
        fields = ('title', 'stall', 'shipping_country', 'shipping_postcode',
                  'others_price', 'others_price_extra', 'others_delivery_time',
                  'others_delivery_time_max', 'shipping_profile_worldwide')


class ShippingRuleForm(forms.ModelForm):

    empty_permitted = False

    def __init__(self, *la, **kwa):
        self.request = kwa.pop('request', None)
        super(ShippingRuleForm, self).__init__(*la, **kwa)
        self.countries_qs = Country.objects.all()

        self.fields['countries'].widget = forms.SelectMultiple(
            attrs={"class": "m2m"})
        self.fields['countries'].queryset = self.countries_qs

        self.fields['rule_price'].widget = FixedCurrencyWidget(
            attrs={"class": "price input-currency money"})
        self.fields['rule_price'].label = _('First item')
        self.fields['rule_price'].required = True

        self.fields['rule_price_extra'].widget = FixedCurrencyWidget(
            attrs={"class": "price input-currency money"})
        self.fields['rule_price_extra'].label = _('Subsequent items')
        self.fields['rule_price_extra'].required = True

        self.fields['despatch_time'].widget = forms.TextInput(
            attrs={"class": "number input-number"})

        self.fields['delivery_time'].widget = forms.TextInput(
            attrs={"class": "number input-number"})
        self.fields['delivery_time_max'].widget = forms.TextInput(
            attrs={"class": "number input-number"})

    class Meta:
        model = ShippingRule
        fields = ('countries', 'profile', 'rule_price', 'rule_price_extra',
                  'despatch_time', 'delivery_time', 'delivery_time_max')

ShippingRulesFormset = inlineformset_factory(
    ShippingProfile, ShippingRule,
    form=ShippingRuleForm,
    can_delete=True,
    extra=1)


class SuggestedCertificateForm(forms.ModelForm):

    def __init__(self, *la, **kwa):
        self.request = kwa.pop('request', None)
        super(SuggestedCertificateForm, self).__init__(*la, **kwa)
        self.fields['title'].label = _('Name of certificate')
        self.fields['url'].label = _('Organisation website')
        self.fields['url'].widget = forms.TextInput()
        self.fields['description'].label = _('Description of certificate')

    class Meta:
        model = SuggestedCertificate

ProductSuggestedCertificateFormset = inlineformset_factory(
    Product, SuggestedCertificate,
    form=SuggestedCertificateForm,
    can_delete=False, max_num=1)
