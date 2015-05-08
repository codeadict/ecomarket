from django.db import models

from django.contrib.auth.models import User

class Todo(models.Model):

    """A thing the user must do.
    If the TodoMiddleware finds any Todo objects linked to the user, they will
    be redirected to the view corresponding to view_name.
    """

    user = models.ForeignKey(User, related_name="todos")
    creation_date = models.DateField(auto_now_add=True, editable=False)
    view_name = models.CharField(max_length=50)

    class Meta:
        ordering = ("user", "creation_date")
        unique_together = ("user", "view_name")

    def __unicode__(self):
        return u"{} must do {}".format(self.user, self.view_name)
