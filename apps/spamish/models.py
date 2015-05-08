from django.db import models
from django.utils.translation import ugettext_lazy as _


class BannedWordManager(models.Manager):

    def active(self):
        return self.filter(active=True)


class BannedWord(models.Model):
    """
    Model for storing words (or phrases) that users are not allowed to message
    each other. For example, swear words or words often associated with spam
    like 'viagra'.
    """
    word = models.CharField(_(u"Word"), max_length=255, help_text=_(u"Word or phrase to ban (case insensitive)."))
    active = models.BooleanField(_(U"Active"), default=True)

    objects = BannedWordManager()

    class Meta:
        ordering = ('word',)

    def __unicode__(self):
        return self.word
