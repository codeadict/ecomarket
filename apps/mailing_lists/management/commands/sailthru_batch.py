# coding=utf-8
from __future__ import print_function

import time

from django.core.management.base import NoArgsCommand
from django.utils.datetime_safe import datetime
from mailing_lists.models import BatchJob
from mailing_lists.constants import BatchStatus


class Command(NoArgsCommand):

    help = ("Export any outstanding batch jobs to Sailthru and wait for "
            "completion")

    PROVIDER = "sailthru"

    def handle_noargs(self, verbosity, **kwargs):
        try:
            verbosity = int(verbosity)
        except ValueError:
            verbosity = 1

        jobs = BatchJob.objects.filter(
            status__in=(BatchStatus.NEW, BatchStatus.FAILED))

        print("Found {} batch jobs".format(jobs.count()), file=self.stdout)

        for number, job in enumerate(jobs, 1):
            count = (job.created.count() + job.updated.count()
                     + job.deleted.count())
            if count == 0:
                print("Skipping empty job {num}...".format(num=number),
                      file=self.stdout)
                continue

            json_output = (self.stdout if verbosity >= 3 else None)

            job.submit(provider=self.PROVIDER, json_output=json_output)

            print("Job {num} started at {datetime}".format(
                num=number, datetime=job.submitted), file=self.stdout)

        filename = "/tmp/%s.txt" % __name__
        result_file = open(filename, "w")
        now = datetime.now()
        result_file.write(now.isoformat())

        ###
        ### NOTE:
        ### The following code breaks more stuff than it tries to "solve".
        ### It just blocks the execution of the command while waiting for BatchJobs to be finished.
        ### If the BatchJob does not finish nothing happens so it can run for eternity.
        ### It even waits for BatchJobs that don't run anymore!
        ###

        ## Check for any jobs that did not finish before
        #jobs = BatchJob.objects.filter(status=BatchStatus.IN_PROGRESS)
        #print("Waiting for {} batch jobs to complete".format(jobs.count()),
        #      file=self.stdout)
        #
        ## Re-poll every 20 seconds
        #jobs_finished = 0
        #messages = {
        #    BatchStatus.COMPLETED: "Job {num} completed at {datetime}",
        #    BatchStatus.FAILED: "Job {num} marked as failed",
        #}
        #
        #while jobs_finished < jobs.count():
        #    for number, job in enumerate(jobs, 1):
        #        if job.status != BatchStatus.IN_PROGRESS:
        #            continue
        #        status = job.check_status(provider=self.PROVIDER)
        #        if status == BatchStatus.IN_PROGRESS:
        #            continue
        #        elif status in messages:
        #            print(messages[status].format(
        #                num=number, datetime=job.completed), file=self.stdout)
        #            jobs_finished += 1
        #    if jobs_finished < jobs.count():
        #        time.sleep(20)
