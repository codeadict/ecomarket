/*global Ecomarket */

// Comment button
function highlightError(element) {
    element.parent().parent().addClass('error');
}
function removeError(element) {
    element.parent().parent().removeClass('error');
}
Ecomarket.Widgets.CommentButton = function() {
    $(document).on('click', '.btn-comment', this.comment.bind(this));
    $(document).on('click', '.btn-comment-login', function(event){
        event.preventDefault();
        $("#login").modal('toggle');
    });

    $(document).on('click', '.btn-comment-register', function(event){
        event.preventDefault();
        $("#register-modal").modal('toggle');
    });
};
Ecomarket.Widgets.CommentButton.prototype.comment = function(event) {
    /* TODO use Jquery.form for this whole thing */
    event.preventDefault();
    var btn = $(event.target),
        container = btn.parents(btn.data('id')).filter(":first"),
        comment = container.find('#id_comment'),
        error = (comment.val().trim() === ""),
        commentwrap = btn.parent(),
        data, commentform, comment_list;
    if (container.is("form")) {
        commentform = container;
    } else {
        commentform = container.find("form").filter(":first");
    }
    if (!error) {
        data = $(commentform).serialize();
        btn.button("loading");
        $.ajax({
            type: "POST",
            data: data,
            url: btn.data('source'),
            cache: false,
            dataType: "html",
            success: function(html, textStatus) {
                var errorlist = $(html).find('[class="errorlist"]'),
                    has_errored = $(errorlist).length > 0,
                    postedComment = $(html).filter('div#newly_posted_comment').html();

                btn.button("reset");

                if ($(".latest-comment").length > 0) {
                    // Pages with a small latest comment box.
                    if (has_errored) {
                        $(".latest-comment").find('.errorlist').remove();
                        comment.after(errorlist);
                    } else {
                        $(".latest-comment").find('.errorlist').remove();
                        container.parent().find('li').remove();
                        $('.comments').append('<li>' + postedComment +'</li>');
                        $('.comments').find("a.comment-reply").remove();
                        commentform.get(0).reset();
                    }
                } else if (commentform.is(".status-form")) {
                    // Status updates.
                    if (has_errored) {
                        $(".status-form").find('.errorlist').remove();
                        $('#send_comment').after(errorlist);
                    } else {
                        $(".status-form").find('.errorlist').remove();
                        $(".comments").prepend('<li>' + postedComment +'</li>');
                        commentform.get(0).reset();
                        window.location.reload();
                    }
                } else {
                    // General comments.
                    if (container.is("li")) {
                        comment_list = container.parent();
                    } else {
                        comment_list = container.parent().children('.comments');
                    }
                    if (has_errored) {
                        comment_list.find('.errorlist').remove();
                        comment.after(errorlist);
                    } else {
                        comment_list.find('.errorlist').remove();
                        if (container.is("li")) {
                            container.before('<li>' + postedComment +'</li>');
                            container.remove();
                        } else {
                            comment_list.append('<li>' + postedComment +'</li>');
                            commentform.get(0).reset();
                        }
                    }
                }
                removeError(comment);

            },
            error: function(XMLHttpRequest, textStatus, errorThrown) {
                container.replaceWith('<p>Your comment was unable to be posted at this time. We apologise for the inconvenience.</p>');
            }
        });
    } else {
        highlightError(comment);
    }
    return false;
};

// Delete button
Ecomarket.Widgets.DeleteButton = function() {
    $(document).on('click', '.comment-delete', function(e){
        e.preventDefault();
        var btn = $(this),
            delete_url = $(this).attr('href');
        $.ajax(delete_url, {
            type: "DELETE",
            success: function(data) {
                if (data === 'OK') {
                    btn.closest('.comment, .activity').remove();
                }
            }
        });
    });
};

Ecomarket.Widgets.ReplyToComment = function() {
    this.show_selector = '.comment-reply';
    this.hide_selector = '.comment-reply-close';
};
Ecomarket.Widgets.ReplyToComment.prototype.setup = function() {
    $(document).on('click', this.show_selector, this.show.bind(this));
    $(document).on('click', this.hide_selector, this.hide.bind(this));
};
Ecomarket.Widgets.ReplyToComment.prototype.show = function(event) {
    var reply_button = $(event.target),
        li = $(reply_button.data("toplevel_comment")),
        target = reply_button.attr("href");
    $.get(target, function(data) {
        /*
        var parent_elem;
        if (li.children("ul.comments").length) {
            parent_elem = li.children("ul.comments");
        } else {
            parent_elem = $("<ul />").addClass("comments").appendTo(li);
        }
        if (parent_elem.children("li.comment-form-container").length) {
            parent_elem.find("li.comment-form-container").html(data);
        } else {
            $("<li />").addClass("comment-form-container")
                       .append(data).appendTo(parent_elem);
        }
        Ecomarket.eco_checkbox.setup(
            parent_elem.find(".eco-checkbox"));
        setTimeout(function(){ parent_elem.find("textarea").focus(); }, 50);
        */
        var comment_li = $('<li class="activity" />')
            .insertAfter(li);
        $("<div />").addClass("comment-form-container")
            .append(data).appendTo(comment_li);
        comment_li.parent('ol').addClass('comments');
        Ecomarket.eco_checkbox.setup(
            comment_li.find(".eco-checkbox"));
        setTimeout(function(){ parent_elem.find("textarea").focus(); }, 50);
    });
    event.preventDefault();
};
Ecomarket.Widgets.ReplyToComment.prototype.hide = function(event) {
    var li = $(event.target).parents("li").filter(":first"),
        ul = li.parent();
    li.remove();
    if (ul.children().length === 0) {
        ul.remove();
    }
    event.preventDefault();
};
Ecomarket.Widgets.ReplyToComment.prototype.from_hash = function(hash) {
    // Hash takes the form #reply-comment-ID
    var comment = $(hash[0] + hash.substring(7, hash.length));
    comment.find(this.show_selector).filter(":first").click();
    if( comment.length > 0 ) {
        comment[0].scrollIntoView(true);
    }
};


jQuery(document).ready(function($) {
    Ecomarket.comment_button = new Ecomarket.Widgets.CommentButton();
    Ecomarket.comment_delete = new Ecomarket.Widgets.DeleteButton();
    $("#go-to-comment-form").click(function(){
        var form = $($(this).attr("href"));
        setTimeout(function(){ form.find("#id_comment").focus(); }, 50);
    });
    Ecomarket.reply_to_comment = new Ecomarket.Widgets.ReplyToComment();
    Ecomarket.reply_to_comment.setup();
    if (window.location.hash.indexOf("reply-") === 1) {
        Ecomarket.reply_to_comment.from_hash(window.location.hash);
    }
});
