from django.conf import settings
from django.core.management.base import NoArgsCommand, CommandError

from datetime import datetime
from os import path

import commands


class Command(NoArgsCommand):
    help = "Create a db backup"

    def handle_noargs(self, **options):        
        backdir = getattr(settings, 'DATABASE_BACKUP_ROOT', '~/backups/')
        if not backdir:
            raise CommandError('"DATABASE_BACKUP_ROOT" must be a valid dir path.')
        if backdir[0] == '~':
            backdir = path.expanduser(backdir)
        if not path.exists(backdir):
            mkdir_cmd = 'mkdir %s' %backdir
            status, output = commands.getstatusoutput(mkdir_cmd)            
            if status != 0:
                raise CommandError(output)
        
        #using the default db conf
        default = settings.DATABASES.get('default', None)
        if default is None:
            raise CommandError('Default db conf do not exist in settings file')
        dbname = default.get('NAME', '')
        user = default.get('USER', '')
        passwd = default.get('PASSWORD', '')
        
        filepath = path.join(backdir, '%s_%s.sql.gz'%(dbname,datetime.now().strftime('%Y%m%d%H%M%S')))
        
        # for mysql        
        backup_cmd = 'mysqldump --single-transaction -u%s -p%s %s | gzip > %s' %(user, passwd, dbname, filepath)
        status, output = commands.getstatusoutput(backup_cmd)            
        if status != 0:
            raise CommandError(output)        
