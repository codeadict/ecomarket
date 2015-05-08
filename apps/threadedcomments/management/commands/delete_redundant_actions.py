from __future__ import print_function

from django.core.management.base import NoArgsCommand

from threadedcomments.models import ThreadedComment


class Command(NoArgsCommand):

    help = ("ONE-OFF command to delete actions that are now linked to deleted "
            "comments")

    def handle_noargs(self, **options):
        for comment in ThreadedComment.objects.filter(is_removed=True):
            msg = "Deleting action(s) for comment '{}' by {}".format(
                comment.comment, comment.user)
            print(msg, file=self.stdout)
            comment.action_object_actions.all().delete()
