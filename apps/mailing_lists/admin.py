import csv
from functools import update_wrapper
from tempfile import NamedTemporaryFile

from django.shortcuts import redirect
from django.conf.urls.defaults import patterns, url
from django.forms.forms import ErrorList
from django.views.generic import FormView

from django.contrib import admin
from django.contrib import messages

from mailing_lists.forms import BulkUpdateForm
from mailing_lists.importer import MissingRequiredColumn, CsvImporter
from mailing_lists.models import MailingListSignup


class MailingListBulkUpdateView(FormView):

    form_class = BulkUpdateForm
    template_name = "admin/mailing_lists/bulk_update.html"

    def get_context_data(self, form):
        adminform = admin.helpers.AdminForm(
            form, [(None, {"fields": form.base_fields.keys()})], {})
        return {
            "form": form,
            "adminform": adminform,
            "title": "Bulk Upload",
            "opts": MailingListSignup._meta,
        }

    def form_valid(self, form):
        with NamedTemporaryFile(suffix=".csv") as fh:
            importer = CsvImporter(fh.name)
            reader = csv.DictReader(form.cleaned_data["csv_file"])
            try:
                importer.import_csv(reader)
            except MissingRequiredColumn, e:
                error_msg = "File is missing required column '{}'".format(e)
                # TODO: Don't do this dirty hack
                form._errors["csv_file"] = ErrorList([error_msg])
                return self.form_invalid(form)
            messages.info(
                self.request,
                "Imported {} addresses".format(importer.import_count))
            if importer.reject_count > 0:
                fh.seek(0)
                context = self.get_context_data(form)
                context.update({
                    "reject_count": importer.reject_count,
                    "rejected_emails": fh.read().strip().split("\n"),
                })
                return self.render_to_response(context)
        return redirect("admin:mailing_lists_mailinglistsignup_changelist")


class MailingListAdmin(admin.ModelAdmin):
    date_hierarchy = 'date_added'
    list_display = ('email_address', 'user', 'first_name', 'last_name')
    search_fields = ['email_address']
    list_filter = ['date_added', 'source']

    def get_urls(self):
        def wrap(view):
            """Copied from admin.ModelAdmin.get_urls"""
            def wrapper(*args, **kwargs):
                return self.admin_site.admin_view(view)(*args, **kwargs)
            return update_wrapper(wrapper, view)

        urls = super(MailingListAdmin, self).get_urls()
        return patterns("",
            url(r"^bulk_upload/$", wrap(MailingListBulkUpdateView.as_view()),
                name="bulk_upload"),
        ) + urls


admin.site.register(MailingListSignup, MailingListAdmin)
