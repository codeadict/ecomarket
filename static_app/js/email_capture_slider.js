$(document).ready(function(){

    var activate_area_height = 220; // height of activation area from bottom of article
    var bottom_of_article = $('.entry-content').offset().top + $('.entry-content').height();
    var activation_line = bottom_of_article - activate_area_height;
    var previous_scroll_pos = 0;
    var slider_class = '.capture-slider';
    var current_slider = 1;

    // make close button work
    $('.capture-slider .modal-header a.close').click(function(ev){
        ev.preventDefault();
        hide_slider(current_slider_class());
    });
    // submit form on return keypress
    $('.capture-slider2 input').keypress(function(ev){
        if(ev.which == 13) {
            $('.slider-form' + current_slider).submit();
            $('button[data-action=submit]').addClass('btn-loading');
    
        }
    });
    function handle_form_errors(form, resp){
        $('.ajax-error', form).remove();
        $('.control-group .error').removeClass('error');
        $.each(resp['errors'], function(field_name,error){
            field = form.find('#id_' + field_name);
            field.parent('control-group').addClass('error');
            error_ul = $("<ul />").addClass("errorlist ajax-error");
            error_li = $("<li />").html(error[0]);
            error_ul.append(error_li);
            field.parent().append(error_ul);
        }); 
    }
    function scroll_pos(){
        return $(document).scrollTop() + $(window).height();
    }
    function show_slider(selector){
        $(selector).animate({'right':'0'});
    }
    function hide_slider(selector){
        $(selector).animate({'right':'-220px'});
    }
    function show_hide_slider(selector){
        current_scroll_pos = scroll_pos();
        if ((current_scroll_pos > activation_line) & (previous_scroll_pos < activation_line)){
            show_slider(selector);
        } else if ((current_scroll_pos < activation_line) & (previous_scroll_pos > activation_line)){
            hide_slider(selector);
        }
        previous_scroll_pos = current_scroll_pos;
    }
    function current_slider_class(){
        return slider_class + current_slider;
    }
    function next_slider(){
        if(current_slider < 3){
            hide_slider(current_slider_class());
            if (current_slider == 1){
                $('.capture-slider2 #id_email').val($('.capture-slider1 #id_email_address').val());
                $('.capture-slider2 #id_first_name').focus();
            }
            current_slider += 1;
            show_slider(current_slider_class());
        } else {
        }
    }

    // the important bit
    $(window).scroll(function(){
        show_hide_slider(current_slider_class());
    });

    $('button[data-action="submit"]').click(function(ev){ 
        ev.preventDefault();
        $('.slider-form' + current_slider).submit();
    });

    $('.slider-form').on('submit', function(ev){
        ev.preventDefault();
        var form = $('.slider-form' + current_slider),
            url = form.attr('action'),
            ajax_req = $.ajax({
                url:url,
                type:'POST',
                data:form.serialize(),
                success:function(resp){

                    $('button[data-action=submit]').removeClass('btn-loading');
                    $('body').css('cursor','default');

                    if (resp.status == 'OK'){

                        next_slider();

                    } else if(resp.status == 'ERROR') {

                        // if email already exists just forward to next form
                        if ("SIGNEDUP" in resp.errors){

                            next_slider();

                        }
                        handle_form_errors(form, resp);
                        // if email is already registered offer option to login with it
                        form.find('.ajax-error a[data-toggle="modal"]').on('click', function(){

                            $('.capture1').modal('toggle');
                            hide_slider(current_slider_class());

                        });
                    }
                },
            });
        });
});
