// Messaging related JS

Ecomarket.Messaging.Constants = {
    INBOX: '/messages/inbox/'
}

Ecomarket.Messaging.ComposeModalSetupTypeahead = function(){
    var recipient_selector = '#id_recipient';
    $(recipient_selector).typeahead({
        source: function (query, process) {
            var ajax_url = $(recipient_selector).attr('data-source-url');
            return $.get(ajax_url, { query: query }, function (data) {
                return process(data.recipients);
            });
        },
        items: 12
    });
}

Ecomarket.Messaging.ComposeModal = function(){
    var selector = "a[data-toggle=modal].btn-new-messages.ajax"
    $(document).on("click", selector, function(event) {
        var $btn = $(selector);
        var url = $(this).attr('data-source');
        var target = $(this).attr('data-target');
        var recipient_selector = '#id_recipient';
        var initial_recipient = $(this).attr('data-username');
        $(target).load(url, function(){
            if (initial_recipient != undefined) {
                $(recipient_selector).val(initial_recipient);
            }
            new Ecomarket.Messaging.ComposeModalSetupTypeahead();
        });
    });
}

Ecomarket.Messaging.ReplyModal = function(){
    var selector = "a[data-toggle=modal].btn-reply-messages.ajax"
    $(document).on("click", selector, function(event) {
        var $btn = $(selector);
        var url = $(this).attr('data-source');
        var target = $(this).attr('data-target');
        $(target).load(url, function(){
            $(this).on("hidden", function() {
                $('#tab-content').load('/messages/list/');
            });
        });
    });
}

Ecomarket.Messaging.ComposeSubmitButton = function(){
    // Also deals with reply modal submit.
    var selector = ".ajax-submit"
    $(document).on("click", selector, function(event) {
        var $btn = $(this);
        var $form = $btn.parents("form");
        var url = $form.attr('action');
        var get = null;
        if ($btn.hasClass('resolve') == true) {
            get = '?resolve=1';
        } else {
            get = '';
        }
        $.post(url + get, $form.serialize(), function(data) {
            if ($(data).find('[class="errorlist"]').html() == null) {
                $('#new-message').modal('hide');
                document.location = Ecomarket.Messaging.Constants.INBOX;
            } else {
                $btn.parents('div.modal').html(data);
                new Ecomarket.Messaging.ComposeModalSetupTypeahead();
            }
        })
        event.preventDefault();
    });
}

Ecomarket.Messaging.DeleteSelected = function(){
    var selector = ".toolbar-active .btn-delete-messages.ajax"
    var new_messages_count_selector = '#user-new-messages'
    $(document).on("click", selector, function(event) {
        var $btn = $(selector);
        var url = $(this).attr('data-source');
        var target = $(this).attr('data-target');
        var checked = $('input[name=all]').serialize()
        var url_new_messages = $(new_messages_count_selector).attr('data-source');
        url += '?' + 'tab=inbox&' + checked;
        $.ajax({url: url,
                async: false,
                success: function(data) {
                    document.location = Ecomarket.Messaging.Constants.INBOX;
                }
        });
    });
}

Ecomarket.Messaging.MarkReadSelected = function(){
    var selector = ".toolbar-active .btn-mark-read-messages.ajax"
    var new_messages_count_selector = '#user-new-messages'
    $(document).on("click", selector, function(event) {
        var $btn = $(selector);
        var url = $(this).attr('data-source');
        var target = $(this).attr('data-target');
        var checked = $('input[name=all]').serialize()
        var url_new_messages = $(new_messages_count_selector).attr('data-source');
        url += '?' + 'tab=inbox&' + checked;
        $.ajax({url: url, 
                async: false, 
                success: function(data) {
                    document.location = Ecomarket.Messaging.Constants.INBOX;
                }
            });
        
    });
}

Ecomarket.Messaging.MarkUnReadSelected = function(){
    var selector = ".toolbar-active .btn-mark-unread-messages.ajax"
    var new_messages_count_selector = '#user-new-messages'
    $(document).on("click", selector, function(event) {
        var $btn = $(selector);
        var url = $(this).attr('data-source');
        var target = $(this).attr('data-target');
        var checked = $('input[name=all]').serialize()
        var url_new_messages = $(new_messages_count_selector).attr('data-source');
        url += '?' + 'tab=inbox&' + checked;
        $.ajax({url: url, 
                async: false, 
                success: function(data) {
                    document.location = Ecomarket.Messaging.Constants.INBOX;
                }
            });
    });
}

Ecomarket.Messaging.MarkUnAnsweredSelected = function(){
    // Used for marking resolved *and* unresolved.
    var selector = ".toolbar-active .btn-mark-unanswered-messages.ajax";
    $(document).on("click", selector, function(event) {
        var $btn = $(selector);
        var url = $(this).attr('data-source');
        var target = $(this).attr('data-target');
        var checked = $('input[name=all]').serialize();
        url += '?' + 'tab=inbox&' + checked;
        $.get(url, function(data) {
            document.location = Ecomarket.Messaging.Constants.INBOX;
        });
    });
}

Ecomarket.Messaging.ViewMessage = function(){
    var selector = ".ln-view-message.ajax"
    var new_messages_count_selector = '#user-new-messages'
    $(document).on("click", selector, function(event) {
        var url = $(this).attr('data-source');
        url += '?' + 'tab=inbox&' + checked;
        var url_new_messages = $(new_messages_count_selector).attr('data-source');
        $('.actions-toolbar .btn-group.actions').removeClass('toolbar-active');
        $.ajax({url: url,
                async: false, 
                success: function(data) {
                    $('#messages-container').html(data);
                }
        });
        $.ajax({url: url_new_messages,
                async: false, 
                success: function(data) {
                    $(new_messages_count_selector).html(data);
                }
        });
        $('.actions-toolbar .btn-group.actions').addClass('toolbar-active');
        var scroll_target = document.getElementById("scroll-target");
        if( scroll_target ) {
            scroll_target.scrollIntoView();
        }
    });
}

Ecomarket.Messaging.ViewMessageSent = function(){
    var selector = ".ln-view-message-sent.ajax"
    $(document).on("click", selector, function(event) {
        var url = $(this).attr('data-source');
        $('.section-tabs .nav-tabs. .active').removeClass('active');
        $('#sent .inbox-container').html("");
        $.get(url, function(data) {
            $('#messages-container').html(data);
        });
        $('.actions-toolbar .btn-group.actions').addClass('toolbar-active');
        var scroll_target = document.getElementById("scroll-target");
        if( scroll_target ) {
            scroll_target.scrollIntoView();
        }
    });
}

Ecomarket.Messaging.ScrollReply = function(){
    var selector = "#reply-message"
    var scrollTo = "#scroll-target"
    $(selector).on("shown", function(event) {
        var scroll_target = document.getElementById("scroll-target");
        if( scroll_target ) {            
            scroll_target.scrollIntoView();
            event.preventDefault();
            return false;
        }
    });
}

Ecomarket.Messaging.ScrollViewThread = function(){
    var element_to_scroll = document.getElementById("scroll-target-view");
    if (element_to_scroll) {
        element_to_scroll.scrollIntoView();
    }
    return false;
}

Ecomarket.Messaging.ActiveToolBar = function(){
    var selector = "input[name=all]"
    $(document).on("change", selector, function(event) {
        if ($(this).attr('checked') === 'checked') {
            if ($('.actions-toolbar .btn-group.actions').hasClass('toolbar-active') == false) {
                $('.actions-toolbar .btn-group.actions').addClass('toolbar-active');
            }
        }
    });
}

Ecomarket.Messaging.SetupToggleCheckbox = function(){
    var selector_toggle = "input[name=messages]";
    var selector_all = "input[name=all]";
    var select_all_checked = "input[name=all]:checked";
    var number_of_checkboxes = $(selector_all).length;
    $(document).on("change", selector_toggle, function(event) {
        $(selector_all).prop("checked", $(this).prop("checked")).trigger("change");
    });
    $(document).on("change", selector_all, function(event) {
        $(selector_toggle).prop("checked", $(select_all_checked).length == number_of_checkboxes);
    });
}

Ecomarket.Widgets.ResolveButton = function(){
    if($('.btn-resolve').length == 0) return false;
    $(document).on("click.resolvebutton touchstart.resolvebutton", '.btn-resolve', this.toggle.bind(this));
    $(document).on("mouseover.resolvebutton", '.btn-resolve', this.hoverIn.bind(this));
    $(document).on("mouseout.resolvebutton", '.btn-resolve', this.hoverOut.bind(this));
}

Ecomarket.Widgets.ResolveButton.prototype.toggle = function(event){
    event.preventDefault();
    var btn = $(event.target)
    if(btn.hasClass('animating'))
        return;

    var message_id = btn.attr('data-thread-id');
    var button_text = null;
    var add_class = null
    var remove_class = null;

    if(btn.hasClass('btn-unresolved')) {
        add_class = 'btn-resolved';
        remove_class = 'btn-unresolved';
        button_text = 'Resolved';
    } else {
        add_class = 'btn-unresolved';
        remove_class = 'btn-resolved';
        button_text = 'Unresolved';
    }

    btn.addClass('animating').fadeOut(function() {
        $(this).addClass('btn-resolved').removeClass('btn-unresolved');
        var url = $(this).attr('data-source');
        var target = $(this).attr('data-target');
        url += '&tab=inbox&all=' + message_id;
        $.get(url, function(data) {
            $('#messages-container').html(data);
        });
        $(this).html(button_text);
        $(this).fadeIn(function() {
            $(this).removeClass('animating')
        });
    });
}

Ecomarket.Widgets.ResolveButton.prototype.hoverIn = function(event){
    var btn = $(event.target)
    text = $(btn).html();
    if(text === "Unresolved"){
        $(btn).html("Resolve?")
    } else if(text === "Resolved"){
        $(btn).html("Unresolve?")
    }
}

Ecomarket.Widgets.ResolveButton.prototype.hoverOut = function(event){
    var btn = $(event.target)
    text = $(btn).html();
    if(text === "Resolve?"){
      $(btn).html("Unresolved")
    } else if (text === "Unresolve?"){
      $(btn).html("Resolved")
    }
}

jQuery(document).ready(function($){
    Ecomarket.scroll_reply = new Ecomarket.Messaging.ScrollReply();
    Ecomarket.compose_modal = new Ecomarket.Messaging.ComposeModal();
    Ecomarket.reply_modal = new Ecomarket.Messaging.ReplyModal();
    Ecomarket.compose_submit_button = new Ecomarket.Messaging.ComposeSubmitButton();
    Ecomarket.view_message = new Ecomarket.Messaging.ViewMessage();
    Ecomarket.view_message_sent = new Ecomarket.Messaging.ViewMessageSent();
    Ecomarket.delete_selected = new Ecomarket.Messaging.DeleteSelected();
    Ecomarket.mark_read_selected = new Ecomarket.Messaging.MarkReadSelected();
    Ecomarket.mark_unread_selected = new Ecomarket.Messaging.MarkUnReadSelected();
    Ecomarket.mark_unanswered_selected = new Ecomarket.Messaging.MarkUnAnsweredSelected();
    Ecomarket.active_toolbar = new Ecomarket.Messaging.ActiveToolBar();
    Ecomarket.scroll_view_thread = new Ecomarket.Messaging.ScrollViewThread();
    Ecomarket.setup_toggle_checkbox = new Ecomarket.Messaging.SetupToggleCheckbox();
    Ecomarket.resolve_button = new Ecomarket.Widgets.ResolveButton();
    Ecomarket.compose_typeahead = new Ecomarket.Messaging.ComposeModalSetupTypeahead();
})
