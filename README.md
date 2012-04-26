# perfbucket

## First things first

You need Cassandra running. See the [DataStax Community Edition guide](http://www.datastax.com/docs/1.0/install/install_package#installing-cassandra-rpm-packages). Install apache-cassandra1 (rather than dsc) to only get the open-source Cassandra tools, which are all you need.

## Initial setup on RHEL and CentOS (tested on CentOS 5)

1. Install Python 2.6 and its setuptools:

        yum install -y python26 python26-distribute python26-setuptools python26-devel git gcc
        easy_install-2.6 pip
        easy_install-2.6 -U distribute
        pip-2.6 install git+http://github.com/davidstrauss/perfbucket.git#egg=perfbucket
        ln -s /usr/bin/pip-2.6 /usr/bin/pip  # Optional, fixes Puppet PIP support.

1. Start and enable the Cassandra and perfbucker-watcher services:

        chkconfig cassandra on
        chkconfig perfbucket-watcher on
        /etc/init.d/cassandra start
        /etc/init.d/perfbucket-watcher start

## Initial setup on Fedora (tested on Fedora 16)

1. Set up the Python side:

        yum install -y python-pip gcc python-devel git
        pip-python install git+http://github.com/davidstrauss/perfbucket.git#egg=perfbucket
        ln -s /usr/bin/pip-python /usr/bin/pip  # Optional, fixes Puppet PIP support.

1. Optional: Copy the bundled perfbucket-watcher.service file into /etc/systemd/system to override the init script.
1. Start and enable the Cassandra and perfbucker-watcher services:

        systemctl enable cassandra.service perfbucket-watcher.service
        systemctl start cassandra.service perfbucket-watcher.service

## Final setup for all Red Hat-style systems

1. Initialize the perfbucket schema:

        perfbucket init

1. Set up the PHP side (or examine the files in the php directory to integrate manually). For now, PHP resources aren't installed by PIP.

        yum install -y httpd php php-devel php-pear gcc
        pecl install channel://pecl.php.net/xhprof-0.9.2
        git clone git+http://github.com/davidstrauss/perfbucket.git
        cd perfbucket/php
        ./install

## Usage

* Enable watching of a directory for xhprof/json files:

        perfbucket watch DIRECTORY

* View the slowest requests by hour:

        perfbucket show <verbose> requests

* View the slowest average pages by hour:

        perfbucket show <verbose> pages

* Output the xhprof-compatible profiling data into a file:

        perfbucket export REQUEST-UUID > profile.xhprof_testing

* Install the Cassandra schema:

        perfbucket init
