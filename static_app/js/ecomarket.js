/*jslint browser: true*/
/*global $, ZeroClipboard, jQuery, mixpanel */
"use strict";

/* Like Django truncatechars
 * https://docs.djangoproject.com/en/1.5/ref/templates/builtins/#truncatechars
 */
String.prototype.truncatechars = function(n){
    return this.substr(0,n-1)+(this.length>n?'&hellip;':'');
};

var Ecomarket;

window.Ecomarket = {
    Widgets: {},
    Product: {}, Messaging: {},
    Purchase: {},
    MyAccount: {},
    ImageCrop: {},
    Stall: {}
};


Ecomarket.Widgets.ActivitiesButton = function (activities_button) {
    $(document)
    .on('click', activities_button, function(evt) {
        evt.preventDefault();
        $('#activities-modal')
        .load('/activities/info/').modal({});
    });
};

/* login form */
Ecomarket.Widgets.ModalLogin = function () {
    $(document).on('click', '.modal-login .toggle a, .modal-login a.switch-to-register, .modal-register .toggle a, .modal-register a.switch-to-login', this.toggle.bind(this));
    $(document).on('click', '.modal-login a.show-register', this.show_register.bind(this));
    var login_modal = $('#login');
    if( login_modal.length ) {    
        /* This allows us to change the login form action temporarily
         * e.g. for the Follow form we want ?next=/follow/action so the user
         *      performs the follow action after login.
         * When the login dialog is hidden the form action is reset to what it
         * was before :)
         */
        var login_form = $('.login-form', login_modal);
        login_modal.on('show', function (event) {
            var new_action = login_modal.data('tempAction');
            if( new_action ) {
                var facebook_action = new_action.replace(/\/(accounts\/login|register)\//, '/accounts/social/login/facebook/');               
                var fb_login_link = $('a.fb-login', login_modal);
                fb_login_link.attr('href', facebook_action);

                login_form.data('old-action', login_form.attr('action'));
                login_form.attr('action', new_action);
                login_modal.removeData('tempAction');                
            }
        });
        login_modal.on('hide', function (event) {
            var old_action = login_form.data('old-action')
            if( old_action ) {
                var facebook_action = old_action.replace('/accounts/social/login/facebook/', '/accounts/login/');               
                var fb_login_link = $('a.fb-login', login_modal);
                fb_login_link.attr('href', facebook_action);

                login_form.attr('action', old_action);
                login_form.removeData('old-action');
            }
        });
    }

    var register_modal = $('#register-modal');
    if( register_modal.length ) {
        var register_form = $('.register-form', register_modal);
        register_modal.on('show', function (event) {
            var new_action = register_modal.data('tempAction');
            if( new_action ) {
                var facebook_action = new_action.replace(/\/(accounts\/login|register)\//, '/accounts/social/login/facebook/');               
                var fb_login_link = $('a.fb-register', register_modal);
                fb_login_link.attr('href', facebook_action);

                register_form.data('old-action', register_form.attr('action'));
                register_form.attr('action', new_action);
                register_modal.removeData('tempAction');                
            }
        });

        register_modal.on('hide', function (event) {
            var old_action = register_form.data('old-action')
            if( old_action ) {
                var facebook_action = old_action.replace('/accounts/social/login/facebook/', '/accounts/login/');               
                var fb_login_link = $('a.fb-register', register_modal);
                fb_login_link.attr('href', facebook_action);

                register_form.attr('action', old_action);
                register_form.removeData('old-action');
            }
        });
    }
};

Ecomarket.Widgets.ModalLogin.prototype.show_register = function (event) {
    $("#login").modal('hide');
    $("#register-modal").modal('show');
}

Ecomarket.Widgets.ModalLogin.prototype.toggle = function (event) {
    var link = $(event.target);

    event.preventDefault();

    // dont do anything on clicking active link 
    if (link.hasClass('active')){
      return false;
    }

    var login_modal = $('#login');
    var register_modal = $('#register-modal');

    if( $('.login-form', register_modal).data('old-action') ) {
        var new_register_action = $('.login-form', login_modal).data('old-action').replace('/accounts/login/', '/register/');
        register_modal.data('tempAction', old_login_action);
    }
    else if( $('.register-form', register_modal).data('old-action') ) {
        var new_login_action = $('.register-form', register_modal).attr('action').replace('/register/', '/accounts/login/');
        login_modal.data('tempAction', new_login_action);   
    }
    
    login_modal.modal('toggle');
    register_modal.modal('toggle');
};

Ecomarket.Widgets.Selects = function (selector, select_params) {
    selector = selector || $('.select');
    selector.each(function (index, item) {
        var num;
        item = $(item);
        num = 8;
        if (item.data('search') === true) {
            num = 1;
        } else if (item.data('search') === 'hide') {
            num = 99;
        }
        select_params = (typeof (select_params) === 'function') ? select_params(this) : {
            minimumResultsForSearch: num
        };
        $(item).select2(select_params);
    });
};

/* links in new window open */
Ecomarket.Widgets.BlankLinks = function () {
  $(document).on('click.blanklinks', 'a[rel=external]', function(event){
    event.preventDefault();
    window.open(this.href);
  });
};

// M2M Select
Ecomarket.Widgets.SelectM2M = function (selector) {
    var m2ms;
    selector = selector || $(document);
    m2ms = selector.find('.m2m');
    m2ms.hide();
    //console.log(this);
    $('.tagger-select', selector).change(this.select_m2m.bind(this));

    selector.each(function (index, item) {
        var select, hidden_select, value, i;
        hidden_select = $(this);
        value = hidden_select.val();
        if ((value !== null) && (value.length > 0)) {
            select = hidden_select.next();
            for (i = 0; i < value.length; i += 1) {
                select.val(value[i]);
                select.change();
            }
        }
    });
};

Ecomarket.Widgets.SelectM2M.prototype.select_m2m = function (event) {
    event.preventDefault();
    var selected, hidden_select, val, title, chosen_option, split, tags;
    selected = $(event.target);

    // return if no change
    if (selected.val() === "") {
        return;
    }

    if (selected.val().indexOf('__') !== -1) {
        split = selected.val().split('__');
        val = selected.val();
        title = split[0];
    } else {
        val = selected.val();
        title = selected.children('option:selected').text();
    }

    // get tags list in context of select parent
    tags = $('.tags-list', selected.parent());
    tags.append('<span class="tag"><em data-value="' + val + '">'
                + title
                + '</em><a href="#" class="tag-remove">'
                + '<i class="icon icon-remove-sign m2m-icon"></i></a></span>');

    hidden_select = selected.parents('.controls').find('.m2m');

    // select this item in the hidden multiselect
    chosen_option = $('option[value="' + val + '"]', hidden_select);
    if (!chosen_option.length) {
        hidden_select.append('<option value="' + val + '" selected="selected">'+title+'</option>');
        chosen_option = $('option[value="' + val + '"]', hidden_select);
    }

    chosen_option.attr('selected', 'selected');

    // unselect
    $("option:selected", selected).remove();
};


// Nice loading buttons

Ecomarket.Widgets.LoadButtons = function () {
    if ($('.btn-load').length === 0) {
        return;
    }
    $('.btn-load').on('click', this.toggleLoading.bind(this));
    // preload loaading icon
    var imgs = [];
    imgs[0] = new Image();
    imgs[0].src = "/static/images/loading/green.gif";

    imgs[1] = new Image();
    imgs[1].src = "/static/images/loading/light.gif";

};

Ecomarket.Widgets.LoadButtons.prototype.toggleLoading = function (event) {
    // temporary prevent default
    var btn = $(event.target);
    if (btn.hasClass('btn-loading')) {
        return;
    }
    btn.html('<span class="inner">' + btn.html() + '</span><em></em>');
    btn.addClass('btn-loading');
    $('body').addClass('loading');

};

// Causes icons clickable
Ecomarket.Widgets.Causes = function () {
    if ($(".eco-icons > a").length === 0) {
        return;
    }
    $('.eco-icons > a')
        .on('click', this.toggle.bind(this));
};

Ecomarket.Widgets.Causes.prototype.toggle = function (event) {
    var t, box_id;
    event.preventDefault();
    t = $(event.target);
    if (t.hasClass("icon")) {
        t = t.parent();
    }

    box_id = t.attr('href');

    if (t.hasClass("active")) {
        t.removeClass('active');
        $(box_id).slideUp(function () {
            $(this).removeClass('expanded');
        });
        return;
    }

    // first reset previous state
    $(".eco-icons a.active").removeClass('active');

    // then show selected
    t.addClass('active');

    // expand via slide
    if ($('.eco-info.expanded').length > 0) {
        $('.eco-info.expanded').slideUp('fast', function () {
            $('.eco-info.expanded').removeClass('expanded');
            $(box_id).addClass('expanded').slideDown();
        });
    } else {
        $(box_id).addClass('expanded').slideDown();
    }
};

// Cart incrementation, decrementation buttons
Ecomarket.Widgets.Cart = function () {
    // if ($(".item-quantity").length == 0) return;
    // $('.item-quantity .btn-minus').on('click', this.decrement.bind(this));
    // $('.item-quantity .btn-plus').on('click', this.increment.bind(this));
};

Ecomarket.Widgets.Cart.prototype.decrement = function (event) {
    var i, v;
    event.preventDefault();
    i = $(event.target).next();
    v = i.val();
    if (v > 1) {
        $(i).val(v - 1);
    }
};

Ecomarket.Widgets.Cart.prototype.increment = function (event) {
    var i, v;
    event.preventDefault();
    i = $(event.target).prev();
    v = i.val();
    $(i).val(v + 1);
};
// Category dropdown

Ecomarket.Widgets.CategoryDropdown = function(selector) {
    this.selector = selector;
    if ($(selector).length !== 0) {
        this.initialize();
    }
};

Ecomarket.Widgets.CategoryDropdown.prototype.initialized = false;

Ecomarket.Widgets.CategoryDropdown.prototype.initialize = function () {
    $(this.selector).each(function() {
        var $select, value, $dro, $ul, text, i;
        $select = $(this);

        // Replace with selector
        $select.hide().next().removeClass('hidden')
            .find(".em-dropdown-current-choice .em-dropdown-value").text(
                $select.data("placeholder"));

        // loading default value
        value = $select.val();
        if (value !== "") {
            $dro = $select.next();
            $ul = $dro.find(".em-dropdown-list");
            text = $ul.find('.em-dropdown-choice[data-value="' + value + '"]').text().trim();
            if (text !== "") {
                $dro.find('.em-dropdown-value').html(text);
            }
        }

        // also add class if select has it
        if ($select.hasClass('category-picker')) {
            if ($dro) {
                $dro.addClass('category-picker');
            }
        }

        // set title attribute
        $('.category-picker .em-dropdown-choice').each(function(index,item){
          i = $(item);
          i.attr('title', i.text());
        });
    });

    if (this.initialized) {
        return;
    }
    $(document)
        .on('click.category-dropdown',
            '.em-dropdown-current-choice',
            this.toggleDropdown.bind(this));
    $(document)
        .on('click.category-dropdown',
            '.em-dropdown-list-toggle',
            this.toggleList.bind(this));
    $(document)
        .on('click.category-dropdown',
            '.em-dropdown-choice',
            this.choice.bind(this));

    // collapse when not clicked on dropdown
    $('html').on('click.category-dropdown touchstart.category-dropdown', function (event) {
        var x;
        if ($(event.target).parents('.em-dropdown').length <= 0) {
            x = $('.em-dropdown.em-dropdown-expanded');
            x.toggleClass('em-dropdown-collapsed').toggleClass("em-dropdown-expanded");
        }
    });

    this.initialized = true;
};

Ecomarket.Widgets.CategoryDropdown.prototype.toggleDropdown = function (event) {
    var dropdown,all_dropdowns;
    event.preventDefault();
    
    // trigger click on html to hide other dropdowns before show
    $('html').trigger('click.category-dropdown');
    
    dropdown = $(event.target).parents('.em-dropdown');
    dropdown
        .toggleClass('em-dropdown-collapsed')
        .toggleClass("em-dropdown-expanded");
};

Ecomarket.Widgets.CategoryDropdown.prototype.toggleList = function (event) {
    var dropdown, item, item_parent_ul, next_ul;
    event.preventDefault();
    dropdown = $(event.target).parents('.em-dropdown');
    item = $(event.target);
    item_parent_ul = item.parent().parent();
    next_ul = item.next();

    if (item.hasClass('active')) {
        next_ul.show().slideUp('fast');
    } else {
        // collapse other opened dropdowns
        if (item_parent_ul.hasClass("em-dropdown-list")) {// on primary level
            $(".em-dropdown-list-toggle.active").toggleClass('active');
            $(".em-dropdown-nested-list.em-dropdown-list-expanded")
                .toggleClass('em-dropdown-list-collapsed')
                .toggleClass("em-dropdown-list-expanded")
                .slideUp('fast');
        } else {// on secondary level
            $('> li > .em-dropdown-list-toggle.active', item_parent_ul)
                .toggleClass('active');
            $("> li > .em-dropdown-nested-list.em-dropdown-list-expanded", item_parent_ul)
                .toggleClass('em-dropdown-list-collapsed')
                .toggleClass("em-dropdown-list-expanded")
                .slideUp('fast');
        }
        next_ul.hide().slideDown('fast');
    }
    next_ul
        .toggleClass("em-dropdown-list-expanded")
        .toggleClass('em-dropdown-list-collapsed');
    item.toggleClass('active');
};

Ecomarket.Widgets.CategoryDropdown.prototype.choice = function (event) {
    var dropdown, item, value, value_text;
    event.preventDefault();
    dropdown = $(event.target).parents('.em-dropdown');
    item = $(event.target);

    // toggle dropdown
    dropdown
        .toggleClass('em-dropdown-collapsed')
        .toggleClass("em-dropdown-expanded");

    // clean all expanded classes
    dropdown.find('.active')
        .removeClass('active');
    dropdown.find('.em-dropdown-list-expanded')
        .hide()
        .removeClass('em-dropdown-list-expanded');

    // apply selected option

    value = item.data('value');
    value_text = item.html();

    $('.em-dropdown-value', dropdown).html(value_text);
    dropdown.prev().val(value).change();
};


// Color picker
Ecomarket.Widgets.ColorPicker = function () {
    if (".color-picker".length === 0) {
        return;
    }
    this.initialize();
};

Ecomarket.Widgets.ColorPicker.prototype.initialize = function () {
    $('.color-picker')
        .hide()
        .next()
        .removeClass('hidden');
    $(document)
        .on('click.colorpicker', '.em-colorpicker-current-choice',
            this.toggleDropdown.bind(this));
    $(document)
        .on('click.colorpicker', '.em-colorpicker-list a',
            this.choice.bind(this));

    // collapse when not clicked on colorpicker dropdown
    $('html').on('click.colorpicker touchstart.colorpicker', function (event) {
        var x;
        if ($(event.target).parents('.em-colorpicker').length <= 0) {
            x = $('.em-colorpicker.em-colorpicker-expanded');
            x.toggleClass('em-colorpicker-collapsed').toggleClass("em-colorpicker-expanded");
        }
    });

    $('.em-colorpicker-list a').each(function (index, item) {
        $(item).css('background-color', $(item).data('value'));
        $(item).attr('title', $(item).data('value'));
    });
};

Ecomarket.Widgets.ColorPicker.prototype.toggleDropdown = function (event) {
    var dropdown;
    event.preventDefault();
    dropdown = $(event.target).parents('.em-colorpicker');
    dropdown
        .toggleClass('em-colorpicker-collapsed')
        .toggleClass("em-colorpicker-expanded");
};

Ecomarket.Widgets.ColorPicker.prototype.choice = function (event) {
    var item, colorpicker, value, value_text;
    event.preventDefault();
    colorpicker = $(event.target).parents('.em-colorpicker');
    item = $(event.target);

    // toggle dropdown
    colorpicker
        .toggleClass('em-colorpicker-collapsed')
        .toggleClass("em-colorpicker-expanded");

    // clean all expanded classes
    colorpicker.find('.active').removeClass('active');

    // apply selected option

    value = item.data('value');
    value_text = item.html();

    $('.em-colorpicker-value', colorpicker).html(value_text);
    colorpicker.prev().val(value).change();
};

// Datepicker
Ecomarket.Widgets.DatePicker = function () {
    if ($('.date-picker').length > 0) {

        $('.date-picker').DatePicker({
            date : new Date(),
            calendars : 1,
            starts : 1,
            onChange : function (formated, dates, el) {
                $(el).val(formated);
                $(el).DatePickerHide();
            }
        });
    }

    if ($('.daterange-picker').length > 0) {

        $('.daterange-picker').DatePicker({
            date : [Date.parse("last month"), Date.today()],
            calendars : 2,
            mode : 'range',
            starts : 1,
            onShow : function (datepicker) {
                $(this).DatepickerUpdateDate();
            },
            onChange : function (formatted, dates, el) {
                $('.range-start', this).val(formatted[0]);
                if (formatted[0] !== formatted[1]) {
                    $('.range-end', this).val(formatted[1]);
                }
            },
            onApply : function (formatted, dates, el) {
                $(el).val(formatted.join(" / "));
                $(el).DatePickerHide();
            }
        });
    }
};

Ecomarket.Widgets.DateDropdown = function () {
    if ($('.date-dropdown').length === 0) {
        return;
    }

    $(document)
        .on("click.datedropdown touchstart.datedropdown", '.date-dropdown .dropdown-menu a',
            this.toggle.bind(this));

    $('.date-dropdown input.date-dropdown-value').DatePicker({
        date : [Date.parse("last month"), Date.today()],
        calendars : 2,
        mode : 'range',
        starts : 1,
        onShow : function (datepicker) {
            $(this).DatepickerUpdateDate();
            $(this).DatepickerFixPosition();
        },
        onChange : function (formatted, dates, el) {
            $('.range-start', this).val(formatted[0]);
            if (formatted[0] !== formatted[1]) {
                $('.range-end', this).val(formatted[1]);
            }
        },
        onApply : function (formatted, dates, el) {
            var dropdown;
            dropdown = $(el).parents('.date-dropdown');
            $(el).val(formatted.join(" / "));
            $(el).DatePickerHide();

            dropdown.find(".date-label").html("Custom range");

            // just for demo, remove for production
            $("#sample").val(formatted.join(" / "));
        }
    });
};

Ecomarket.Widgets.DateDropdown.prototype.toggle = function (event) {
    var el, dropdown, range;
    el = $(event.target);
    dropdown = el.parents('.date-dropdown');
    if (el.hasClass('custom')) {
        dropdown.find('.date-dropdown-value').DatePickerShow();
    } else {
        range = Date
            .parse(el.html()).toString("yyyy-M-dd")
            + " / "
            + Date.today().toString("yyyy-M-dd");
        dropdown.find(".date-dropdown-value").val(range);
        dropdown.find(".date-label").html(el.html());
        // just for demo, remove for production
        $("#sample").val(range);
    }
    dropdown.removeClass('open');
    event.preventDefault();
};

Ecomarket.Widgets.NumberInput = function () {
    // replace non numeric characters with ''
    $('input.input-number').live('keyup', function (evt) {
        $(this).val(
            $(this).val().replace(/[^\d]+/, '')
        );
    });

    // dont allow other inputs
    $('input.input-number').live('keydown', function (evt) {
        return (evt.ctrlKey || evt.altKey
                || (47 < evt.keyCode && evt.keyCode < 58 && evt.shiftKey === false)
                || (95 < evt.keyCode && evt.keyCode < 106)
                || (evt.keyCode === 8) || (evt.keyCode === 9)
                || (evt.keyCode > 34 && evt.keyCode < 40)
                || (evt.keyCode === 46));
    });

    // no pasting either
    $('input.input-number').live('paste', function (evt) {
        return (evt.ctrlKey || evt.altKey
                || (47 < evt.keyCode && evt.keyCode < 58 && evt.shiftKey === false)
                || (95 < evt.keyCode && evt.keyCode < 106)
                || (evt.keyCode === 8) || (evt.keyCode === 9)
                || (evt.keyCode > 34 && evt.keyCode < 40)
                || (evt.keyCode === 46));
    });
};

Ecomarket.Widgets.CurrencyInput = function () {
    // replace non numeric characters with ''
    $('input.input-currency').live(
        'keyup',
        function (evt) {
            var regex, num_str, dots, parts, dot;
            regex = /^\d+(\.{0,1}\d{0,2})$/;
            if (!regex.test(num_str)) {
                num_str = $(this).val().replace(/[^.0-9]/g, '');
                dots = num_str.match(/\./g);
                if (dots && dots.length > 1) {
                    num_str = num_str.split('.').slice(0, 2).join('.');
                }
                dot = num_str.indexOf('.');
                if (num_str.split('.').pop().length > 2) {
                    parts = num_str.split('.');
                    if (parts.length > 1) {
                        num_str = [parts[0], parts[1].slice(0, 2)].join('.');
                    }
                }
                $(this).val(num_str);
            }
        }
    );

    // dont allow other inputs
    $('input.input-currency').live('keydown', function (evt) {
        return (evt.ctrlKey || evt.altKey
                || (47 < evt.keyCode && evt.keyCode < 58 && evt.shiftKey === false)
                || (95 < evt.keyCode && evt.keyCode < 106)
                || (evt.keyCode === 8) || (evt.keyCode === 9)
                || (evt.keyCode > 34 && evt.keyCode < 40)
                || (evt.keyCode === 46)
                || (evt.keyCode === 190));
    });

    // no pasting either
    $('input.input-currency').live('paste', function (evt) {
        return (evt.ctrlKey || evt.altKey
                || (47 < evt.keyCode && evt.keyCode < 58 && evt.shiftKey === false)
                || (95 < evt.keyCode && evt.keyCode < 106)
                || (evt.keyCode === 8) || (evt.keyCode === 9)
                || (evt.keyCode > 34 && evt.keyCode < 40)
                || (evt.keyCode === 46)
                || (evt.keyCode === 190));
    });
};

Ecomarket.Widgets.Reviews = function () {
    if ($(".reveal-review").length === 0) {
        return;
    }
    $(document)
        .on('click', '.reveal-review',
            this.reveal.bind(this));
};

Ecomarket.Widgets.Reviews.prototype.reveal = function (event) {
    event.preventDefault();
    $(event.target).hide();
    $(event.target).prev()
        .removeClass('hidden')
        .hide()
        .slideDown();
};

// add class to provide hover effect
Ecomarket.Widgets.Hovers = function () {
    $('img').each(function (index, item) {
        var img, parentLink;
        img = $(item);
        parentLink = img.parent();
        if (parentLink.is("a") && !parentLink.hasClass('thmb')) {
            parentLink.addClass("thmb");
        }
    });
};

// notifications handling
Ecomarket.Widgets.Notifications = function () {
    $(document)
        .on('click', '.notice-dismiss',
            function (event) {
                event.preventDefault();
                $(event.target).parents(".page-notice")
                    .first()
                    .fadeOut();
            });

    $(document)
        .on('click', '.alert-dismiss',
            function (event) {
                event.preventDefault();
                $(event.target).parents(".alert")
                    .first()
                    .fadeOut();
            });
};

Ecomarket.Product.Scrollables = function () {
    if ($(".products-scrollable, .blogs-scrollable").length > 0) {
        this.initProducts();
    }

    if ($(".photos-scrollable").length > 0) {
        this.initPhotos();
    }
};

Ecomarket.Product.Scrollables.prototype.initProducts = function () {
    $(".products-scrollable, .blogs-scrollable").scrollable({});
    $('.scrollable-container a.scrollable-browse').on('click', function (event) {
        event.preventDefault();
    });
};

Ecomarket.Product.Scrollables.prototype.initPhotos = function () {
    $(".photos-scrollable").scrollable({
        vertical : true
    });
};

// inifinite scroll on search page
Ecomarket.Product.InfiniteScroll = function () {
    if ($("#infinite-scroll").length !== 0) {
        this.initProductScroll();
    }

    if ($("#activity-scroll").length !== 0) {
        this.initActivityScroll();
    }

};

Ecomarket.Product.InfiniteScroll.prototype.initProductScroll = function () {
    var page_no = parseInt($('#infinite-scroll').attr('data-page'), 10),
        max_page_no = parseInt($('#infinite-scroll').attr('data-max-page'), 10);
    $('#infinite-scroll').infinitescroll({
        loading : {
            finished : function (event) {
              $("#infscr-loading").fadeOut();
              if ( "Markerly" in window ) {
                window.Markerly.selection.image_listener();
              }
            },
            finishedMsg : "No more results. You've reached the end of the line my friend.",
            img : "/static/images/loading.gif",
            speed : "fast",
            msgText : "Loading new products..."
        },
        state: {
            currPage: page_no
        },
        maxPage: max_page_no,
        bufferPx: 150,
        navSelector : "#infinite-scroll .pagination",
        nextSelector : ".pagination ul li.active + li a",
        itemSelector : "#infinite-scroll .pagination-results"
    }, function(arrayOfNewElems) {
		// optional callback when new content is successfully loaded in.
		// keyword `this` will refer to the new DOM content that was just added.
		// as of 1.5, `this` matches the element you called the plugin on (e.g. #content)
		// all the new elements that were found are passed in as an array
		currency.changeAll($(arrayOfNewElems));
        $(arrayOfNewElems).find('.discover-list .details .product').each(function() {
            txt = $(this).text().truncatechars(50);
            $(this).html(txt);
        });
	});

};

Ecomarket.Product.InfiniteScroll.prototype.initActivityScroll = function () {
    $('#activity-scroll').infinitescroll({
        loading : {
            finished : function (event) {
                $("#infscr-loading").fadeOut();
            },
            finishedMsg : "No more results. You've reached the end of the line my friend.",
            img : "/static/images/loading.gif",
            speed : "fast",
            msgText : "Loading new items..."
        },
        bufferPx: 150,
        navSelector : "#activity-scroll .pagination",
        nextSelector : ".pagination ul li:first a",
        itemSelector : "#activity-scroll .pagination-results"
    });

};


// filter follow
Ecomarket.Product.FilterFollow = function () {
    if ($("#filter-follow").length !== 0) {
        this.initFilter();
    }
};

Ecomarket.Product.FilterFollow.prototype.initFilter = function () {
    if (typeof($.waypoints) === "undefined"){
      return false;
    }
    $.waypoints.settings.scrollThrottle = 100;
    $('#filter-follow').waypoint({
        offset : -100,
        continuous: false,
        handler: this.onWaypointReach
    });

    $(document).on('click', '.btn-to-top', function (event) {
        event.preventDefault();
        var targetOffset = $('#filter-follow').offset().top;
        $('html,body').animate({
            scrollTop : targetOffset
        }, 150, 'swing');
    });
};

Ecomarket.Product.FilterFollow.prototype.onWaypointReach = function (direction) {
    if (direction === "down") {
        $(this).find('.sticky-filter')
            .addClass('sticky')
            .hide()
            .fadeIn();
    } else {
        $(this).find('.sticky-filter')
            .removeClass('sticky')
            .hide()
            .fadeIn();
    }
};

// Switchable images on product page

Ecomarket.Product.PhotoGallery = function(){
  if($('.photo-slider').length === 0) { return; }

  $('.photos-nav a').on('click', this.switchPhoto);
};

Ecomarket.Product.PhotoGallery.prototype.switchPhoto = function (event) {
  event.preventDefault();
  //$('.primary-photo a').attr('href', $(this).data('big'))
  $('.primary-photo img').attr('src', $(this).data('preview'));

};

// Love button
Ecomarket.Widgets.LoveButton = function () {

    // dont initialize when there are no love buttons on page
    if ($('.btn-love, .love-this').length !== 0) {
        $(document).on("click.lovebutton touchstart.lovebutton", '.love-this', this.love.bind(this));
        $(document).on("click.lovebutton touchstart.lovebutton", '.btn-love', this.love.bind(this));
        $(document).on("click.lovebutton touchstart.lovebutton", '.love-current-list', this.loveList.bind(this));
        $(document).on("click.lovebutton touchstart.lovebutton", '.love-change-list', this.loveList.bind(this));
        $(document).on("click.lovebutton touchstart.lovebutton", '.love-manage-list', this.manageLoveList.bind(this));

        $(document).on('click.lovebutton touchstart.lovebutton', 'html', this.clearMenu.bind(this));

        $(document).on('change.lovebutton', '.lovelist-choice', this.revealForm.bind(this));
    }
};


Ecomarket.Widgets.LoveButton.prototype.animateButton = function(btn) {
        btn.addClass('animating');
        btn.fadeOut(function () {
            $(this).addClass('btn-loved').addClass('has-lovelist').fadeIn(function(){
              $(this).removeClass('animating');
              $(this).removeClass('love-dropdown-toggle');
            }).css("display","inline-block");
        });
};


Ecomarket.Widgets.LoveButton.prototype.submitModal = function(url, data) {
    var existing_modal = $("#loveListModal");
    if (data.success) {
        if (data.created) {
            mixpanel.track("Saved product to love list",
                           data.product_mixpanel_data);
            mixpanel.people.increment("Loved Products", 1);
        }
        if ( "product_slug" in data ) {
            existing_modal.modal("hide").remove();
            this.animateButton($("#love-button-" + data.product_slug));
        }
    } else {
        existing_modal.html($(data.html).html())
                      .find("form").ajaxForm({
                          url: url,
                          type: "POST",
                          beforeSubmit: function(arr, form, options) {
                              form.find("button").button("loading");
                          },
                          success: function(data) {
                              this.submitModal.bind(this)(url, data);
                          }.bind(this)
                      });
        Ecomarket.category_dropdown.initialize
                 .bind(Ecomarket.category_dropdown)();
    }
};

Ecomarket.Widgets.LoveButton.prototype.triggerModal = function(slug) {
    // trigger modal
    var url, dialog = $('#loveListModal');
    if (dialog.length) {
        // This means the product name in the URL is no longer the definitive
        // product name of the product being saved
        dialog.find("form").find("input[name=product_slug]").val(slug);
        dialog.modal({});
    } else {
        dialog = $("#loading-modal").clone().attr("id", "loveListModal")
            .addClass("modal-loading")
            .appendTo("body").modal({});
        url = "/love/ajax/love_list_select/" + slug + "/";
        $.ajax(url, {
            success: function(data) {
                dialog.html($(data.html).html())
                      .removeClass("modal-loading")
                      .addClass("love-modal")                      
                      .find("form").ajaxForm({
                          url: url,
                          type: "POST",
                          beforeSubmit: function(arr, form, options) {
                              form.find("button").button("loading");
                          },
                          success: function(data) {
                              this.submitModal.bind(this)(url, data);
                          }.bind(this),
                          http_error: {
                              forbidden: function(data) {
                                  dialog.removeAttr("id")
                                        .html($("#errorModal").html());
                                  if (data.reason) {
                                      new Ecomarket.Widgets.ErrorDialog(dialog)
                                          .show(data.reason);
                                  }
                              }
                           }
                      });
                dialog.find('.lovelist-choice').select2({minimumResultsForSearch: 99});
                Ecomarket.category_dropdown.initialize
                         .bind(Ecomarket.category_dropdown)();
                Ecomarket.eco_checkbox.setup(
                    $("#loveListModal .eco-checkbox"));
            }.bind(this)
        });
    }
};


Ecomarket.Widgets.LoveButton.prototype.love = function (event) {
    function _text_link(href, klass, text) {
        return $("<a />").attr("href", href)
            .addClass(klass).text(text)
            .appendTo("<li />").parent();
    }
    var btn, slug, remove_url;
    event.preventDefault();
    event.stopPropagation();

    btn = $(event.target);

    if (btn.hasClass('icon')) {
        // traverse up if icon clicked
        btn = btn.parent();
    }

    // return if is currently animating
    if (btn.hasClass('animating')) {
        return;
    }

    slug = btn.data("slug");
    if (!slug) {
        // Better to bail out early than to look like it's worked when
        // it hasn't
        window.console.error("Love button not linked to product!");
        return;
    }

    // remove button
    if (btn.hasClass("btn-love-remove")) {
        remove_url = "/love/ajax/remove/" + slug + "/"
                     + btn.data("list_identifier") + "/";
        $.post(remove_url, {}, function(data) {
            $("span.products_count").text(data.products_count);
            btn.parents("li").hide("fast", function() {
                $(this).remove();
            });
        });
        return;
    }

    // some logic to show / hide modals or just love

    if (btn.hasClass("love-dropdown-toggle")) {
        this.clearMenu();
        return;
    }

    this.clearMenu();

    $.ajax("/love/ajax/current_love_list/" + slug + "/", {
        success: function(data) {
            var current_love_list, dd, offset;
            mixpanel.track("Clicked love on product",
                           data.product_mixpanel_data);
            switch (data.action) {
                case "login":
                    $("#register-modal").modal('toggle');
                    break;

                case "show_menu":
                    current_love_list = data.list_name;
                    btn.addClass('love-dropdown-toggle');
                    dd = $("#love-dropdown");
                    if (dd.length) {
                        dd.find(".love-current-list").text('Add to "' + current_love_list + '"');
                    } else {
                        // generate dropdown on the fly
                        dd = _text_link("#", "love-current-list", 'Add to "' + current_love_list + '"')
                            .add(_text_link("#", "love-change-list", "Add to a different or new love list"))
                            .add(_text_link("/love/", "love-manage-list", "Manage my love lists"))
                            .appendTo("<ul />").parent()
                                .attr("id", "love-dropdown")
                                .addClass("dropdown-menu love-dropdown")
                                .attr("role", "menu").attr("aria-labelledby", "dLabel")
                                .appendTo("body");
                    }
                    offset = btn.offset();
                    dd.data("item_slug", slug);
                    // position to right if its overlapping the screen
                    if(offset.left + $("#love-dropdown").width() < $('body').width()) {                    
                      dd.css({
                        left: offset.left - 3 + "px",
                        top: offset.top + 28 + "px"
                      }).removeClass('right-side');
                    } else{
                       dd.css({
                          left: offset.left - $("#love-dropdown").width() + 30 + "px",
                          top: offset.top + 28 + "px"
                        }).addClass('right-side');
                    }
                    dd.show();
                    break;

                case "create_new":
                    this.triggerModal(slug);
                    break;

                default:
                    window.console.warn("Unknown action '" + data.action + "'");
            }
        }.bind(this)
    });

};

Ecomarket.Widgets.LoveButton.prototype.loveList = function (event) {
    var btn, link, slug;
    event.preventDefault();
    event.stopPropagation();

    // find love button

    link = $(event.target);
    slug = link.parents("ul").data("item_slug");
    btn = $("#love-button-" + slug);

    if (link.hasClass('love-current-list')) {

        this.clearMenu();

        $.ajax("/love/ajax/add/" + slug + "/", {
            type: "POST",
            success: function(data) {
                if (data.created) {
                    mixpanel.track("Saved product to love list",
                                   data.product_mixpanel_data);
                    mixpanel.people.increment("Loved Products", 1);
                }
            },
            http_error: {
                forbidden: function(data) {
                    if (data.reason) {
                        Ecomarket.error_dialog.show(data.reason);
                    }
                }
            }
        });

        this.animateButton(btn);
    } else {
        this.triggerModal(slug);
        this.clearMenu();
    }
};

Ecomarket.Widgets.LoveButton.prototype.manageLoveList = function (event) {
};

Ecomarket.Widgets.LoveButton.prototype.revealForm = function (event) {
    var item;
    item = $(event.target);
    if (item.val() === "new") {
        $('.reveal-list-form').slideDown(function () {
            $(this).addClass('expanded');
            $(this).css('overflow', 'visible');
        });
    } else {
        $('.reveal-list-form.expanded')
            .removeClass('expanded')
            .slideUp();
    }
};

Ecomarket.Widgets.LoveButton.prototype.clearMenu = function (event) {
    $('#love-dropdown').hide();
    $('.love-dropdown-toggle').removeClass('love-dropdown-toggle');
};

Ecomarket.Widgets.LoginToReply = function () {
    $('#login-to-reply').click(function (e) {
        e.preventDefault();
        e.stopImmediatePropagation();
        $('#register-modal').modal();
    });
};

Ecomarket.Widgets.AskQuestionButton = function () {
    $('#ask-question-link.needs-login').click( function (e) {
        e.preventDefault();
        e.stopImmediatePropagation();
        var link = $(e.target);
        $('#register-modal')
            .data('tempAction', link.attr('data-next'))
            .modal('toggle');
    });
};

Ecomarket.Widgets.RequestDeliveryCountryButton = function () {
    $('#request-delivery-country-link.needs-login').click( function (e) {
        e.preventDefault();
        e.stopImmediatePropagation();
        var link = $(e.target);
        console.log(link.attr('data-next'));
        $('#register-modal')
            .data('tempAction', link.attr('data-next'))
            .modal('toggle');
    });
};

// Follow button
Ecomarket.Widgets.FollowButton = function () {
    if ($('.btn-follow').length !== 0) {
        $('.btn-follow-login').click(function (e) {
            e.preventDefault();
            e.stopImmediatePropagation();

            var link = $(e.target);
            $('#register-modal')
                .data('tempAction', link.attr('href'))
                .modal('toggle');
            return false;
        });
        $(document).on("click.followbutton touchstart.followbutton", '.btn-follow', this.toggle.bind(this));
        $(document).on("mouseover.followbutton", '.btn-follow.btn-following', this.hoverIn.bind(this));
        $(document).on("mouseout.followbutton", '.btn-follow.btn-following', this.hoverOut.bind(this));
    }
};

Ecomarket.Widgets.FollowButton.prototype.toggle = function (event) {
    var btn, text, user_id, protocol, url;
    event.preventDefault();
    btn = $(event.target);

    if (!btn.hasClass('animating')) {
        user_id = btn.data('user_id');
        if(user_id === "" || typeof user_id === "undefined"){
            protocol = "http://";
            window.location = protocol + window.location.host + btn.attr('href');
        }
        if (!btn.hasClass('btn-following')) {
            url = "/activities/follow/" + user_id + "/";
            $.post(url, {}, function(data) {
                if(data.status){
                    btn.addClass('animating').fadeOut(function () {
                        $(this).addClass('btn-following');
                        text = $(this).html();
                        $(this).html(text.replace("Follow", "Following"));
                        $(this).fadeIn(function () {
                            $(this).removeClass('animating');
                        });
                    });
                }
            });
        } else {
            url = "/activities/unfollow/" + user_id + "/";
            $.post(url, {}, function(data) {
                if(data.status === "OK"){
                    btn.addClass('animating').fadeOut(function () {
                        $(this).removeClass('btn-following').removeClass('btn-unfollow');
                        text = $(this).html();
                        $(this).html(text.replace("Following", "Follow").replace("Unfollow", "Follow"));
                        $(this).fadeIn(function () {
                            $(this).removeClass('animating');
                        });
                    });
                }
            });

        }
    }
};

Ecomarket.Widgets.FollowButton.prototype.hoverIn = function (event) {
    var btn, text;
    btn = $(event.target);
    text = $(btn).html();
    $(btn).html(text.replace("Following", "Unfollow"))
        .addClass('btn-unfollow');
};

Ecomarket.Widgets.FollowButton.prototype.hoverOut = function (event) {
    var btn, text;
    btn = $(event.target);
    text = $(btn).html();
    $(btn).html(text.replace("Unfollow", "Following"))
        .removeClass('btn-unfollow');
};

// Resolve button

Ecomarket.Widgets.ResolveButton = function () {
    if ($('.btn-resolve').length !== 0) {
        $(document).on("click.resolvebutton touchstart.resolvebutton", '.btn-resolve', this.toggle.bind(this));
        $(document).on("mouseover.resolvebutton", '.btn-resolve', this.hoverIn.bind(this));
        $(document).on("mouseout.resolvebutton", '.btn-resolve', this.hoverOut.bind(this));
    }
};

Ecomarket.Widgets.ResolveButton.prototype.toggle = function (event) {
    var btn, text;
    event.preventDefault();
    btn = $(event.target);

    if (!btn.hasClass('animating')) {
        if (btn.hasClass('btn-unresolved')) {
            // do resolve action
            btn.addClass('animating').fadeOut(function () {
                $(this).addClass('btn-resolved')
                    .removeClass('btn-unresolved');
                text = $(this).html();
                $(this).html("Resolved");
                $(this).fadeIn(function () {
                    $(this).removeClass('animating');
                });
            });
        } else {
            // do unresolve action
            btn.addClass('animating').fadeOut(function () {
                $(this).removeClass('btn-resolved')
                    .addClass('btn-unresolved');
                text = $(this).html();
                $(this).html("Unresolved");
                $(this).fadeIn(function () {
                    $(this).removeClass('animating');
                });
            });
        }
    }
};

Ecomarket.Widgets.ResolveButton.prototype.hoverIn = function (event) {
    var btn, text;
    btn = $(event.target);
    text = $(btn).html();
    if (text === "Unresolved") {
        $(btn).html("Resolve?");
    } else if (text === "Resolved") {
        $(btn).html("Unresolve?");
    }
};

Ecomarket.Widgets.ResolveButton.prototype.hoverOut = function (event) {
    var btn, text;
    btn = $(event.target);
    text = $(btn).html();
    if (text === "Resolve?") {
        $(btn).html("Unresolved");
    } else if (text === "Unresolve?") {
        $(btn).html("Resolved");
    }
};


Ecomarket.Widgets.CopyClipboard = function () {
    if ($("a.clipboard").length !== 0) {
        $("a.clipboard").click(function () {
            var clip = new ZeroClipboard.Client();
            clip.setHandCursor(true);
            clip.setText($(this).parent().find('input').val());
            return false;
        });
    }
};

// Nice iphone style on / off checkboxes

Ecomarket.Widgets.EcoCheckbox = function () {
    var $checkboxes = $('.eco-checkbox');
    if ($checkboxes.length !== 0) {
        this.setup($checkboxes);
    }
};

Ecomarket.Widgets.EcoCheckbox.prototype.setup = function ($checkboxes) {
    $checkboxes.iphoneStyle({
        checkedLabel: "",
        uncheckedLabel: "",
        resizeContainer: false,
        resizeHandle: false
    });
};


// initialize video playback
Ecomarket.Widgets.VideoPlayer = function () {

    if ($('video').length !== 0) {
        $('video').mediaelementplayer({
            // if the <video width> is not specified, this is the default
            defaultVideoWidth: 480,
            // if the <video height> is not specified, this is the default
            defaultVideoHeight: 270,
            // if set, overrides <video width>
            videoWidth: -1,
            // if set, overrides <video height>
            videoHeight: -1,
            // width of audio player
            audioWidth: 400,
            // height of audio player
            audioHeight: 30,
            // initial volume when the player starts
            startVolume: 0.8,
            // useful for <audio> player loops
            loop: false,
            // enables Flash and Silverlight to resize to content size
            enableAutosize: true,
            // the order of controls you want on the control bar (and other plugins below)
            features: ['playpause', 'progress', 'current',
                       'duration', 'tracks', 'volume', 'fullscreen'],
            // Hide controls when playing and mouse is not over the video
            alwaysShowControls: false,
            // force iPad's native controls
            iPadUseNativeControls: false,
            // force iPhone's native controls
            iPhoneUseNativeControls: false,
            // force Android's native controls
            AndroidUseNativeControls: false,
            // forces the hour marker (##:00:00)
            alwaysShowHours: false,
            // show framecount in timecode (##:00:00:00)
            showTimecodeFrameCount: false,
            // used when showTimecodeFrameCount is set to true
            framesPerSecond: 25,
            // turns keyboard support on and off for this instance
            enableKeyboard: true,
            // when this player starts, it will pause other players
            pauseOtherPlayers: true,
            // array of keyboard commands
            keyActions: []
        });
    }
};

Ecomarket.Widgets.Autocomplete = function (selector) {

    // example of autocomplete on tags
    selector.typeahead({
        source: function (query, process) {
            var attr_name, attr_toggle, attr_target, attr_params;
            attr_target = this.$element.attr('data-target');
            attr_name = this.$element.attr('data-type');
            attr_toggle = this.$element.attr('data-toggle');
            attr_params = this.$element.attr('data-params');
            $.get(attr_target, {
                attr: attr_name,
                params: attr_params,
                q: query
            }, function (data) {
                if( typeof data === "undefined" ) { return; }
                if (attr_toggle === 'suggest' && data.indexOf(query) === -1) {
                    data.splice(0, 0, "Add '"
                                + query
                                + "' as "
                                + attr_name);
                }
                process(data);
            });
        },
        updater: function (tag) {
            var el, tags, attr_name, hidden_select;
            attr_name = this.$element.attr('data-type');
            el = $(this.$element);
            tags = $('.tags-list', el.parent());

            if (tag !== "") {

                // clean tag a bit if its a new tag
                if (tag.match(/'\ as ' + attr_name$/) !== -1) {
                    // strip it
                    tag = tag.replace("Add '", "")
                        .replace("' as " + attr_name, "");
                }
                tags.append('<span class="tag"><em data-value="'+tag+'">'
                            + tag
                            + '</em><a href="#" class="tag-remove">'
                            + '<i class="icon icon-remove-sign m2m-icon"></i></a></span>');
                el.val('');

                // add to hidden select
                hidden_select = el.parents('.controls').find('.m2m');
                hidden_select.append('<option selected=selected value="'
                                     + tag + '" />');
            }
        },
        sorter: function(items) {
            return items;
        }
    });
};

Ecomarket.Widgets.Truncater = function(selector, limit) {
    $(selector).jTruncate({
        length: limit,
        moreText: "read more",
        lessText: "read less",
        moreAni: "fast",
        lessAni: "fast"
      });
};


Ecomarket.Widgets.ErrorDialog = function(selector) {
    this.selector = selector;
};

Ecomarket.Widgets.ErrorDialog.prototype.show = function(new_data) {
    var div = $(this.selector), data;
    if (!div.length) {
        window.console.error("Error dialog not found");
        return;
    }
    // Default data
    data = {
        title: "Error",
        description: "An error has occurred",
        dismiss: "OK"
    };
    if (typeof new_data === "string") {
        new_data = {description: new_data};
    }
    $.extend(data, new_data);
    div.find("h3.title").text(data.title);
    div.find("p.description").text(data.description);
    div.find("a.btn-dismiss").text(data.dismiss);
    div.modal({});
};

Ecomarket.Widgets.TouchEvents = function(){
  // do only if don't support hover
  if("Modernizr" in window && window.Modernizr.touch){
    $('body').on('touchend.tap', 'ul.discover-list li a.image', function(event){
        event.preventDefault();
        $(this).parent().toggleClass('touched');
    });
  }
};

function getCookie(name) {
    /* Taken from https://docs.djangoproject.com/en/dev/ref/contrib/csrf/ */
    var cookieValue = null, cookies, cookie, i;
    if (document.cookie && document.cookie !== '') {
        cookies = document.cookie.split(';');
        for (i = 0; i < cookies.length; i+=1) {
            cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


jQuery(document).ready(function ($) {
    Ecomarket.blank_links = new Ecomarket.Widgets.BlankLinks();
    Ecomarket.selects = new Ecomarket.Widgets.Selects();

    Ecomarket.load_buttons = new Ecomarket.Widgets.LoadButtons();
    
    Ecomarket.modal_login = new Ecomarket.Widgets.ModalLogin();


    Ecomarket.activities_button = new Ecomarket.Widgets.ActivitiesButton('a.modal-activities');

    Ecomarket.causes = new Ecomarket.Widgets.Causes();
    Ecomarket.cart = new Ecomarket.Widgets.Cart();

    Ecomarket.category_dropdown = new Ecomarket.Widgets.CategoryDropdown('.multiple-dropdown');
    Ecomarket.color_picker = new Ecomarket.Widgets.ColorPicker();
    Ecomarket.daterange_picker = new Ecomarket.Widgets.DatePicker();
    Ecomarket.date_dropdown = new Ecomarket.Widgets.DateDropdown();
    Ecomarket.number_input = new Ecomarket.Widgets.NumberInput();
    Ecomarket.currency_input = new Ecomarket.Widgets.CurrencyInput();

    Ecomarket.autocomplete = Ecomarket.Widgets.Autocomplete($('.tags-autocomplete'));

    Ecomarket.reviews = new Ecomarket.Widgets.Reviews();

    Ecomarket.scrollables = new Ecomarket.Product.Scrollables();

    Ecomarket.infinite_scroll = new Ecomarket.Product.InfiniteScroll();
    Ecomarket.filter_follow = new Ecomarket.Product.FilterFollow();
    Ecomarket.photo_gallery = new Ecomarket.Product.PhotoGallery();

    Ecomarket.hovers = new Ecomarket.Widgets.Hovers();
    Ecomarket.notifications = new Ecomarket.Widgets.Notifications();

    Ecomarket.copy_clipboards = new Ecomarket.Widgets.CopyClipboard();

    Ecomarket.love_button = new Ecomarket.Widgets.LoveButton();
    Ecomarket.follow_button = new Ecomarket.Widgets.FollowButton();
    Ecomarket.login_to_reply = new Ecomarket.Widgets.LoginToReply();
    Ecomarket.askquestion_button = new Ecomarket.Widgets.AskQuestionButton();
    Ecomarket.request_delivery_country_button = new Ecomarket.Widgets.RequestDeliveryCountryButton();
    Ecomarket.resolve_button = new Ecomarket.Widgets.ResolveButton();

    Ecomarket.eco_checkbox = new Ecomarket.Widgets.EcoCheckbox();

    Ecomarket.video_player = new Ecomarket.Widgets.VideoPlayer();

    Ecomarket.expander = Ecomarket.Widgets.Truncater($('p.truncate'), 450);

    Ecomarket.error_dialog = new Ecomarket.Widgets.ErrorDialog("#errorModal");

    Ecomarket.touch_events = new Ecomarket.Widgets.TouchEvents();

    /* Taken from https://docs.djangoproject.com/en/dev/ref/contrib/csrf/ */
    $.ajaxSetup({
        crossDomain: false, // obviates need for sameOrigin test
        beforeSend: function(xhr, settings) {
            if (!(/^(GET|HEAD|OPTIONS|TRACE)$/.test(settings.type))) {
                xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
            }
        }
    });

    $(document).ajaxError(function(event, jqXHR, ajaxSettings, thrownError){
        /* AJAX error handling, as an easier way to handle errors give the user
         * some feedback. As an example, consider:
         *
         * $.ajax({
         *     ...
         *     'http_error': {
         *         'forbidden': function(data) {
         *             // Do something nice with the JSON data here
         *         },
         *         'not found': function(data) {
         *             // Do something else with the JSON data here
         *         },
         *     }
         * });
         */
        var callback, data;
        thrownError = thrownError.toLowerCase();
        if (ajaxSettings.http_error && ajaxSettings.http_error[thrownError]) {
            callback = ajaxSettings.http_error[thrownError];
            try {
                data = $.parseJSON(jqXHR.responseText);
            } catch (err) {
                // Data is probably not JSON
                return;
            }
            return callback(data);
        }
    });
    
    
    $(document).on('show', '.modal', function(e){
      if ($(window).height() < 700)
        $(this).css('top', '20px');
      else
        $(this).css('top', '20%');
      // fix modal on mobile devices
    });

    $('input, textarea').placeholder();

    $('form').submit(function(event) {
     var origin = $("input[type=submit][clicked=true]").attr('name');

      var selector = '#' + origin;
      $(selector).removeAttr('disabled');
      $('.single-trigger').attr('disabled',true);
    });

    $("form input[type=submit]").click(function() {
      $("input[type=submit]", $(this).parents("form")).removeAttr("clicked");
      $(this).attr("clicked", "true");
    });
});
