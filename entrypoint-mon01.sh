#!/bin/bash
set -e

# MariaDB (Zabbix database)
if [ -d /var/lib/mysql ]; then
    chown -R mysql:mysql /var/lib/mysql /var/run/mysqld 2>/dev/null
    mkdir -p /var/run/mysqld && chown mysql:mysql /var/run/mysqld
    /etc/init.d/mariadb start
    sleep 2
fi

# Apache + Zabbix Frontend
/etc/init.d/apache2 start

# Zabbix Server
mkdir -p /var/run/zabbix && chown zabbix:zabbix /var/run/zabbix
/etc/init.d/zabbix-server start

# Zabbix Agent
/etc/init.d/zabbix-agent start

# Prometheus
if [ -f /usr/local/bin/prometheus ]; then
    /usr/local/bin/prometheus \
        --config.file=/etc/prometheus/prometheus.yml \
        --storage.tsdb.path=/var/lib/prometheus \
        &>/var/log/prometheus.log &
fi

# Blackbox Exporter
if [ -f /usr/local/bin/blackbox_exporter ]; then
    /usr/local/bin/blackbox_exporter \
        --config.file=/etc/blackbox/blackbox.yml \
        &>/var/log/blackbox.log &
fi

# Grafana
if [ -f /opt/grafana/bin/grafana ]; then
    cd /opt/grafana
    /opt/grafana/bin/grafana server \
        --homepath=/opt/grafana \
        --config=/opt/grafana/conf/custom.ini \
        &>/var/log/grafana.log &
fi

# SSH
mkdir -p /run/sshd
/usr/sbin/sshd -D
