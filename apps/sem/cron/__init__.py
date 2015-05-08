import logging

from django_cron import CronJobBase, Schedule

from sem.management.commands.sync_adwords_ads import Command
from sem.management.commands.update_adwords import Command as UpdateAdwords


logger = logging.getLogger(__name__)


class AdWordsPullCron(CronJobBase):
    """
    This Job will pull data from Google AdWords API.
    Runs every 40th minute of every hour.
    """
    RUN_AT_TIMES = ['%s:40' % str(j) for j in range(0, 24)]

    schedule = Schedule(run_at_times=RUN_AT_TIMES)
    code = 'sem.cron.adowrds_pull_cron'

    def do(self):
        logger.info("Starting AdWords Pull Cron")
        cmd = Command()
        cmd.handle()
        logger.info("Finished AdWords Pull Cron")


class AdWordsManipulateCron(CronJobBase):
    """
    We manipulate the Bids on AdWords Ads to optimize them as needed.
    """
    RUN_AT_TIMES = ['%s:50' % str(j) for j in range(0, 24)]

    schedule = Schedule(run_at_times=RUN_AT_TIMES)
    code = 'sem.cron.adowrds_pull_cron'

    def do(self):
        logger.info("Starting AdWords Manipulation Cron")
        cmd = UpdateAdwords()
        cmd.handle()
        logger.info("Finished AdWords Manipulation Cron")