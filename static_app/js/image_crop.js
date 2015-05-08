/*jslint browser: true*/
/*global qq, document, Ecomarket, $, csrfmiddlewaretoken */
"use strict";

function InitUploader(selector, url, instructions, onUploadComplete) {
  return function () {
    var uploader;
    uploader = new qq.FileUploader({
      element: $(selector)[0],
      action: url,
      params: {
        'csrf_token': csrfmiddlewaretoken,
        'csrf_name': 'csrfmiddlewaretoken',
        'csrf_xname': 'X-CSRFToken'
      },
      onComplete: onUploadComplete,
      onProgress: function (id, filename, bytesUploaded, bytesTotal) {
        var progress = (bytesUploaded / bytesTotal * 100) + '%'
        $('.ecomarket-progress.hide').removeClass('hide')
        $('.ecomarket-progress .bar').css('width',
          progress)
      },
      instructions: instructions
    });
  };
}

Ecomarket.ImageCrop.CropModal = function (selector, params, onCroppingComplete) {
  var crapi, setup_jcrop, show_preview, close, modal, setup_handlers;
  modal = "#uploadModal";
  close = "button[data-dismiss=modal].close";
  var crop_coords = [];

  show_preview = function (coords, preview_width, preview_height) {
    var rx, ry, preview;
    rx = 100 / coords.w;
    ry = 100 / coords.h;
    preview = 'img#crop-image-preview';
    $(preview).css({
      width: Math.round(rx * preview_width) + 'px',
      height: Math.round(ry * preview_height) + 'px',
      marginLeft: '-' + Math.round(rx * coords.x) + 'px',
      marginTop: '-' + Math.round(ry * coords.y) + 'px'
    });
  };

  setup_handlers = function () {
    $('a[name=cancel-image-upload]',
      selector)
      .click(function (evt) {
        // TODO: send notification to server
        evt.preventDefault();
        $(close).click();
        $(modal).html('');
      });

    $('a[name=submit-image-upload]',
      selector)
      .bind('click',
      function (evt) {
        var selection, crop_url, filetitle, title_input;
        evt.preventDefault();
        selection = crapi.tellSelect();
        title_input = $(this).parents('form').find('input[name=file-title]');
        filetitle = title_input.val();

        // Unfortunately it is possible to remove the crop area.
        // If someone manages do to it the image (width=0, heigth=0) cannot be created.
        // In those cases we use the default crop area
        if (selection.w < 30 || selection.h < 30) {
          selection.x = crop_coords[0];
          selection.y = crop_coords[1];
          selection.x2 = crop_coords[2];
          selection.y2 = crop_coords[3];
        }

        crop_url = '/image-crop/crop_image/?'
          + 'filename=' + params.filename
          + '&file-title=' + filetitle
          + '&xl=' + selection.x + '&xr=' + selection.x2
          + '&yt=' + selection.y + '&yb=' + selection.y2;

        if (filetitle) {
          $.ajax({
            url: crop_url
          }).done(function (data) {
              if (data.success) {
                onCroppingComplete(data.filename,
                  data.filetitle,
                  data.data);
                $(close).click();
                $(modal).html('');
              } else {
                // TODO: handle cropping failure
              }
            });
        } else {
          title_input.parents('.control-group').addClass('error');
        }
      });
  };

  setup_jcrop = function (ratio, preview_width, preview_height) {
    var max_height, min_width, min_height,
      x1, x2, y1, y2, crop_size, aspectRatio;

    min_width = 228 * ratio;
    min_height = 228 * ratio;

    if (preview_height > preview_width) {
      max_height = preview_width;
    } else if (preview_height <= preview_width) {
      max_height = preview_height;
    }

    if ((0.8 * max_height) > min_height) {
      crop_size = 0.8 * max_height;
    } else if ((0.9 * max_height) > min_height) {
      crop_size = 0.9 * max_height;
    } else {
      crop_size = max_height;
    }

    x1 = (preview_width - crop_size);
    if (x1) {
      x1 = x1 / 2;
    }
    x2 = x1 + crop_size;

    y1 = (preview_height - crop_size);
    if (y1) {
      y1 = y1 / 2;
    }
    y2 = y1 + crop_size;

    crop_coords = [x1, y1, x2, y2];

    selector.find('img#crop-image').Jcrop(
      aspectRatio = 1,
      function () {
        setup_handlers();
        crapi = this;
        crapi.setOptions({
          allowMove: true,
          allowResize: true,
          onChange: function (coords) {
            show_preview(coords,
              preview_width,
              preview_height);
          },
          onSelect: function (coords) {
            show_preview(coords,
              preview_width,
              preview_height);
          },
          minSize: [min_width, min_height],
          aspectRatio: 1
        });
        crapi.animateTo(crop_coords);
      }
    );
  };

  $(params.target)
    .load(params.url,
    'filename=' + params.filename,
    function (data) {
      setup_jcrop(
        params.ratio,
        params.preview_height,
        params.preview_width
      );
    });
};

Ecomarket.ImageCrop.UploadModal = function (selector, onUploadComplete, onUploadFail) {
  selector.on("click",
    function (event) {
      var $this, url, target, uploader_selector, instructions;
      url = $(this).attr('data-source');
      target = $(this).attr('data-target');
      uploader_selector = '#file-uploader';
      instructions = $(this).attr('data-upload-instructions');
      $this = this;
      $(target)
        .load(url,
          new InitUploader(uploader_selector,
            url,
            instructions,
            function (id, orig_filename, data) {
              if (data.success) {
                onUploadComplete($this,
                  data);
              } else {
                onUploadFail($this,
                  data);
              }
            }));
    });
};
