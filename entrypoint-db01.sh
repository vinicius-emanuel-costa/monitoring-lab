#!/bin/bash
set -e

# MariaDB
chown -R mysql:mysql /var/lib/mysql /var/run/mysqld 2>/dev/null
mkdir -p /var/run/mysqld && chown mysql:mysql /var/run/mysqld
/etc/init.d/mariadb start
sleep 2

# Node Exporter
if [ -f /usr/local/bin/node_exporter ]; then
    /usr/local/bin/node_exporter &>/var/log/node_exporter.log &
fi

# MySQL Exporter
if [ -f /usr/local/bin/mysqld_exporter ]; then
    /usr/local/bin/mysqld_exporter \
        --config.my-cnf=/etc/.mysqld_exporter.cnf \
        &>/var/log/mysqld_exporter.log &
fi

# Zabbix Agent
mkdir -p /var/run/zabbix && chown zabbix:zabbix /var/run/zabbix 2>/dev/null
/etc/init.d/zabbix-agent start 2>/dev/null || true

# SSH
mkdir -p /run/sshd
/usr/sbin/sshd -D
