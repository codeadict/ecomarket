# Starting out from a fresh server #

These are steps i did to install the app on the server and some basic sysadmin stuff. This guide is applicable to Ubuntu Precise, with python 2.7. Minimal changes would be required for higher versions.

Our image is a fresh Ubuntu 12.04 image 64bit

## Setting up User ##
Added my key to /home/ubuntu/.ssh/authorized_keys

Add Ubuntu to sudoers

    sudo visudo

Paste the following at the end. This enables you to use sudo without password

    ubuntu  ALL=(ALL) NOPASSWD:ALL


## Installing required tools ##

Log on as ubuntu user

    ssh-keygen -C <ubuntu@server_ip> -b 2048
    sudo apt-get update
    sudo apt-get upgrade


External requirements for making it easier to install modules like mysql + PIL inside virtualenv
set passwd for mysql user root

    yes| sudo apt-get install nginx mysql-server mysql-client locate python-setuptools python-pip git-core subversion mercurial htop screen byobu memcached unzip default-jre

    # for lxml, pil, mysql
    yes| sudo apt-get install python-dev libjpeg62-dev zlib1g-dev libfreetype6-dev liblcms1-dev libxml2-dev libxslt-dev libmysqlclient-dev

    # for pycurl
    yes| sudo apt-get install python-pycurl-dbg librtmp-dev libcurl4-openssl-dev


### Security ###

TODO
    * Install logwatch
    * Install port knock


Install python-based intrusion prevention software

    sudo apt-get install fail2ban


change default ssh port to "Port XXXX"

    sudo nano /etc/ssh/sshd_config
    sudo /etc/init.d/ssh restart


### virtualenv/virtualenvwrapper ###

    sudo easy_install pip
    sudo pip install virtualenv virtualenvwrapper

Note where it installs virtualenvwrapper.sh
The installation script says something like ----> changing mode of /usr/bin/virtualenvwrapper.sh to 755

    export WORKON_HOME=~/venvs
    source /usr/local/bin/virtualenvwrapper.sh

Copy these lines at the top of ~/.bashrc
The above lines should appear above [ -z "$PS1" ] && return

    # ---------------------------------------------
    # virtualenvwrapper
    export WORKON_HOME=~/venvs
    source /usr/local/bin/virtualenvwrapper.sh
    export PIP_VIRTUALENV_BASE=$WORKON_HOME
    export PIP_RESPECT_VIRTUALENV=true
    # ---------------------------------------------

Create the directory to hold virtual environments and then load virtualenv.
    mkdir ~/venvs
    source ~/.bashrc
    mkvirtualenv --no-site-packages ecomarket

From this point you can always use the ``workon`` command to start a virtual environment
Here ecomarket is the name we gave our virtualenv. For more info goto - http://www.doughellmann.com/docs/virtualenvwrapper/

    workon ecomarket


### Django ###

    workon ecomarket

    mkdir ~/webapps/
    cd ~/webapps/
    git clone <repo_url> # assuming the dir name created is <app>. If not then rename it to something appropriate
    cd <app>
    pip install -r requirements.txt


### nginx ###

Remove default app
    sudo rm /etc/nginx/sites-enabled/000-default

Create new nginx config for the site

    sudo touch /etc/nginx/sites-available/<app>

Copy the following to the file /etc/nginx/sites-available/<app>

    server {
        listen 80;
        client_max_body_size 4G;
        server_name example.cloudshuffle.com;

        keepalive_timeout 5;

        location /static/admin {
            root  /home/ubuntu/webapps/example/;
            expires 7d;
        }

        location /static/ {
            root  /home/ubuntu/webapps/example/;
            expires 7d;
        }

        location /media/ {
            root  /home/ubuntu/webapps/example/;
            expires 7d;
        }

        location / {
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header Host $http_host;
            proxy_redirect off;
            proxy_pass http://127.0.0.1:8000;

            #gzip on;
            #gzip_types       text/plain application/xml text/xml;
            #gzip_proxied any;
        }

        #error_page 500 502 503 504 /500.html;
        #location = /500.html {
        #    root /path/to/app/current/public;
        #}
    }

Enable it using
    sudo ln -s /etc/nginx/sites-available/<app> /etc/nginx/sites-enabled/<app>

For this project, you can find the nginx config file under conf/<env>/*.nginx.conf


### Solr ###

Install solr on the server, to the ~/apps/ directory

    wget http://apache.techartifact.com/mirror/lucene/solr/3.6.0/apache-solr-3.6.0.zip
    unzip apache-solr-3.6.0.zip
    mkdir apps
    mv apache-solr-3.6.0 apps/solr/
    rm apache-solr-3.6.0.zip

Install solr as a system daemon

    sudo cp conf/solr /etc/init.d/solr
    sudo chmod ugo+x /etc/init.d/solr

TODO: Setup schema


### Supervisord ###

Make sure the conf/supervisord/supevisord.conf file is up to date in our codebase.

Install supervisor

    sudo pip install supervisor


Install to upstart
    sudo cp ~/webapps/<app>/conf/supervisor/supervisord /etc/init.d/.
    sudo chmod +x /etc/init.d/supervisord
    sudo update-rc.d supervisord defaults


Now we'll tell supervisord about our django app + solr + celery.
There's a ready made conf file in our codebase. So you can simply
copy over supervisord.conf from the codebase.

    sudo cp ~/webapps/<app>/conf/supervisor/supervisord.conf /etc/.


You can also create a new sample conf using, if you want to start from scratch.

    sudo echo_supervisord_conf > /etc/supervisord.conf


Start supervisor daemon

    sudo /etc/init.d/supervisord start
    sudo supervisorctl status


After any edits to the supervisord.conf, you should restart it

    sudo /etc/init.d/supervisord restart


Now you should be able to start/stop your app:

    sudo supervisorctl restart <app>


### Sources ###

* http://brandonkonkle.com/blog/2010/jun/25/provisioning-new-ubuntu-server-django/
* http://supervisord.org/installing.html
* http://bluebream.zope.org/doc/1.0/manual/deployment.html
