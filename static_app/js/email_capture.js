"use strict";

function setup_capture_form(modal) {
    $('.modal-capture .sign-in').click(function(){
        $('#login').modal('toggle');
        modal.modal('toggle');
    });
    var form = modal.find("form.form");
    form.ajaxForm({
        beforeSubmit: function() {
            form.find("button").button("loading");
        },
        success: function(data) {
            modal.html(data);
            setup_capture_form(modal);
        }
    });
}


$(document).ready(function(){
    var modal = $('#capture');
    /* capture form */
    if($.cookie('ecomarket') === undefined ){
        $.ajax({
            url: "mailinglists/signup/",
            success: function(data) {
                modal.html(data).modal("toggle");
                setup_capture_form(modal);
            }
        });
        // SET COOKIE
        $.cookie('ecomarket','true', {'expires': 30});
    }
});

// refresh the page for user login
$(document).on('click', '.reload-after-click', function(){
    location.reload();
});
