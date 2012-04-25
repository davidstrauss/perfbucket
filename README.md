# perfbucket

## Setup on Fedora 16

1. Add the DataStax repository to /etc/yum.repos.d/datastax.repo:

        [datastax]
        name=DataStax Repo for Apache Cassandra
        baseurl=http://rpm.datastax.com/community
        enabled=1
        gpgcheck=0

1. Add the perfbucket service to /etc/systemd/system/perfbucket-watcher.service:

        [Unit]
        After=network.target

        [Service]
        TimeoutSec=90s
        User=apache
        Group=apache
        ExecStart=/usr/bin/python /opt/perfbucket/watcher.py /var/tmp/perfbucket
        Restart=on-failure
        RestartSec=5min

        [Install]
        WantedBy=multi-user.target

1. Set up the Python side:

        yum install -y apache-cassandra1 python-pip gcc python-devel git
        pip-python install git+http://github.com/davidstrauss/perfbucket.git#egg=perfbucket
        systemctl enable cassandra.service perfbucket-watcher.service
        systemctl start cassandra.service perfbucket-watcher.service

1. Use schema.py in the installed package to configure Cassandra.

1. Set up the PHP side:

        yum install -y httpd mysql mysql-server php php-mysql php-devel php-pear php-pecl-apc
        pecl install channel://pecl.php.net/xhprof-0.9.2
        echo "extension=xhprof.so" > /etc/php.d/xhprof.ini
        systemctl enable httpd.service mysqld.service
        systemctl start httpd.service mysqld.service

1. Use the files in the "php" directory as a guide for having all PHP runs send profiling information to perfbucket.
