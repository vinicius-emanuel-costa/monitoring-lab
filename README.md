# Monitoring Lab

![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker&logoColor=white)
![Prometheus](https://img.shields.io/badge/Prometheus-E6522C?logo=prometheus&logoColor=white)
![Grafana](https://img.shields.io/badge/Grafana-F46800?logo=grafana&logoColor=white)
![Zabbix](https://img.shields.io/badge/Zabbix-CC0000?logo=zabbix&logoColor=white)
![OpenSearch](https://img.shields.io/badge/OpenSearch-005EB8?logo=opensearch&logoColor=white)
![Kubernetes](https://img.shields.io/badge/K3s-FFC61C?logo=kubernetes&logoColor=black)
![Ubuntu](https://img.shields.io/badge/Ubuntu_22.04-E95420?logo=ubuntu&logoColor=white)

Stack completa de observabilidade rodando em Docker Compose. Construida para pratica hands-on com ferramentas enterprise de monitoramento, logging e alertas em um unico ambiente de laboratorio.

## Arquitetura

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
    │ alertmanager  │     │              Pipeline de Logs                       │
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

## Servicos

| Servico | Container | IP | Portas | Descricao |
|---|---|---|---|---|
| **mon01** | lab-mon01 | 10.10.10.40 | 3000, 9090, 8080, 9115, 2240 | Prometheus + Grafana + Zabbix + Blackbox Exporter |
| **web01** | lab-web01 | 10.10.10.10 | 8088, 7080, 2210 | Servidor web LiteSpeed + PHP-FPM |
| **db01** | lab-db01 | 10.10.10.20 | 3306, 2220 | Servidor de banco de dados MariaDB |
| **bkp01** | lab-bkp01 | 10.10.10.30 | 2230 | Servidor de backup (rsync + cron) |
| **alertmanager** | lab-alertmanager | 10.10.10.41 | 9093 | Prometheus Alertmanager |
| **node-exporter** | lab-node-exporter | 10.10.10.42 | 9100 | Exportador de metricas do host |
| **opensearch** | lab-opensearch | 10.10.10.45 | 9200 | OpenSearch 2.12 (armazenamento de logs) |
| **opensearch-dash** | lab-opensearch-dash | 10.10.10.46 | 5601 | OpenSearch Dashboards |
| **logstash** | lab-logstash | 10.10.10.44 | 5044 | Pipeline de processamento de logs |
| **fluent-bit** | lab-fluentbit | 10.10.10.43 | — | Coletor de logs (logs de containers Docker) |
| **proxmox-mock** | lab-proxmox-mock | 10.10.10.47 | 8006 | Simulador da API Proxmox VE (Flask) |
| **k3s** | lab-k3s | 10.10.10.48 | 6443 | Kubernetes leve (K3s) |

## Como Usar

### Pre-requisitos

- Docker Engine 20.10+
- Docker Compose v2+
- Minimo de 8 GB de RAM recomendado

### 1. Clonar e configurar

```bash
git clone https://github.com/Vinicius-Costa14/monitoring-lab.git
cd monitoring-lab
cp .env.example .env
# Edite o .env e defina suas senhas
```

### 2. Buildar as imagens customizadas

```bash
docker build -t monitoring-lab/mon01:v1 dockerfiles/mon01/
docker build -t monitoring-lab/web01:v1 dockerfiles/web01/
docker build -t monitoring-lab/db01:v1 dockerfiles/db01/
docker build -t monitoring-lab/bkp01:v1 dockerfiles/bkp01/
docker build -t monitoring-lab/proxmox-mock:v1 config/proxmox-mock/
```

### 3. Subir a stack

```bash
docker compose up -d
```

### 4. Acessar os servicos

| Servico | URL |
|---|---|
| Grafana | http://localhost:3000 |
| Prometheus | http://localhost:9090 |
| Zabbix Frontend | http://localhost:8080 |
| OpenSearch Dashboards | http://localhost:5601 |
| LiteSpeed | http://localhost:8088 |
| LiteSpeed Admin | https://localhost:7080 |
| Alertmanager | http://localhost:9093 |
| Proxmox Mock API | https://localhost:8006 |

## Topologia de Rede

Todos os servicos rodam em uma rede Docker bridge `lab-internal` com subnet **10.10.10.0/24**.

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

## Pipeline de Logs

```
Docker containers → Fluent Bit → Logstash → OpenSearch → OpenSearch Dashboards
```

Fluent Bit coleta os logs dos containers Docker, encaminha para o Logstash para processamento, que entao indexa no OpenSearch. Visualize e consulte os logs pelo OpenSearch Dashboards na porta 5601.

## Estrutura do Projeto

```
monitoring-lab/
├── docker-compose.yml          # Definicao principal da stack (14 servicos)
├── .env.example                # Template de variaveis de ambiente
├── entrypoint-mon01.sh         # Startup do mon01 (MariaDB, Apache, Zabbix, Prometheus, Grafana)
├── entrypoint-web01.sh         # Startup do web01 (PHP-FPM, LiteSpeed, Exim4)
├── entrypoint-db01.sh          # Startup do db01 (MariaDB, MySQL Exporter)
├── entrypoint-bkp01.sh         # Startup do bkp01 (cron, rsync)
├── 01-commit-containers.sh     # Helper: commit de containers rodando como imagens
├── dockerfiles/
│   ├── mon01/Dockerfile        # Ubuntu 22.04 + MariaDB + Apache + PHP + deps Zabbix
│   ├── web01/Dockerfile        # Ubuntu 22.04 + PHP-FPM + ferramentas de sistema
│   ├── db01/Dockerfile         # Ubuntu 22.04 + MariaDB
│   └── bkp01/Dockerfile        # Ubuntu 22.04 + cron + rsync
└── config/
    ├── alertmanager/alertmanager.yml
    ├── fluentbit/fluent-bit.conf
    ├── logstash/pipeline/logstash.conf
    ├── proxmox-mock/
    │   ├── Dockerfile
    │   └── app.py              # API Flask simulando Proxmox VE
    └── k3s/                    # K3s kubeconfig (gerado em runtime)
```

## Tecnologias

- **Monitoramento**: Prometheus, Grafana, Zabbix, Blackbox Exporter, Node Exporter, MySQL Exporter
- **Alertas**: Alertmanager
- **Logging**: Fluent Bit, Logstash, OpenSearch, OpenSearch Dashboards
- **Web**: LiteSpeed, PHP-FPM
- **Banco de dados**: MariaDB
- **Containers**: Docker Compose, K3s (Kubernetes)
- **Simulacao de virtualizacao**: Simulador de API Proxmox VE (Flask + Python)
- **SO base**: Ubuntu 22.04 (containers customizados)

## Licenca

Este projeto e para fins educacionais e de laboratorio.
