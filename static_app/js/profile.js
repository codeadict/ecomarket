/*jslint browser: true*/
/*global Ecomarket, $ */
"use strict";

$(document).ready(function () {
    var split_file_ext, upload_button, avatar_crop_widget;

    split_file_ext = function (filename) {
        return {
            root: filename.substr(0, filename.lastIndexOf('.')),
            ext: filename.substr(filename.lastIndexOf('.') + 1)
        };
    };

    avatar_crop_widget = function (clicked, data) {
        data.url = $(clicked).attr('data-crop');
        data.target = $(clicked).attr('data-target');
        new Ecomarket.ImageCrop
            .CropModal($(data.target), data, function (filename, filetitle, data) {
                var split_filename, filepath, photo;

                split_filename = split_file_ext(filename);
                filepath = '/media/image_crop/standard/'
                    + split_filename.root + '.100x100.' + split_filename.ext;

		photo = $(clicked).parents('.photo')

                // update the thumbnail
                $('img', $(clicked))
		    .attr('src', filepath);

                // and the hidden fields
                $('input.image-filename', photo)
		    .val(filename);

                $('input.image-thumbnail', photo)
		    .val(filepath);

                $('input.image-title', photo)
		    .val(filetitle);

		$('input.image-data', photo)
		    .val(JSON.stringify(data));
            });
    }

    upload_button = $("a[data-toggle=modal].add");
    Ecomarket.product_upload_modal = new Ecomarket.ImageCrop.UploadModal(
        upload_button,
        function (clicked, data) {
	    avatar_crop_widget(clicked, data);
        mixpanel.track("uploads avatar");
        },
	function (clicked, data) {
	    var upload_overlay;
            upload_overlay = $($(clicked).attr('data-target'));
	    $('.modal-body', upload_overlay)
		.html('Image upload failed: ' + data.reason);

	}
    );
});
