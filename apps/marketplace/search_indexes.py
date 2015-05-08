from haystack import indexes
from .models import Product
 
class RealTimeSearchIndex(indexes.RealTimeSearchIndex):
    """
    A variant of the stock ``RealTimeSearchIndex`` that constantly keeps the
    index fresh, including removing an object when it is saved to a state such
    that it should no longer be in the index. (The latter is not done by the
    stock one.)
 
    """
 
    def should_update(self, instance, **kwargs):
        """
        Determine if an object should be updated in the index.
 
        Different from the stock method in that this one does not always
        return true. Rather, we verify that we should actually update the
        object.
 
        """
        if instance in self.index_queryset():
            return True
        return False
 
    def update_object(self, instance, using=None, **kwargs):
        """
        Update the index for a single object. Attached to the class's
        post-save hook.
 
        """
        # Check to make sure we want to index this first.
        if self.should_update(instance, **kwargs):
            self._get_backend(using).update(self, [instance])
        else:
            # Otherwise, remove it.
            self.remove_object(instance)

class ProductIndex(RealTimeSearchIndex, indexes.Indexable):
    stall_name = indexes.CharField(model_attr='stall__title')
    title = indexes.CharField(model_attr='title')
    description = indexes.CharField(model_attr='description')
    slug = indexes.CharField(model_attr='slug')
    categories = indexes.MultiValueField()
    price = indexes.FloatField()
    ships_from = indexes.CharField(model_attr='ships_from_country')
    ships_to = indexes.MultiValueField()
    status = indexes.CharField(model_attr='status')

    causes = indexes.CharField(document=False, use_template=True)
    certificates = indexes.CharField(document=False, use_template=True)
    colors = indexes.MultiValueField()
    ingredients = indexes.CharField(document=False, use_template=True)
    materials = indexes.CharField(document=False, use_template=True)
    keywords = indexes.MultiValueField()
    occasions = indexes.CharField(document=False, use_template=True)
    recipients = indexes.CharField(document=False, use_template=True)

    number_of_recent_sales = indexes.IntegerField(document=False, model_attr="number_of_recent_sales")
    number_of_sales = indexes.IntegerField(document=False, model_attr="number_of_sales")

    created = indexes.DateTimeField(model_attr='created')
    updated = indexes.DateTimeField(model_attr='updated')
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return Product

    def index_queryset(self):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.filter(status=Product.PUBLISHED_LIVE).exclude(stock=0)

    def read_queryset(self):
        return self.get_model().objects.select_related('stall__identifier').prefetch_related('prices')

    def extract_category_ids(self, category):
        cats = []
        if category:
            categories = category.get_ancestors()
            cats = [c.id for c in categories] + [category.id]
        return cats

    def prepare_keywords(self, obj):
        return [k.title for k in obj.keywords.all()]

    def prepare_colors(self, obj):
        return [c.id for c in obj.colors.all()]

    def prepare_categories(self, obj):
        """Used to extract the 2nd level category of a category tree"""
        return self.extract_category_ids(obj.primary_category) + self.extract_category_ids(obj.secondary_category)

    def prepare_ships_to(self, obj):
        ship_rules = obj.shipping_profile.shipping_rules.all()
        ships_to = [country.code for rule
                    in ship_rules for country in
                    rule.countries.all()]

        if obj.shipping_profile.ships_worldwide():
            ships_to = ['worldwide']
        return ships_to

    def prepare_price(self, obj):
        """this will change for multiple currencies"""
        return obj.get_price_instance().amount
