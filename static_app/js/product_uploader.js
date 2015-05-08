/*jslint browser: true*/
/*global Ecomarket, $, jQuery */
"use strict";

Ecomarket.Product.Info = function (fieldset) {
    // open the secondary category select when primary is changed
    var open;
    open = false;

    $('.categories .em-dropdown-choice').on(
        'click',
        function (evt) {
            if (!open) {
                $(this).parents(fieldset).find('.secondary-category')
                    .removeClass('hidden')
                    .hide().slideDown(function () {
                        $(this).css('overflow', "visible");
                    });
                open = true;
            }
        }
    );
};

Ecomarket.Product.StockLevel = function () {
    // show/hide stock level
    $('select#stock-level')
        .on('change', function (evt) {
            var fixed, stock, slide;
            stock = $(this).parents('fieldset.stock').find('.control-group.stock');
            slide = ($(this).val() === 'fixed') ? stock.slideDown() : stock.slideUp();
        });
};

Ecomarket.Product.Causes = function (fieldset) {
    var open;
    open = false;

    // open the certificates select when causes is changed
    $(fieldset + ' #select-id_causes')
        .on('change', function (evt) {
            if (!open) {
                $(this).parents(fieldset)
                    .find('.control-group.certificates')
                    .slideDown();
            }
        });

    // trigger to show new certificate
    $(fieldset + ' .suggest-certificate').on('click', function (e) {
        e.preventDefault();
        $(this).parent().fadeOut();
        $('.new-certificate').slideToggle();
    });
};


$(document).ready(function () {
    Ecomarket.product_info = new Ecomarket.Product.Info('fieldset.info');
    Ecomarket.product_stock_level = new Ecomarket.Product.StockLevel('fieldset.stock');
    Ecomarket.product_causes = new Ecomarket.Product.Causes('fieldset.causes');

});

Ecomarket.Widgets.RemoveM2M = function () {
    $(document)
        .on('click',
            '.tags-editable.tags-list .tag',
            this.remove_m2m.bind(this));
};

Ecomarket.Widgets.RemoveM2M.prototype.remove_m2m = function (evt) {
    // get select in context of links parent container
    evt.preventDefault();
    var $tag, $select, $em, text, value, $hidden_select;
    $tag = $(evt.target);
    if ($tag.hasClass('m2m-icon')) {
        $select = $(".tagger-select", $tag.parents('.controls'));
        $hidden_select = $("select.m2m", $tag.parents('.controls'));
        $em = $tag.parent().prev();
        text = $em.html();
        value = $em.attr('data-value');
        if( value === undefined ) {
            value = $em.attr('value');
        }
        $tag.parent().parent().remove();
        //$select.append(
        //    "<option value=" + value + ">" + text + "</option>");
        $('option[value="' + value + '"]', $hidden_select).remove();
    }
};
// M2M Color picker

Ecomarket.Widgets.ColorPickerM2M = function () {
    if (".color-picker-m2m".length === 0) {
        return;
    }
    this.initialize();
};

Ecomarket.Widgets.ColorPickerM2M.prototype.initialize = function () {
    $('.color-picker-m2m').hide().next().removeClass('hidden');
    $(document).on('click', '.m2m-colorpicker-current-choice', this.toggleDropdown.bind(this));
    $(document).on('click', '.m2m-colorpicker-list a', this.choice.bind(this));
    $('.m2m-colorpicker-list a').each(function (index, item) {
        $(item).css('background-color', $(item).data('value'));
        $(item).attr('title', $(item).data('value'));
    });
    // loading default value
    $(".color-picker-m2m").each(function (index, item) {
        var $hidden_select, $wrap, value, i;
        $hidden_select = $(this);
        value = $hidden_select.val();
        if ((value !== null) && (value.length > 0)) {
            $wrap = $hidden_select.next();
            for (i = 0; i < value.length; i += 1) {
                $wrap.find(".m2m-colorpicker-list a[data-source=" + value[i] + "]").click();
                $wrap.find(".m2m-colorpicker-current-choice").click();
            }
        }
    });
};

Ecomarket.Widgets.ColorPickerM2M.prototype.toggleDropdown = function (event) {
    var dropdown;
    event.preventDefault();
    dropdown = $(event.target).parents('.m2m-colorpicker');
    dropdown
        .toggleClass('m2m-colorpicker-collapsed')
        .toggleClass("m2m-colorpicker-expanded");
};

Ecomarket.Widgets.ColorPickerM2M.prototype.choice = function (event) {
    var colorpicker, item, id, value, value_text, tags, selecteds;
    event.preventDefault();
    colorpicker = $(event.target).parents('.m2m-colorpicker');
    item = $(event.target);

    // toggle dropdown
    colorpicker
        .toggleClass('m2m-colorpicker-collapsed')
        .toggleClass("m2m-colorpicker-expanded");

    // clean all expanded classes
    colorpicker.find('.active').removeClass('active');

    // apply selected option
    id = item.data('source');
    value = item.data('value');
    value_text = item.html();

    $('.m2m-colorpicker-value', colorpicker)
        .html(value_text);

    tags = $('.m2m-colors-tags-list', colorpicker.parent());
    selecteds = tags.find('em[data-value=' + id + ']');
    if (selecteds.length === 0) {
        // get tags list in context of select parent
        tags = $('.m2m-colors-tags-list', colorpicker.parent());
        tags.append('<span class="tag m2m-colors-tag"><em data-value="'
                    + id + '">' + value_text
                    + '</em><a href="#" class="tag-remove">'
                    + '<i class="icon icon-remove-sign m2m-colors-icon">'
                    + '</i></a></span>');

        // select this item in the hidden multiselect
        colorpicker.prev()
            .children('option[value=' + id + ']')
            .attr('selected', 'selected');
    }
};

Ecomarket.Widgets.ColorRemoveM2M = function () {
    $(document)
        .on('click',
            '.m2m-colors-tags-editable.m2m-colors-tags-list .m2m-colors-tag',
            this.remove_m2m.bind(this));
};

Ecomarket.Widgets.ColorRemoveM2M.prototype.remove_m2m = function (event) {
    // get select in context of links parent container
    event.preventDefault();
    var $tag, $select, $em, text, value, $parent;
    $tag = $(event.target);
    if ($tag.hasClass('m2m-colors-icon')) {
        $parent = $tag.parent().parent();
        $select = $("select.color-picker-m2m",
                    $parent.parents('.controls'));
        $em = $tag.parent().prev();
        text = $em.html();
        value = $em.attr('data-value');
        $parent.remove();
        $select
            .children('option[value=' + value + ']')
            .removeAttr('selected');
    }
};

jQuery(document).ready(function ($) {
    var split_file_ext, upload_button, crop_widget, update_formset_node;

    $('.image-name').each(function(){
        if( $(this).val() ) {
            $(this).show();
        }
    });

    Ecomarket.m2m_select = new Ecomarket.Widgets.SelectM2M();
    Ecomarket.m2m_remove = new Ecomarket.Widgets.RemoveM2M();
    Ecomarket.m2m_color_picker = new Ecomarket.Widgets.ColorPickerM2M();
    Ecomarket.m2m_color_remove = new Ecomarket.Widgets.ColorRemoveM2M();
    Ecomarket.m2m_certificates = new Ecomarket.Widgets.Selects(
        $('.ajax-causes-select'),
        function ($this) {
            var target;
            target = $($this).attr('data-target');
            // select2 seems to require an id being set, strange
            // this needs fixing
            return {
                id: function (e) {
                    return e.value;
                },
                minimumResultsForSearch: 99,
                ajax: {
                    url: target,
                    data: function () {
                        var causes = [];
                        $($this).parents('fieldset.causes')
                            .find('#id_causes option:selected').each(function () {
                                causes.push($(this).val());
                            });
                        return {causes: causes};
                    },
                    results: function (data) {
                        return {results: data};
                    },
                },
                formatResult: function (result) {
                    return result.term;
                }
            };
        }
    );

    split_file_ext = function (filename) {
        return {
            root: filename.substr(0, filename.lastIndexOf('.')),
            ext: filename.substr(filename.lastIndexOf('.') + 1)
        };
    };

    // remove unwanted photos
    $('.photo .toolbar .remove a')
        .live('click', function (evt) {
            evt.preventDefault();
            $(this).parents('.photo-container')
		.prev().find('input').attr('checked', 'checked');
            $(this).parents('.photo-container')
                .remove();
        });

    // recrop an image
    $('.photo .toolbar .edit a')
        .live('click', function (evt) {
            evt.preventDefault();
        });

    update_formset_node = function (els, prefix, id) {
	var id_regex, name_regex, replacement, s2_regex, el;

	id_regex = new RegExp('(id_' + prefix + '-\\d+)');
	name_regex = new RegExp('(' + prefix + '-\\d+)');
	s2_regex = new RegExp('(s2id_select-id_' + prefix + '-\\d+)');

	els.each(function () {
	    el = $(this);
	    if (el.attr('id')) {
		if (el.attr('id').substring(0, 15) == "s2id_select-id_") {
		    replacement = 's2id_select-id_' + prefix + '-' + id;
		    el.attr('id', el.attr('id')
			    .replace(s2_regex, replacement));
		} else {
		    replacement = 'id_' + prefix + '-' + id;
		    el.attr('id', el.attr('id')
			    .replace(id_regex, replacement));
		}
	    }
	    if (el.attr('name')) {
		replacement = prefix + '-' + id;
		el.attr('name', el.attr('name')
			.replace(name_regex, replacement));
	    }
	    if (el.attr('for')) {
		replacement = 'id_' + prefix + '-' + id;
		el.attr('for', el.attr('for')
			.replace(id_regex, replacement));
	    }
	});
    };

    crop_widget = function (clicked, data) {
	// TODO: get the prefix from the node
	var prefix, id_regex, name_regex;

	prefix = 'thumbs';
	id_regex = new RegExp('(id_' + prefix + '-\\d+)');
	name_regex = new RegExp('(' + prefix + '-\\d+)');
        data.url = $(clicked).attr('data-crop');
        data.target = $(clicked).attr('data-target');
        new Ecomarket.ImageCrop
            .CropModal($(data.target), data, function (filename, filetitle, data) {
                var placeholder, containers, containers_maxed, photo_field,
		clicked_container, split_filename, filepath,
		new_container, new_id, new_container_id, replacement,
		form_totals_node, form_total;

		photo_field = $(clicked).parents('fieldset.photos');
		clicked_container = $(clicked).parents('.photo-container');
                containers = $('.photo-container', photo_field);
                split_filename = split_file_ext(filename);

		// TODO: get the cropped filepath from the server
                filepath = '/media/image_crop/standard/'
                    + split_filename.root + '.100x100.' + split_filename.ext;

		if (clicked_container.is(containers.last()) && containers.length < 10) {
		    containers.last()
			.after(containers.last().clone(true));
		    containers = $('.photo-container', photo_field);
		    new_container = containers.last();
		}

		form_totals_node = $('input[name="' + prefix + '-TOTAL_FORMS' + '"]',
				     photo_field);

		form_total = parseInt(form_totals_node.val(), 10);

		// increment the number of forms
		form_totals_node
		    .val(form_total + 1)

		$('input.image', clicked_container)
		    .val(filename);

		$('input.image-data', clicked_container)
		    .val(JSON.stringify(data));

		$('input.image-filename', clicked_container)
		    .val(filename.split('/').pop());

		$('input.image-name', clicked_container)
		    .val(filetitle).show();

		$('.photo img', clicked_container).attr('src', filepath).show()
		new_id = containers.length - 1;
		replacement = prefix + '-' + new_id;
		if (new_container) {
		    update_formset_node(new_container, prefix, new_id);
		    update_formset_node($('*', new_container), prefix, new_id);
		}
            });
    };

    upload_button = $("a[data-toggle=modal].add");
    Ecomarket.product_upload_modal = new Ecomarket.ImageCrop.UploadModal(
        upload_button,
        function (clicked, data) {
	    return crop_widget(clicked, data)
        },
	function (clicked, data) {
	    var upload_overlay;
            upload_overlay = $($(clicked).attr('data-target'));
	    $('.modal-body', upload_overlay)
		.html('Image upload failed: ' + data.reason);
	}
    );
});