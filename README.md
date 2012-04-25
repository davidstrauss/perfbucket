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
        ExecStart=/usr/bin/python /opt/perfbucket/watcher.py
        Restart=on-failure
        RestartSec=5min

        [Install]
        WantedBy=multi-user.target

1. Finish setup:

        yum upgrade -y
        yum install -y httpd mysql mysql-server php php-mysql php-devel php-pear php-pecl-apc
        yum install -y apache-cassandra1 python-pip gcc python-devel git
        pip-python install git+http://github.com/davidstrauss/perfbucket.git#egg=perfbucket
        pecl install channel://pecl.php.net/xhprof-0.9.2
        echo "extension=xhprof.so" > /etc/php.d/xhprof.ini
        systemctl enable httpd.service mysqld.service cassandra.service perfbucket-watcher.service

1. Ensure all the updates take effect:

        reboot

## Using with Drupal
