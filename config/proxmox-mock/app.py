from flask import Flask, jsonify, request
import random, time

app = Flask(__name__)

@app.route('/api2/json/access/ticket', methods=['POST'])
def login():
    return jsonify({"data": {"ticket": "PVE:mock:FAKTICKET", "CSRFPreventionToken": "FAKECSRF"}})

@app.route('/api2/json/version', methods=['GET'])
def version():
    return jsonify({"data": {"version": "7.0.0", "release": "1", "repoid": "mock"}})

@app.route('/api2/json/nodes', methods=['GET'])
def nodes():
    return jsonify({"data": [
        {"node": "pve-mock", "status": "online", "type": "node",
         "cpu": round(random.uniform(0.05, 0.60), 4), "maxcpu": 8,
         "mem": random.randint(4000000000, 10000000000), "maxmem": 16000000000,
         "disk": random.randint(20000000000, 40000000000), "maxdisk": 100000000000,
         "uptime": int(time.time()) - 86400}
    ]})

@app.route('/api2/json/nodes/<node>/status', methods=['GET'])
def node_status(node):
    return jsonify({"data": {
        "cpu": round(random.uniform(0.05, 0.60), 4),
        "cpuinfo": {"cpus": 8, "model": "Intel Mock CPU"},
        "memory": {"used": random.randint(4000000000, 10000000000), "total": 16000000000},
        "swap": {"used": 0, "total": 2000000000},
        "rootfs": {"used": random.randint(20000000000, 40000000000), "total": 100000000000},
        "uptime": int(time.time()) - 86400,
        "loadavg": [round(random.uniform(0.1, 1.5), 2)] * 3,
        "kversion": "Linux 6.2.0-mock-pve", "pveversion": "pve-manager/7.0.0/mock"
    }})

@app.route('/api2/json/nodes/<node>/qemu', methods=['GET'])
def vms(node):
    return jsonify({"data": [
        {"vmid": 100, "name": "vm-web", "status": "running", "cpu": round(random.uniform(0.01, 0.3), 4), "mem": 1073741824, "maxmem": 2147483648, "uptime": 3600},
        {"vmid": 101, "name": "vm-db", "status": "running", "cpu": round(random.uniform(0.01, 0.3), 4), "mem": 2147483648, "maxmem": 4294967296, "uptime": 7200},
        {"vmid": 102, "name": "vm-app", "status": "stopped", "cpu": 0, "mem": 0, "maxmem": 2147483648, "uptime": 0},
    ]})

@app.route('/api2/json/nodes/<node>/lxc', methods=['GET'])
def lxc(node):
    return jsonify({"data": [
        {"vmid": 200, "name": "ct-nginx", "status": "running", "cpu": round(random.uniform(0.01, 0.1), 4), "mem": 536870912, "maxmem": 1073741824, "uptime": 1800},
        {"vmid": 201, "name": "ct-redis", "status": "running", "cpu": round(random.uniform(0.01, 0.1), 4), "mem": 268435456, "maxmem": 536870912, "uptime": 900},
    ]})

@app.route('/api2/json/nodes/<node>/storage', methods=['GET'])
def storage(node):
    return jsonify({"data": [
        {"storage": "local", "type": "dir", "active": 1, "used": random.randint(20000000000, 40000000000), "total": 100000000000, "avail": 60000000000},
        {"storage": "local-lvm", "type": "lvmthin", "active": 1, "used": random.randint(10000000000, 30000000000), "total": 50000000000, "avail": 20000000000},
    ]})

@app.route('/api2/json/nodes/<node>/network', methods=['GET'])
def network(node):
    return jsonify({"data": [
        {"iface": "eth0", "type": "eth", "active": 1, "address": "192.168.1.100", "netmask": "255.255.255.0"},
        {"iface": "vmbr0", "type": "bridge", "active": 1, "address": "10.10.10.1", "netmask": "255.255.255.0"},
    ]})

@app.route('/api2/json/cluster/resources', methods=['GET'])
def cluster_resources():
    return jsonify({"data": [
        {"id": "node/pve-mock", "type": "node", "node": "pve-mock", "status": "online", "cpu": round(random.uniform(0.05, 0.60), 4), "maxcpu": 8, "mem": random.randint(4000000000, 10000000000), "maxmem": 16000000000},
        {"id": "qemu/100", "type": "qemu", "node": "pve-mock", "name": "vm-web", "status": "running", "vmid": 100, "cpu": round(random.uniform(0.01, 0.3), 4), "mem": 1073741824, "maxmem": 2147483648, "uptime": 3600},
        {"id": "qemu/101", "type": "qemu", "node": "pve-mock", "name": "vm-db", "status": "running", "vmid": 101, "cpu": round(random.uniform(0.01, 0.3), 4), "mem": 2147483648, "maxmem": 4294967296, "uptime": 7200},
        {"id": "qemu/102", "type": "qemu", "node": "pve-mock", "name": "vm-app", "status": "stopped", "vmid": 102, "cpu": 0, "mem": 0, "maxmem": 2147483648, "uptime": 0},
        {"id": "lxc/200", "type": "lxc", "node": "pve-mock", "name": "ct-nginx", "status": "running", "vmid": 200, "cpu": round(random.uniform(0.01, 0.1), 4), "mem": 536870912, "maxmem": 1073741824, "uptime": 1800},
        {"id": "lxc/201", "type": "lxc", "node": "pve-mock", "name": "ct-redis", "status": "running", "vmid": 201, "cpu": round(random.uniform(0.01, 0.1), 4), "mem": 268435456, "maxmem": 536870912, "uptime": 900},
        {"id": "storage/local", "type": "storage", "node": "pve-mock", "storage": "local", "status": "available", "disk": random.randint(20000000000, 40000000000), "maxdisk": 100000000000},
    ]})

@app.route('/api2/json/cluster/status', methods=['GET'])
def cluster_status():
    return jsonify({"data": [
        {"id": "cluster", "type": "cluster", "name": "mock-cluster", "quorate": 1, "nodes": 1, "version": 7},
        {"id": "node/pve-mock", "type": "node", "name": "pve-mock", "online": 1, "local": 1, "nodeid": 1}
    ]})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8006, ssl_context='adhoc')


@app.route('/api2/json/nodes/<node>/lxc/<vmid>/status/current', methods=['GET'])
def lxc_status(node, vmid):
    return jsonify({"data": {
        "vmid": int(vmid), "status": "running",
        "cpu": round(random.uniform(0.01, 0.1), 4),
        "mem": random.randint(200000000, 800000000), "maxmem": 1073741824,
        "disk": random.randint(1000000000, 3000000000), "maxdisk": 10000000000,
        "netin": random.randint(1000, 100000), "netout": random.randint(1000, 100000),
        "diskread": random.randint(1000, 50000), "diskwrite": random.randint(1000, 50000),
        "uptime": random.randint(3600, 86400)
    }})

@app.route('/api2/json/nodes/<node>/qemu/<vmid>/status/current', methods=['GET'])
def qemu_status(node, vmid):
    status = "stopped" if vmid == "102" else "running"
    return jsonify({"data": {
        "vmid": int(vmid), "status": status,
        "cpu": round(random.uniform(0.01, 0.3), 4) if status == "running" else 0,
        "mem": random.randint(500000000, 2000000000) if status == "running" else 0,
        "maxmem": 2147483648,
        "disk": random.randint(5000000000, 15000000000), "maxdisk": 32000000000,
        "netin": random.randint(1000, 100000), "netout": random.randint(1000, 100000),
        "diskread": random.randint(1000, 50000), "diskwrite": random.randint(1000, 50000),
        "uptime": random.randint(3600, 86400) if status == "running" else 0
    }})

@app.route('/api2/json/nodes/<node>/storage/<storage>/status', methods=['GET'])
def storage_status(node, storage):
    return jsonify({"data": {
        "storage": storage, "type": "dir", "active": 1,
        "used": random.randint(20000000000, 40000000000),
        "total": 100000000000,
        "avail": random.randint(50000000000, 70000000000)
    }})
