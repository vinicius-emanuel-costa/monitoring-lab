# Monitoring Lab

![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker&logoColor=white)
![Prometheus](https://img.shields.io/badge/Prometheus-E6522C?logo=prometheus&logoColor=white)
![Grafana](https://img.shields.io/badge/Grafana-F46800?logo=grafana&logoColor=white)
![Zabbix](https://img.shields.io/badge/Zabbix-CC0000?logo=zabbix&logoColor=white)
![OpenSearch](https://img.shields.io/badge/OpenSearch-005EB8?logo=opensearch&logoColor=white)
![Kubernetes](https://img.shields.io/badge/K3s-FFC61C?logo=kubernetes&logoColor=black)
![Ubuntu](https://img.shields.io/badge/Ubuntu_22.04-E95420?logo=ubuntu&logoColor=white)

Full observability stack running on Docker Compose. Built for hands-on practice with enterprise monitoring, logging, and alerting tools in a single lab environment.

## Architecture

```
                          ┌─────────────────────────────────────────────┐
                          │           Network: 10.10.10.0/24            │
                          └─────────────────────────────────────────────┘

    ┌──────────────┐     ┌──────────────┐     ┌──────────────┐     ┌──────────────┐
    │    mon01      │     │    web01      │     │    db01       │     │    bkp01      │
    │  10.10.10.40  │     │  10.10.10.10  │     │  10.10.10.20  │     │  10.10.10.30  │
    │               │     │               │     │               │     │               │
    │ - Prometheus  │     │ - LiteSpeed   │     │ - MariaDB     │     │ - Rsync       │
    │ - Grafana     │◄────│ - PHP-FPM     │     │ - MySQL Exp.  │     │ - Cron        │
    │ - Zabbix      │     │ - Node Exp.   │     │ - Node Exp.   │     │ - Node Exp.   │
    │ - Blackbox    │     │ - Zabbix Agt  │     │ - Zabbix Agt  │     │ - Zabbix Agt  │
    └──────┬───────┘     └──────────────┘     └──────────────┘     └──────────────┘
           │
    ┌──────┴───────┐     ┌──────────────────────────────────────────────────────┐
    │ alertmanager  │     │              Log Pipeline                            │
    │ 10.10.10.41   │     │                                                      │
    │ :9093         │     │  fluent-bit ──► logstash ──► opensearch              │
    └──────────────┘     │  .43            .44           .45                     │
                          │                                ▼                      │
                          │                          opensearch-dash              │
                          │                          .46  :5601                   │
                          └──────────────────────────────────────────────────────┘

    ┌──────────────┐     ┌──────────────┐     ┌──────────────┐
    │ node-exporter │     │ proxmox-mock  │     │     k3s       │
    │ 10.10.10.42   │     │ 10.10.10.47   │     │ 10.10.10.48   │
    │ :9100         │     │ :8006         │     │ :6443         │
    └──────────────┘     └──────────────┘     └──────────────┘
```

## Services

| Service | Container | IP | Ports | Description |
|---|---|---|---|---|
| **mon01** | lab-mon01 | 10.10.10.40 | 3000, 9090, 8080, 9115, 2240 | Prometheus + Grafana + Zabbix + Blackbox Exporter |
| **web01** | lab-web01 | 10.10.10.10 | 8088, 7080, 2210 | LiteSpeed + PHP-FPM web server |
| **db01** | lab-db01 | 10.10.10.20 | 3306, 2220 | MariaDB database server |
| **bkp01** | lab-bkp01 | 10.10.10.30 | 2230 | Backup server (rsync + cron) |
| **alertmanager** | lab-alertmanager | 10.10.10.41 | 9093 | Prometheus Alertmanager |
| **node-exporter** | lab-node-exporter | 10.10.10.42 | 9100 | Host metrics exporter |
| **opensearch** | lab-opensearch | 10.10.10.45 | 9200 | OpenSearch 2.12 (log storage) |
| **opensearch-dash** | lab-opensearch-dash | 10.10.10.46 | 5601 | OpenSearch Dashboards |
| **logstash** | lab-logstash | 10.10.10.44 | 5044 | Log processing pipeline |
| **fluent-bit** | lab-fluentbit | 10.10.10.43 | — | Log collector (Docker container logs) |
| **proxmox-mock** | lab-proxmox-mock | 10.10.10.47 | 8006 | Proxmox VE API simulator (Flask) |
| **k3s** | lab-k3s | 10.10.10.48 | 6443 | Lightweight Kubernetes (K3s) |

## Quick Start

### Prerequisites

- Docker Engine 20.10+
- Docker Compose v2+
- At least 8 GB RAM recommended

### 1. Clone and configure

```bash
git clone https://github.com/Vinicius-Costa14/monitoring-lab.git
cd monitoring-lab
cp .env.example .env
# Edit .env and set your passwords
```

### 2. Build custom images

```bash
docker build -t monitoring-lab/mon01:v1 dockerfiles/mon01/
docker build -t monitoring-lab/web01:v1 dockerfiles/web01/
docker build -t monitoring-lab/db01:v1 dockerfiles/db01/
docker build -t monitoring-lab/bkp01:v1 dockerfiles/bkp01/
docker build -t monitoring-lab/proxmox-mock:v1 config/proxmox-mock/
```

### 3. Start the stack

```bash
docker compose up -d
```

### 4. Access the services

| Service | URL |
|---|---|
| Grafana | http://localhost:3000 |
| Prometheus | http://localhost:9090 |
| Zabbix Frontend | http://localhost:8080 |
| OpenSearch Dashboards | http://localhost:5601 |
| LiteSpeed | http://localhost:8088 |
| LiteSpeed Admin | https://localhost:7080 |
| Alertmanager | http://localhost:9093 |
| Proxmox Mock API | https://localhost:8006 |

## Network Topology

All services run on a Docker bridge network `lab-internal` with subnet **10.10.10.0/24**.

```
Gateway:          10.10.10.1
web01:            10.10.10.10
db01:             10.10.10.20
bkp01:            10.10.10.30
mon01:            10.10.10.40
alertmanager:     10.10.10.41
node-exporter:    10.10.10.42
fluent-bit:       10.10.10.43
logstash:         10.10.10.44
opensearch:       10.10.10.45
opensearch-dash:  10.10.10.46
proxmox-mock:     10.10.10.47
k3s:              10.10.10.48
```

## Log Pipeline

```
Docker containers → Fluent Bit → Logstash → OpenSearch → OpenSearch Dashboards
```

Fluent Bit collects Docker container logs, forwards them to Logstash for processing, which then indexes them into OpenSearch. Visualize and query logs through OpenSearch Dashboards on port 5601.

## Project Structure

```
monitoring-lab/
├── docker-compose.yml          # Main stack definition (14 services)
├── .env.example                # Environment variables template
├── entrypoint-mon01.sh         # mon01 startup (MariaDB, Apache, Zabbix, Prometheus, Grafana)
├── entrypoint-web01.sh         # web01 startup (PHP-FPM, LiteSpeed, Exim4)
├── entrypoint-db01.sh          # db01 startup (MariaDB, MySQL Exporter)
├── entrypoint-bkp01.sh         # bkp01 startup (cron, rsync)
├── 01-commit-containers.sh     # Helper: commit running containers as images
├── dockerfiles/
│   ├── mon01/Dockerfile        # Ubuntu 22.04 + MariaDB + Apache + PHP + Zabbix deps
│   ├── web01/Dockerfile        # Ubuntu 22.04 + PHP-FPM + system tools
│   ├── db01/Dockerfile         # Ubuntu 22.04 + MariaDB
│   └── bkp01/Dockerfile        # Ubuntu 22.04 + cron + rsync
└── config/
    ├── alertmanager/alertmanager.yml
    ├── fluentbit/fluent-bit.conf
    ├── logstash/pipeline/logstash.conf
    ├── proxmox-mock/
    │   ├── Dockerfile
    │   └── app.py              # Flask API simulating Proxmox VE
    └── k3s/                    # K3s kubeconfig (generated at runtime)
```

## Technologies

- **Monitoring**: Prometheus, Grafana, Zabbix, Blackbox Exporter, Node Exporter, MySQL Exporter
- **Alerting**: Alertmanager
- **Logging**: Fluent Bit, Logstash, OpenSearch, OpenSearch Dashboards
- **Web**: LiteSpeed, PHP-FPM
- **Database**: MariaDB
- **Containers**: Docker Compose, K3s (Kubernetes)
- **Virtualization mock**: Proxmox VE API simulator (Flask + Python)
- **Base OS**: Ubuntu 22.04 (custom containers)

## License

This project is for educational and lab purposes.
