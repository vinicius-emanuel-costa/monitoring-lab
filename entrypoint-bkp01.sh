#!/bin/bash
set -e

/etc/init.d/cron start 2>/dev/null || true
/etc/init.d/rsync start 2>/dev/null || true

if [ -f /usr/local/bin/node_exporter ]; then
    /usr/local/bin/node_exporter &>/var/log/node_exporter.log &
fi

mkdir -p /var/run/zabbix && chown zabbix:zabbix /var/run/zabbix 2>/dev/null
/etc/init.d/zabbix-agent start 2>/dev/null || true

mkdir -p /run/sshd
/usr/sbin/sshd -D
