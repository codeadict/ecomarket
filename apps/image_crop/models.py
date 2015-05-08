import logging

from django.contrib.auth.models import User
from django.db import models
from django_extensions.db.fields import UUIDField
from django_extensions.db.fields.json import JSONField
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils.translation import ugettext as _

from image_crop.fields \
    import ImageWithFixedAspectThumbsField, ImageWithPreviewField
from image_crop.utils import calculate_size_for_max

logger = logging.getLogger(__name__)


class TempImage(models.Model):
    """
    Temporary model to store ajax uploaded images until the product is saved.
    data is JSON dictionary with the keys
    large_x, large_y, large_w, large_h
    """
    uuid = UUIDField()
    user = models.ForeignKey(User, related_name='images')
    filename = models.CharField(
        max_length=255, blank=True, default='', null=False)
    original = ImageWithPreviewField(
        upload_to='image_crop/original/',
        blank=False, null=False,
        max_length=255,
        preview_size=(300, 200))
    standard = ImageWithFixedAspectThumbsField(
        upload_to='image_crop/standard/',
        aspect_ratio=1, sizes=(100, 200, 300),
        max_length=255,
        blank=False, null=True)
    tag = models.CharField(
        max_length=255, blank=True, default='', null=False)
    data = JSONField(blank=True, default='', null=False)
    created = models.DateTimeField(
        _('Created'),
        auto_now_add=True, editable=False)

    @property
    def preview_ratio(self):
        # TODO: fix this
        max_size = (300, 200)

        preview_width, preview_height = calculate_size_for_max(
            (self.original.width, self.original.height),
            max_size)
        return float(self.original.width) / preview_width

    def crop_from_preview(self, coords):
        # update the thumbnails using the given co-ordinates
        xl, xr, yt, yb = coords

        # x = xr - xl
        # y = yb - yt

        # validate that the co-ordinates match our aspect ratio
        # try:
        #     assert x / y == self.original.field.aspect_ratio
        # except:
        #     pass

        # work out the ratio of the preview to original image
        # multiply co-ordinates by ratio
        # grab the original image
        # crop image from co-ordinates

        self.original.file.open()
        self.original.file.seek(0)
        cropped = self.original.read()

        upfile = SimpleUploadedFile(self.filename, cropped)
        coords = map(
            lambda x: int(x * self.preview_ratio), [xl, yt, xr, yb])

        self.data.update(
            {'coords': {'xl': coords[0],
                        'yt': coords[1],
                        'xr': coords[2],
                        'yb': coords[3]}})

        self.standard.save(
            self.filename, upfile, True, coords)

        self.save()
