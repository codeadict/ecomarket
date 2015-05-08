from django.conf.urls.defaults import patterns, url

from image_crop.views import \
    FileUploaderAjax, ImageCropperView, ImageCropperAjax

urlpatterns = patterns(
    'image_crop.views',
    url(r'^crop/$', ImageCropperView.as_view(),
        name='image_crop_crop'),
    url(r'^crop_image/$', ImageCropperAjax.as_view(),
        name='image_crop_crop_image'),
    url(r'^photo/$', 'photo', name='image_crop_photo'),
)
