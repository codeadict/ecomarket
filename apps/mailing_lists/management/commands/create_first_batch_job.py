from __future__ import print_function

from django.core.management.base import (NoArgsCommand, CommandError,
                                         make_option)
from django.db import transaction

from mailing_lists.constants import BatchStatus
from mailing_lists.models import BatchJob, MailingListSignup


class Command(NoArgsCommand):

    help = ("ONE OFF command to create a batch job containing all existing "
            "MailingListSignup objects")
    option_list = NoArgsCommand.option_list + (
        make_option("-f", "--force", action="store_true", dest="force",
                    default=False,
                    help="Create the batch job, even if one already exists"),
    )

    @transaction.commit_on_success
    def handle_noargs(self, **options):
        if not options["force"] and BatchJob.objects.count():
            raise CommandError("A batch job already exists")
        added = 0
        batch_count = 0;
        try:
            job = BatchJob.objects.filter(status=BatchStatus.NEW)[0]
        except IndexError:
            job = None
        else:
            if (job.created.count() or job.updated.count()
                    or job.deleted.count()):
                msg = """\
There is already a new batch job with tasks to perform. Please close the job
or clear its tasks before proceeding. The object signature looks like:
    {}""".format(repr(job))
                raise CommandError(msg)
        for mls in MailingListSignup.objects.all():
            if job is None:
                job = BatchJob.objects.create()
            job.created.add(mls)
            added += 1
            batch_count += 1
            if added % 50 == 0:
                print("Added {} objects".format(added), file=self.stdout)
            if batch_count == 5000:
                batch_count = 0
                job = None
