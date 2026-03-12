#!/bin/bash
set -e

# PHP-FPM
/etc/init.d/php8.1-fpm start 2>/dev/null || true

# LiteSpeed
if [ -f /usr/local/lsws/bin/lswsctrl ]; then
    /usr/local/lsws/bin/lswsctrl start
elif [ -f /usr/local/lsws/bin/litespeed ]; then
    /usr/local/lsws/bin/litespeed start
fi

# Exim4
/etc/init.d/exim4 start 2>/dev/null || true

# Cron
/etc/init.d/cron start 2>/dev/null || true

# Node Exporter
if [ -f /usr/local/bin/node_exporter ]; then
    /usr/local/bin/node_exporter &>/var/log/node_exporter.log &
fi

# Zabbix Agent
mkdir -p /var/run/zabbix && chown zabbix:zabbix /var/run/zabbix 2>/dev/null
/etc/init.d/zabbix-agent start 2>/dev/null || true

# SSH
mkdir -p /run/sshd
/usr/sbin/sshd -D
