from django.core.urlresolvers import reverse
from django.db import DatabaseError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_safe, require_http_methods

from django.contrib.auth.decorators import login_required
from django.contrib import comments
from django.contrib.comments import signals
from django.contrib.contenttypes.models import ContentType

from threadedcomments.models import ThreadedCommentFlag


def perform_delete(request, comment):
    # Reimplementation of comments.views.moderation.perform_delete
    # See https://github.com/django/django-contrib-comments/issues/1
    # TODO if the above issue is fixed, see if it provides a better solution
    flag, created = ThreadedCommentFlag.objects.get_or_create(
        comment=comment,
        user=request.user,
        flag=comments.models.CommentFlag.MODERATOR_DELETION
    )
    comment.is_removed = True
    comment.save()
    signals.comment_was_flagged.send(
        sender=comment.__class__,
        comment=comment,
        flag=flag,
        created=created,
        request=request,
    )


@require_http_methods(["DELETE"])
@login_required
def delete(request, comment_id):
    """
    Deletes a comment. Comment must belong to the user.
    """
    comment = get_object_or_404(comments.get_model(),
                                pk=comment_id, user=request.user)
    # Fallback to home page in worst case.
    next_ = request.GET.get('next', '/')
    try:
        perform_delete(request, comment)
    except DatabaseError:
        return HttpResponse("ERROR", status=500)

    if request.is_ajax():
        return HttpResponse("OK")
    return HttpResponseRedirect(next_)


@require_safe
def reply(request, comment_id, template_name="comments/reply_form.html"):
    comment = get_object_or_404(comments.get_model(), pk=comment_id)
    form = comments.get_form()(comment.content_object,
                               initial={"parent_id": comment.id})

    return render(request, template_name, {
        "object": comment.content_object,
        "form": form,
        "form_id": "{}-reply-{}".format(comment.content_object.id, comment_id),
        "form_target": reverse("comment_reply", args=[comment_id]),
    })


@require_safe
def create(request, content_type_id, object_id, template_name="comments/reply_form.html"):
    print content_type_id, object_id
    ctype = get_object_or_404(ContentType, id=content_type_id)
    entity = get_object_or_404(ctype.model_class(), pk=object_id)
    print ctype, entity
    form = comments.get_form()(entity)
    return render(request, template_name, {
        "object": entity,
        "form": form,
        "form_id": "{}-comment".format(entity.id),
    })