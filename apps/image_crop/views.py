import os
import logging
import math
import uuid

try:
    from PIL import Image
    Image
except:
    import Image


from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.auth.decorators import login_required
from django.http import \
    HttpResponse, HttpResponseBadRequest

from django.shortcuts import render
from django.utils import simplejson as json
from django.utils.translation import ugettext as _
from django.views.generic.base import TemplateView

from image_crop.models import TempImage
from image_crop.utils import normalize_filename, validate_uploaded_image
from image_crop.exceptions import ImageUploadError

from main.utils.decorators import view_dispatch_decorator

logger = logging.getLogger(__name__)

CROP_FILEPATH = '/media/image_crop/'


def image_dimensions(image):
    image.seek(0)
    _image = Image.open(image)
    if _image.mode not in ('L', 'RGB', 'RGBA'):
        _image = _image.convert('RGB')
    return _image.size


def get_temp_image_dimensions(temp_image):
    filepath = 'image_crop/original/'
    filebase, fileext = temp_image.filename.rsplit('.', 1)
    orig_path = '%s%s.%s' % (filepath, filebase, fileext)
    prev_path = '%s%s.preview.%s' % (filepath, filebase, fileext)
    storage = temp_image.original.storage
    return {'original': image_dimensions(storage.open(orig_path)),
            'preview':  image_dimensions(storage.open(prev_path))}


@view_dispatch_decorator(login_required)
class ImageCropperAjax(TemplateView):
    """
    """
    template_name = 'image_crop/crop_image.html'

    def get(self, request):
        success = True
        filename = None
        temp_file = None

        # get the crop co-ordinates
        # round up to the nearest pixel
        roundup = lambda x: int(math.ceil(float(x)))
        try:
            xl = roundup(request.GET['xl'])
            xr = roundup(request.GET['xr'])
            yt = roundup(request.GET['yt'])
            yb = roundup(request.GET['yb'])
        except AttributeError:
            success = False
            message = _('Co-ordinates not supplied')

        filetitle = request.GET.get('file-title')

        try:
            filename = normalize_filename(
                request.GET['filename'])
        except AttributeError:
            success = False
            message = _('Filename not supplied')

        try:
            # find the temp image
            if filename:
                temp_file = TempImage.objects.filter(
                    filename=filename)[0]
        except IndexError:
            success = False
            message = _('File %s not found' % filename)

        try:
            # crop it
            if temp_file:
                temp_file.crop_from_preview([xl, xr, yt, yb])
                success = True
                message = _('File cropped')
        except:
            success = False
            message = _('Cropping file %s failed' % filename)

        coords = map(
            lambda x: int(x * temp_file.preview_ratio), [xl, xr, yt, yb])

        context = {
            'filename': filename,
            'filetitle': filetitle,
            'success': success,
            'data': dict(image_crop=coords),
            'message': message}

        return HttpResponse(
            json.dumps(context, cls=DjangoJSONEncoder),
            content_type='application/json; charset=utf-8')


@view_dispatch_decorator(login_required)
class ImageCropperView(TemplateView):
    """
    """
    template_name = 'image_crop/crop.html'

    def get(self, request):
        return TemplateView.get(self, request)

    def get_context_data(self, **kwargs):
        preview_filename = normalize_filename(
            self.request.GET.get(
                'filename'))

        _filename, _ext = os.path.splitext(preview_filename)
        filename = '%s.preview%s' % (_filename, _ext)
        return {
            'original': preview_filename,
            'preview': filename,
            'filepath': '%soriginal/' % CROP_FILEPATH}


@view_dispatch_decorator(login_required)
class FileUploaderAjax(TemplateView):
    """
    Receives files sent by qqUploader
    """
    template_name = 'image_crop/upload.html'

    def _posted_image(self, request):
        upload = request
        filename = normalize_filename(
            request.GET['qqfile'])
        content = upload.read()
        upfile = SimpleUploadedFile(filename, content)
        return filename, upfile

    def _save_temp_image(self, request, filename, upfile):

        image_uuid = uuid.uuid4()
        filename = normalize_filename(
            '%s_%s' % (image_uuid, filename))

        temp_image = TempImage(
            user=request.user, filename=filename,
            uuid=image_uuid)
        temp_image.original.save(filename, upfile, True)
        temp_image.save()
        return temp_image

    def _success_response(self, filename, temp_image):
        # calculate the ratio of the original/preview
        dimensions = get_temp_image_dimensions(temp_image)
        ratio = float(
            dimensions['preview'][0]) / dimensions['original'][0]

        # let Ajax Upload know whether we saved it or not
        context = {
            'success': True,
            'filename': '%s_%s' % (temp_image.uuid, filename),
            'ratio': ratio,
            'preview_height': dimensions['preview'][0],
            'preview_width': dimensions['preview'][1],
            'filepath': '%soriginal/' % CROP_FILEPATH,
            'id': temp_image.id}

        return HttpResponse(
            json.dumps(context, cls=DjangoJSONEncoder),
            content_type='application/json; charset=utf-8')

    def _fail_response(self, reason):
        # let Ajax Upload know whether we saved it or not
        context = {
            'success': False,
            'reason': str(reason)}

        return HttpResponse(
            json.dumps(context, cls=DjangoJSONEncoder),
            content_type='application/json; charset=utf-8')

    def post(self, request):
        try:
            filename, upfile = self._posted_image(request)
        except KeyError:
            return HttpResponseBadRequest("AJAX request not valid")

        try:
            validate_uploaded_image(upfile)
        except ImageUploadError, e:
            return self._fail_response(e)

        try:
            return self._success_response(
                filename,
                self._save_temp_image(request, filename, upfile))
        except KeyError:
            return HttpResponseBadRequest("AJAX request not valid")


def photo(request, template_name='image_crop/photo.html'):
    context = {}
    return render(request, template_name, context)
