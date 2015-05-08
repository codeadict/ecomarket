Ecomarket
=========

In order to run Ecomarket during development you need to do:

Clone the repo first

    git clone git@github.com:ecomarket/ecomarket.git
    cd ecomarket

On local you need to install all required system dependencies

    sudo apt-get install python-setuptools libmysqlclient-dev mysql-server python-dev python-pip default-jre libxml2-dev libxslt1-dev git
    pip install fabric virtualenv virtualenvwrapper

Install dependencies, optionally within a virtualenv

    mkvirtualenv --no-site-packages ecomarket
    workon ecomarket
    pip install -r requirements.txt

If you get "ImportError: No module named pkg_resources" in-between
    curl http://python-distribute.org/distribute_setup.py | python

Then create a local database called `ecomdb_0` with username & password as  `ecomarket`, if required copy the sample local_settings.py file to root and modify the DB settings.

Then import a copy of the development database into mysql
    
    pv ecomdb_0_dump.sql | mysql -uroot -ppassword ecomdb_0    
    python manage.py build_solr_schema > ../apache-solr-3.6.1/example/solr/conf/schema.xml
    python manage.py collectstatic
    python manage.py update_static_categories
    python manage.py rebuild_index
    python manage.py runserver

Configuring & Running Apache Solr

    wget http://archive.apache.org/dist/lucene/solr/3.6.1/apache-solr-3.6.1.tgz
    tar -xf apache-solr-3.6.1.tgz
    cd apache-solr-3.6.1/example
    echo '' > solr/conf/stopwords_en.txt
    java -Dsolr.solr.home="./solr/" -jar start.jar


Install and run compass SCSS compressor:

    sudo apt-get install rubygems
    sudo gem install sass compass
    cd static_app && ./compass_watch.sh
