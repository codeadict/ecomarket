from django.core.exceptions import ValidationError
import django.forms as forms

from marketplace.models import Category

from lovelists.models import LoveList

from marketplace.models import Product


class LoveListForm(forms.ModelForm):

    widget_attrs = {
        "title": {
            "placeholder": ("Give your love list a name; be creative. "
                            "For example 'purrrfect eco treats for the cat'"),
        },
        "description": {
            "placeholder": ("Add a description. For example 'A collection of "
                            "my favourite eco friendly presents for cats, "
                            "because they're worth it too!'"),
            "style": "height: 6em",
        },
        "primary_category": {
            "class": "multiple-dropdown",
            "data-placeholder": "Main category",
        },
        "secondary_category": {
            "class": "multiple-dropdown",
            "data-placeholder": "Optional second category",
        },
        "tertiary_category": {
            "class": "multiple-dropdown",
            "data-placeholder": "Optional third category",
        },
        "is_public": {
            "class": "eco-checkbox",
        },
    }

    def __init__(self, *args, **kwargs):
        super(LoveListForm, self).__init__(*args, **kwargs)
        for field_name, attrs in self.widget_attrs.iteritems():
            self.fields[field_name].widget.attrs.update(attrs)
        category_list = [("", "")] + list(
                Category.objects.values_list("id", "name"))
        for field_name in ["primary_category", "secondary_category",
                           "tertiary_category"]:
            self.fields[field_name].choices = category_list

    class Meta:
        model = LoveList
        fields = ("title", "description", "primary_category",
                  "secondary_category", "tertiary_category", "is_public")


class LoveListProductForm(forms.ModelForm):

    # This holds, at various times, both the slug and the ID, hence the
    # dubious naming
    product_id = forms.CharField(label="Product Slug")

    def __init__(self, initial=None, instance=None, *args, **kwargs):
        if initial is None:
            initial = {}
        if instance is not None and "product_id" not in initial:
            initial["product_id"] = instance.product.slug
        return super(LoveListProductForm, self).__init__(
            *args, initial=initial, instance=instance, **kwargs)

    def clean_product_id(self):
        slug = self.cleaned_data["product_id"]
        try:
            product = Product.objects.get(slug=slug)
        except Product.DoesNotExist:
            raise ValidationError("Please enter an existing product slug")
        return product.id

    def save(self, commit=True):
        self.instance.product_id = self.cleaned_data["product_id"]
        return super(LoveListProductForm, self).save(commit=commit)

    class Meta:
        fields = ("product_id", "weight")
