from __future__ import with_statement

import time

from fabric.api import cd, \
                        env, \
                        local, \
                        put, \
                        require, \
                        run as fabric_run, \
                        settings as fabric_settings, \
                        sudo as fabric_sudo
from fabric.contrib.console import confirm

USAGE = '''
================================================================
NOTE:
    using this fabfile expects that you have the python utility
fabric locally installed, ssh access to your servers, and your
ssh public key assciated with the account 'root@'
================================================================
USAGE:

* fab help
    print this command

* fab (stage|live) deploy
    updates a project to the latest release and applies database updates

* fab (stage|live) setup
    setups a site from scratch

* fab (stage|live) syncdb
    runs django-admin.py syncdb --migrate (including migrations)

* fab (stage|live) build_solr_schema
    builds and installs a new solr schema

* fab (stage|live) rebuild_index
    rebuilds the search indexes
================================================================
'''

def stage():
    '''
    Environment settings for stage.

    Usage:
         fab stage <task>
    '''
    env.name = 'stage'
    env.project_name = 'ecomarket'
    env.project_root = '~/webapps/%(project_name)s/' % env
    env.hosts = ['23.23.238.151']
    env.user = 'ubuntu'
    env.branch = 'master'
    env.venv_root = '/home/%(user)s/venvs/%(project_name)s/' % env
    env.virtualenv_activate = 'source /home/%(user)s/venvs/%(project_name)s/bin/activate' % env
    env.nginx_conf = '%(project_name)s.nginx.conf' % env

def live():
    '''
    Environment settings for live.

    Usage:
         fab live <task>
    '''
    yes = confirm("Are you sure you want to use LIVE and not stage?", default=False)
    if not yes:
        sys.exit()
    env.name = 'live'
    env.project_name = 'ecomarket'
    env.project_root = '~/webapps/%(project_name)s/' % env
    env.hosts = ['']
    env.user = 'ubuntu'
    env.branch = 'master'
    env.venv_root = '/home/%(user)s/venvs/%(project_name)s/' % env
    env.virtualenv_activate = 'source /home/%(user)s/venvs/%(project_name)s/bin/activate' % env
    env.nginx_conf = '%(project_name)s.nginx.conf' % env

# Utility functions
# =================
def run(command, shell=True, pty=True):
    return fabric_run(command % (env), shell=shell, pty=pty)

def sudo(command, shell=True, pty=True, user=None):
    return fabric_sudo(command % (env), shell=shell, user=user, pty=pty)

def virtualenv(command):
    with cd(env.project_root):
        run(env.virtualenv_activate + ' && ' + command)

def manage(command):
    virtualenv('python manage.py {0}'.format(command))

def help():
    print USAGE

# Deployment
# ===========
def deploy():
    '''
    Usage:

    $>fab <env name> deploy
    '''
    require('name')
    git_pull()
    setup_dirs()
    local_settings()
    install_requirements()
    collectstatic()
    syncdb_migrate()
    gunicorn_restart()

def local_settings():
    virtualenv('cp conf/%(name)s/local_settings.py .')

def collectstatic():
    manage('collectstatic -v0 --noinput')

def setup_dirs():
    with fabric_settings(warn_only=True):
        with cd(env.project_root):
            run("mkdir static")
            run("mkdir media")

        # CSS compress
        with cd(env.project_root):
            run("mkdir static/CACHE")
            run("chmod 777 static/CACHE")

        # Solr
        run("mkdir /tmp/solr.log")
        run("chmod 777 /tmp/solr.log")

def git_reset(do_reset=True):
    do_reset = confirm("Are you sure you want to reset?", default=False)
    if do_reset:
        with cd(env.project_root):
                run('git reset --hard')

def git_pull():
    with cd(env.project_root):
        run('git fetch;')
        run('git checkout %(branch)s; git pull origin %(branch)s;')

def clean():
    """Clear out extraneous files, like pyc/pyo"""
    virtualenv("""find -type f -name "*.py[co]" -delete""")

def syncdb_migrate():
    manage('syncdb --migrate')

def gunicorn_restart():
    "Restart the web server"
    sudo("sudo supervisorctl restart %(project_name)s")

def nginx_conf():
    "Restart the web server"
    with cd(env.project_root):
        sudo("cp conf/%(name)s/%(nginx_conf)s /etc/nginx/sites-available/.")
        with fabric_settings(warn_only=True):
            sudo("ln -s /etc/nginx/sites-available/%(nginx_conf)s /etc/nginx/sites-enabled/%(nginx_conf)s")

def nginx_restart():
    "Restart the web server"
    sudo("/etc/init.d/nginx restart")


# Solr
# =============

def build_solr_schema():
    """
    Builds a new SOLR schema and replaces the existing config.

    """
    manage('build_solr_schema -f /home/%(user)s/apps/solr/example/solr/conf/schema.xml')
    solr_restart()

def update_index():
    """
    Updates haystack indexes with 4 worker processes.

    """
    manage('update_index -k 4 --verbosity 2')

def rebuild_index():
    """
    Rebuilds haystack indexes with 4 worker processes.

    """
    manage('rebuild_index -k 4 --noinput --verbosity 2')

def solr_stop():
    sudo("/etc/init.d/solr stop")

def solr_start():
    sudo("/etc/init.d/solr start")

def solr_restart():
    sudo("/etc/init.d/solr restart")


# Server Setup
# TODO: Complete.
# See docs/server_setup.md for more details.
# ==================
def setup_dependencies():
    """
    For things that need to be installed via apt-get.
    These are installed before requirements.txt in the venv otherwise some python modules won't install properly
    """
    sudo('apt-get update')
    sudo("yes| apt-get install nginx mysql-server mysql-client locate python-setuptools python-pip git-core subversion mercurial htop screen byobu memcached unzip default-jre")
    sudo('yes| apt-get install python-dev libjpeg62-dev zlib1g-dev libfreetype6-dev liblcms1-dev libxml2-dev libxslt-dev libmysqlclient-dev')
    sudo('yes| apt-get install python-pycurl-dbg librtmp-dev libcurl4-openssl-dev')

def install_requirements():
    virtualenv('pip install -r requirements.txt')

def setup_solr_upstart():
    with cd(env.project_root):
        sudo('cp conf/solr /etc/init.d/solr')
        sudo('chmod ugo+x /etc/init.d/solr')

def setup_solr():
    with cd('~'):
        run('wget http://apache.techartifact.com/mirror/lucene/solr/4.0.0-ALPHA/apache-solr-4.0.0-ALPHA.zip')
        run('unzip apache-solr-4.0.0-ALPHA.zip')
        run('mkdir apps')
        run('mv apache-solr-4.0.0-ALPHA apps/solr/')


# Shortcuts
# ==================
def push2stage():
    local('git pull origin master', capture=False)
    local('git push origin master', capture=False)
    local('fab stage deploy', capture=False)

def push2live():
    local('git pull origin master', capture=False)
    local('git push origin master', capture=False)
    local('fab live deploy', capture=False)

try:
    from local_fabfile import *
except:
    pass

