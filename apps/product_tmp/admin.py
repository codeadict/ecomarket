from __future__ import absolute_import

import copy
import datetime
from itertools import chain
from urlparse import urljoin

from categories.admin import CategoryBaseAdmin
from django import forms
from django.conf import settings
from django.contrib import admin
from django.forms import widgets
from django.forms.util import flatatt, to_current_timezone
from django.utils.datastructures import MultiValueDict, MergeDict
from django.utils.html import escape, conditional_escape
from django.utils.translation import ugettext, ugettext_lazy
from django.utils.encoding import StrAndUnicode, force_unicode
from django.utils.safestring import mark_safe
from django.utils import datetime_safe, formats

from marketplace.models import Recipient
from product_tmp.models import OldCategory, TempProduct


class OldCategoryAdmin(CategoryBaseAdmin):
    pass


def convert_recipients_to_list(recipients=None):
    if not recipients:
        recipients = unicode([u'everyone', ])
    #if type(recipients) in [type(''), type(u'')]:
    recipients = recipients.replace("[", '').replace("]", '')
    recipients = recipients.replace("u'", '')
    recipients = recipients.replace("'", '')
    #recipients = recipients.replace(",", '')
    recipients = recipients.split(",")
    recipients = [i.strip() for i in recipients]
    return recipients

class CustomSelectMultiple(widgets.SelectMultiple):

    def render_options(self, choices, selected_choices):
        selected_choices = convert_recipients_to_list(selected_choices)
        # Normalize to strings.
        selected_choices = set(force_unicode(v) for v in selected_choices)
        output = []
        for option_value, option_label in chain(self.choices, choices):
            if isinstance(option_label, (list, tuple)):
                output.append(u'<optgroup label="%s">' % escape(force_unicode(option_value)))
                for option in option_label:
                    output.append(self.render_option(selected_choices, *option))
                output.append(u'</optgroup>')
            else:
                output.append(self.render_option(selected_choices, option_value, option_label))
        return u'\n'.join(output)

    def render(self, name, value, attrs=None, choices=()):
        if value is None: value = []
        final_attrs = self.build_attrs(attrs, name=name)
        output = [u'<select class="multiselect" multiple="multiple"%s  SIZE=18>' % flatatt(final_attrs)]
        options = self.render_options(choices, value)
        if options:
            output.append(options)
        output.append('</select>')
        return mark_safe(u'\n'.join(output))


RECIPIENT_CHOICES = []
for item in Recipient.objects.all():
    RECIPIENT_CHOICES.append((item.slug, item.title))

class TempProductAdminForm(forms.ModelForm):
    class Meta:
        model = TempProduct
    recipients = forms.CharField(widget=CustomSelectMultiple(choices=RECIPIENT_CHOICES))

    def clean_recipients(self, *args, **kwargs):
        cd = self.cleaned_data
        recipients = convert_recipients_to_list(cd['recipients'])
        if ('everyone' in recipients) and \
            not len(recipients)==1:
            raise forms.ValidationError, "You cannot add 'Everyone' with other choices."
        return cd['recipients']


class TempProductAdmin(admin.ModelAdmin):
    def desc(self, obj):
        s = obj.description
        s += "<br/>"
        s += obj.keywords
        s += "<br/>"
        url = "http://www.ethicalcommunity.com/index.php?option=com_ethmp&Itemid=117&id=%s&lang=en&view=product" % obj.id
        s += """<a href='%(url)s' >%(url)s</a>""" % {'url':url}
        return s
    desc.allow_tags = True

    list_display = ('title', 'desc', 'primary_category', 'recipients', 'old_category', )
    list_editable = ('primary_category', 'recipients')# 'recipient',)
    list_filter = ('last_updated_by', )
    list_select_related = True
    list_per_page = 5

    def get_changelist_form(self, request, **kwargs):
        kwargs.setdefault('form', TempProductAdminForm)
        return super(TempProductAdmin, self).get_changelist_form(request, **kwargs)

    def save_model(self, request, obj, form, change):
        obj.last_updated_by = request.user
        obj.save()


admin.site.register(OldCategory, OldCategoryAdmin)
admin.site.register(TempProduct, TempProductAdmin)
