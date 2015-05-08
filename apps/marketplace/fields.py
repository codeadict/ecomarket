from StringIO import StringIO
import os

try:
    from PIL import Image
    Image
except:
    import Image

from django.conf import settings
from django import forms
from django.utils.translation import ugettext as _
from django.core.exceptions import ValidationError

from django_thumbs.settings import \
    THUMBS_GENERATE_MISSING_THUMBNAILS

from money.contrib.django.models.fields import \
    MoneyField, MoneyFieldProxy, Money, SUPPORTED_LOOKUPS, \
    NotSupportedLookup
from money.contrib.django.models.managers import \
    MoneyManager
from money.contrib.django.forms import fields as money_forms


from image_crop.fields import \
    ImageWithFixedAspectThumbsField, ImageWithPreviewField, \
    ImageWithFixedAspectThumbsFieldFile

from image_crop.utils import retrieve_cropped_image, idnormalizer


class MoneyFormField(money_forms.MoneyField):

    def clean(self, value):
        if value[0] in [u'', '', None]:
            return None
        return super(MoneyFormField, self).clean(value)


class NullableMoneyFieldProxy(MoneyFieldProxy):

    def _money_from_obj(self, obj):
        if obj.__dict__[self.field.name] == None:
            return None
        return Money(
            obj.__dict__[self.field.name],
            obj.__dict__[self.currency_field_name])


class NullableMoneyField(MoneyField):

    def contribute_to_class(self, cls, name):
        super(NullableMoneyField, self).contribute_to_class(cls, name)
        setattr(cls, self.name, NullableMoneyFieldProxy(self))

        if not hasattr(cls, '_default_manager'):
            cls.add_to_class('objects', MoneyManager())

    def get_prep_lookup(self, lookup_type, value):
        # Necessary because the python-money version is broken
        if not lookup_type in SUPPORTED_LOOKUPS:
            raise NotSupportedLookup(lookup_type)
        if hasattr(value, "amount"):
            value = value.amount
        return super(MoneyField, self).get_prep_lookup(lookup_type, value)

    def formfield(self, **kwargs):
        defaults = {'form_class': MoneyFormField}
        defaults.update(kwargs)
        return super(MoneyField, self).formfield(**defaults)


class ProductImageThumbsFieldFile(ImageWithFixedAspectThumbsFieldFile):

    def _url_for_size(self, size):
        """Return a URL pointing to the thumbnail image of the requested size.
        If `THUMBS_GENERATE_MISSING_THUMBNAILS` is True,
        the thumbnail will be created if it doesn't exist on disk.

        Arguments:
        size  -- A tuple with the desired width and height. Example: (100, 100)

        """
        if not self:
            return ''

        # generate missing thumbnail if needed
        fileBase, extension = self.name.rsplit('.', 1)
        thumb_file = self.THUMB_SUFFIX % (
            fileBase, size[0], size[1], extension)
        if THUMBS_GENERATE_MISSING_THUMBNAILS:
            if not self.storage.exists(thumb_file):
                try:
                    self._generate_thumb(
                        self.storage.open(self.name), size)
                except:
                    if settings.DEBUG:
                        import sys
                        print "Exception generating thumbnail"
                        print sys.exc_info()
        urlBase, extension = self.url.rsplit('.', 1)
        thumb_url = self.THUMB_SUFFIX % (
            urlBase, size[0], size[1], extension)
        return thumb_url


class ProductImageThumbsField(ImageWithFixedAspectThumbsField):
    attr_class = ProductImageThumbsFieldFile

    def generate_filename(self, instance, name):
        ext = name.split('.').pop().lower()
        if instance.name:
            basename = idnormalizer.normalize(instance.name)
        elif len(name) > 36 and name[36] == '_':
            basename = name[37: -(len(ext) + 1)]
        else:
            basename = name

        name = '%s.%s' % (basename, ext)
        dirpath = os.path.join(
            self.upload_to,
            str(instance.product.stall.identifier),
            instance.product.slug,
            'thumbs')
        return os.path.join(dirpath, name)


class ProductImageFormField(forms.ImageField):

    widget = forms.widgets.TextInput

    default_error_messages = {
        'invalid_image': _(
            u"Upload a valid image. The file you uploaded was either not an "
            + "image or a corrupted image."),
    }

    def to_python(self, data):
        """
        Checks that the file-upload field data contains a valid image
        (GIF, JPG, PNG, possibly others -- whatever the Python Imaging
        Library supports).
        """
        cropped_image = retrieve_cropped_image(data)

        if not cropped_image:
            return data

        f = cropped_image['content']

        try:
            # load() could spot a truncated JPEG, but it loads the entire
            # image in memory, which is a DoS vector. See #3848 and #18520.
            # verify() must be called immediately after the constructor.
            Image.open((StringIO(f.read()))).verify()
        except ImportError:
            # Under PyPy, it is possible to import PIL. However, the underlying
            # _imaging C module isn't available, so an ImportError will be
            # raised. Catch and re-raise.
            raise
        # Python Imaging Library doesn't recognize it as an image
        except Exception:
            raise ValidationError(self.error_messages['invalid_image'])

        if hasattr(f, 'seek') and callable(f.seek):
            f.seek(0)
        return f


class ProductImageField(ImageWithPreviewField):

    def formfield(self, **kwa):
        defaults = {'form_class': ProductImageFormField}
        defaults.update(kwa)
        return super(ProductImageField, self).formfield(**defaults)

    def generate_filename(self, instance, name):
        dirpath = os.path.join(
            self.upload_to,
            str(instance.product.stall.identifier),
            instance.product.slug)
        return os.path.join(dirpath, name)


# South introspection rules
try:
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules(
        patterns=["^marketplace\.fields\.NullableMoneyField"],
        rules=[
            (   (NullableMoneyField,),
                [],
                {'no_currency_field': ('add_currency_field', {})}
            )
        ]
    )
except ImportError:
    # South isn't installed
    pass
