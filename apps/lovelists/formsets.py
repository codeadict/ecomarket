from django.core.exceptions import ValidationError
from django.forms.models import BaseInlineFormSet


class LoveListProductFormSet(BaseInlineFormSet):

    def clean(self):
        super(LoveListProductFormSet, self).clean()
        ids = set()
        for form in self.forms:
            if (not hasattr(form, "cleaned_data")
                    or "product_id" not in form.cleaned_data
                    or form.cleaned_data.get("DELETE", False)):
                continue
            product_id = form.cleaned_data["product_id"]
            if product_id in ids:
                raise ValidationError(
                    "Duplicate products found. Please remove any duplicates "
                    "before proceeding.")
            ids.add(product_id)
