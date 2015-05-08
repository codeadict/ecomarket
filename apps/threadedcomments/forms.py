from itertools import chain

from django import forms
from django.core.validators import EMPTY_VALUES
from django.contrib.comments.forms import CommentForm

from apps.spamish.utils import get_validators

from threadedcomments.models import ThreadedComment


class CommentFormWithSpamish(CommentForm):
    """
    Override Django comment form to do some spam protection etc.
    """

    UNWANTED_COMMENT_DATA = frozenset(["user_name", "user_email", "user_url"])

    # TODO adjustable default
    post_to_facebook = forms.BooleanField(initial=True, required=False,
            label="Post to facebook?", widget=forms.CheckboxInput(
                attrs={"class": "eco-checkbox"}))
    parent_id = forms.ChoiceField(required=False)

    def __init__(self, target_object, *args, **kwargs):
        super(CommentFormWithSpamish, self).__init__(
            target_object, *args, **kwargs)
        # TODO should we validate that you can only link to comments on the
        # same page?
        self.fields["parent_id"].choices = chain(
            [("", "")], ThreadedComment.objects.values_list("id", "comment"))

    def get_comment_model(self):
        return ThreadedComment

    def get_comment_create_data(self):
        data = super(CommentFormWithSpamish, self).get_comment_create_data()
        for key in self.UNWANTED_COMMENT_DATA:
            del data[key]
        data["post_to_facebook"] = self.cleaned_data["post_to_facebook"]
        data["parent_id"] = self.cleaned_data["parent_id"]
        return data

    def check_for_duplicate_comment(self, new):
        # Near-complete copy of superclass. Man, django.contrib.comments sucks!
        possible_duplicates = self.get_comment_model()._default_manager.using(
            self.target_object._state.db
        ).filter(
            content_type=new.content_type,
            object_pk=new.object_pk,
        )
        for old in possible_duplicates:
            if (old.submit_date.date() == new.submit_date.date()
                    and old.comment == new.comment):
                return old

        return new

    def clean_comment(self):
        comment = self.cleaned_data['comment']
        for validator in get_validators():
            validator(comment)
        return comment

    def clean_parent_id(self):
        parent_id = self.cleaned_data["parent_id"]
        if parent_id in EMPTY_VALUES:
            return None
        return parent_id

    def disable_facebook_by_default(self):
        # TODO This seems a bit hacky. Is there a better way to do this?
        self.fields["post_to_facebook"].initial = False
