from django.conf import settings
from django.db.models import ImageField
from django.db.models.fields.files import ImageFieldFile
from django_thumbs.db.models import \
    ImageWithThumbsField, ImageWithThumbsFieldFile
from django_thumbs.settings import \
    THUMBS_GENERATE_MISSING_THUMBNAILS, THUMBS_GENERATE_THUMBNAILS

from image_crop.utils import \
    generate_thumb_maintain_aspect, crop_thumb_to_coords, \
    calculate_auto_crop

#from image_crop.widgets import CroppableFileInput


class ImageWithFixedAspectThumbsFieldFile(ImageWithThumbsFieldFile):

    def _generate_thumb(self, image, size, coords=None):
        """Generates a thumbnail of `size`.

        Arguments:
        image -- An `File` object with the image in its original size.
        size  -- A tuple with the desired width and height. Example: (100, 100)

        """
        base, extension = self.name.rsplit('.', 1)
        thumb_name = self.THUMB_SUFFIX % (base, size[0], size[1], extension)
        thumbnail = crop_thumb_to_coords(
            image, size, coords or calculate_auto_crop(image, 228), extension)
        saved_as = self.storage.save(thumb_name, thumbnail)
        if thumb_name != saved_as:
            raise ValueError('There is already a file named %s' % thumb_name)

    def save(self, name, content, save=True, coords=None):
        super(ImageFieldFile, self).save(name, content, save)
        if THUMBS_GENERATE_THUMBNAILS:
            if self.field.sizes:
                for size in self.field.sizes:
                    try:
                        self._generate_thumb(content, size, coords)
                    except:
                        if settings.DEBUG:
                            import sys
                            print "Exception generating thumbnail"
                            print sys.exc_info()


class ImageWithFixedAspectThumbsField(ImageWithThumbsField):
    attr_class = ImageWithFixedAspectThumbsFieldFile

    def __init__(self, verbose_name=None, name=None,
                 width_field=None, height_field=None,
                 sizes=None, aspect_ratio=None, **kwargs):
        self.verbose_name = verbose_name
        self.name = name
        self.width_field = width_field
        self.height_field = height_field
        self._sizes = sizes
        self.aspect_ratio = aspect_ratio
        self.coords = None
        super(ImageField, self).__init__(**kwargs)

    @property
    def sizes(self):
        sizes = map(lambda x: (x, self.aspect_ratio * x), self._sizes)
        return sizes


class ImageWithPreviewFieldFile(ImageWithThumbsFieldFile):
    THUMB_SUFFIX = '%s.%s.%s'
    THUMB_PREVIEW_SUFFIX = '%s.preview.%s'

    def _generate_thumb(self, image, size=None):
        """Generates a thumbnail of `size`.

        Arguments:
        image -- An `File` object with the image in its original size.
        size  -- A tuple with the desired width and height. Example: (100, 100)

        """
        base, extension = self.name.rsplit('.', 1)
        thumb_name = self.THUMB_SUFFIX % (base, 'preview', extension)
        thumbnail = generate_thumb_maintain_aspect(
            image, self.field.preview_size, extension)
        saved_as = self.storage.save(thumb_name, thumbnail)
        if thumb_name != saved_as:
            raise ValueError('There is already a file named %s' % thumb_name)

    def __getattr__(self, name):
        """Return the url for the requested size.

        Arguments:
        name -- The field `url` with size suffix
                formatted as _WxH. Example: instance.url_100x70

        """
        sizeStr = name.replace("url_", "")
        if sizeStr == 'preview':
            return self._url_for_preview()
        return super(ImageWithPreviewFieldFile, self).__getattr__(name)

    def _url_for_preview(self):
        """Return a URL pointing to the preview image
        """
        if not self:
            return ''
        fileBase, extension = self.name.rsplit('.', 1)
        thumb_file = self.THUMB_PREVIEW_SUFFIX % (fileBase, extension)
        if THUMBS_GENERATE_MISSING_THUMBNAILS:
            if not self.storage.exists(thumb_file):
                try:
                    self._generate_thumb(
                        self.storage.open(self.name))
                except:
                    if settings.DEBUG:
                        import sys
                        print "Exception generating thumbnail"
                        print sys.exc_info()
        urlBase, extension = self.url.rsplit('.', 1)
        thumb_url = self.THUMB_PREVIEW_SUFFIX % (urlBase, extension)
        return thumb_url


class ImageWithCroppedThumbsField(ImageWithFixedAspectThumbsField):
    #widget = CroppableFileInput
    pass


class ImageWithPreviewField(ImageWithThumbsField):
    attr_class = ImageWithPreviewFieldFile

    def __init__(self, verbose_name=None, name=None,
                 width_field=None, height_field=None,
                 preview_size=None, **kwargs):
        self.verbose_name = verbose_name
        self.name = name
        self.width_field = width_field
        self.height_field = height_field
        self.preview_size = preview_size
        super(ImageField, self).__init__(**kwargs)

    @property
    def sizes(self):
        return (self.preview_size,)

    def thumbnail(self, widthOrSize, height=None):
        """
        Return the thumbnail url for an specific size.
        The same thing as url_[width]x[height] without the magic.

        Arguments:
        widthOrSize -- Width as integer or size as tuple.
        height      -- Height as integer. Optional,
                       will use `widthOrSize` as height if missing.

        Usage:
        instance.thumbnail(48, 48)
        instance.thumbnail(64)
        instance.thumbnail( (100, 70) )

        """
        if type(widthOrSize) is tuple:
            size = widthOrSize
        else:
            if height is None:
                height = widthOrSize
            size = (widthOrSize, height)
        return self.__getattr__('url_%sx%s' % (size[0], size[1]))
