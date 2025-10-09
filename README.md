# 🚀 Self-Healing Infrastructure with Prometheus, Alertmanager & Ansible

A complete self-healing infrastructure project that automatically detects service failures and recovers them using monitoring alerts and automation.

## 🎯 Project Overview

This project demonstrates a robust self-healing infrastructure system that:
- **Monitors** services using Prometheus
- **Detects** failures and performance issues through alerts
- **Responds** automatically via Alertmanager webhooks
- **Heals** problems using Ansible automation playbooks

## 🏗️ Architecture

```
┌─────────────┐    ┌──────────────┐    ┌─────────────┐    ┌─────────────┐
│   Service   │    │  Prometheus  │    │ Alertmanager│    │   Webhook   │
│   (NGINX)   │◄───┤  Monitoring  │────┤   Alerts    │────┤   Handler   │
└─────────────┘    └──────────────┘    └─────────────┘    └─────────────┘
       ▲                                                          │
       │                                                          ▼
       │                                                   ┌─────────────┐
       └───────────────────────────────────────────────────┤   Ansible   │
                              Self-Healing                 │  Playbooks  │
                                                          └─────────────┘
```

## 📋 Components

### 🔍 Monitoring Stack
- **Prometheus**: Metrics collection and alerting rules
- **Node Exporter**: System metrics (CPU, memory, disk)
- **NGINX Exporter**: Web server metrics
- **Alertmanager**: Alert routing and notifications

### 🔧 Automation Stack  
- **Webhook Service**: Python Flask app receiving alerts
- **Ansible Playbooks**: Automated recovery scripts
- **Docker Compose**: Container orchestration

### 🎯 Sample Service
- **NGINX**: Web server being monitored
- **Demo Page**: Visual status dashboard

## 🚀 Quick Start

### Prerequisites
- Docker Desktop
- Docker Compose
- PowerShell (Windows) or Bash (Linux/Mac)

### 1. Start the Infrastructure
```
# Linux/Mac 
./start.sh
```

### 2. Access the Dashboards
- **Prometheus**: http://localhost:9090
- **Alertmanager**: http://localhost:9093
- **NGINX Demo**: http://localhost
- **Webhook Health**: http://localhost:5000/health

### 3. Test Auto-Healing
```bash
# Stop NGINX to trigger healing
docker stop nginx

# Watch the webhook logs
docker-compose logs -f webhook

# NGINX should automatically restart!
```

## 📊 Monitoring Capabilities

### Alert Rules
| Alert | Trigger | Severity | Action |
|-------|---------|----------|--------|
| `NginxDown` | Service stops | Critical | Restart service |
| `NginxHighCPU` | CPU > 90% | Warning | System recovery |
| `NginxHighMemory` | Memory > 80% | Warning | Cache cleanup |
| `NginxServiceUnhealthy` | Health check fails | Critical | Service restart |

### Metrics Collected
- **System**: CPU, memory, disk usage
- **Network**: Connection counts, response times  
- **Application**: NGINX request rates, error rates
- **Custom**: Service health checks

## 🔧 Auto-Healing Actions

### Service Recovery (`heal-nginx.yml`)
1. Check service status
2. Restart if down
3. Verify health endpoint
4. Log healing action
5. Send notifications

### System Recovery (`system-recovery.yml`)
1. Monitor resource usage
2. Kill high-resource processes
3. Clear system caches
4. Restart problematic services
5. Log recovery actions

## 📁 Project Structure

```
self-healing-infrastructure/
├── 📁 prometheus/          # Monitoring configuration
│   ├── prometheus.yml      # Main Prometheus config
│   └── alert_rules.yml     # Alert definitions
├── 📁 alertmanager/        # Alert management
│   └── alertmanager.yml    # Routing and notifications
├── 📁 ansible/             # Automation playbooks
│   ├── heal-nginx.yml      # Service healing
│   └── system-recovery.yml # System recovery
├── 📁 webhook/             # Webhook service
│   ├── webhook_handler.py  # Flask webhook app
│   ├── requirements.txt    # Python dependencies
│   └── Dockerfile          # Container image
├── 📁 services/            # Sample services
│   ├── nginx.conf          # NGINX configuration
│   └── index.html          # Demo webpage
├── 📁 .vscode/             # VS Code tasks
│   └── tasks.json          # Build and test tasks
├── docker-compose.yml      # Container orchestration
├── start.sh               # Linux/Mac startup script
└── README.md              # This file
```
## 🧪 Testing Scenarios

### 1. Service Failure Recovery
```bash
# Stop the NGINX service
docker stop nginx

# Expected: Service automatically restarts within 30 seconds
# Check: docker ps shows nginx running again
```

### 2. High Resource Usage
```bash
# Simulate high CPU (inside container)
docker exec nginx sh -c "yes > /dev/null &"

# Expected: System recovery triggers, process killed
```

### 3. Memory Pressure
```bash
# The system monitors memory usage and cleans caches automatically
# when usage exceeds 80%
```

## 📈 Monitoring Dashboard Queries

### Prometheus Queries
```promql
# Service uptime
up{job="nginx"}

# CPU usage
100 - (avg by(instance) (rate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)

# Memory usage  
(node_memory_MemTotal_bytes - node_memory_MemFree_bytes) / node_memory_MemTotal_bytes * 100

# NGINX requests per second
rate(nginx_http_requests_total[5m])
```

## 🔧 Configuration

### Adjusting Alert Thresholds
Edit `prometheus/alert_rules.yml`:
```yaml
- alert: NginxHighCPU
  expr: cpu_usage > 80  # Change from 90 to 80
  for: 1m              # Change from 2m to 1m
```

### Adding New Services
1. Add monitoring target to `prometheus/prometheus.yml`
2. Create alert rules in `prometheus/alert_rules.yml`  
3. Add healing playbook in `ansible/`
4. Update webhook mapping in `webhook/webhook_handler.py`

### Customizing Recovery Actions
Edit Ansible playbooks in `ansible/` directory:
- `heal-nginx.yml`: Service-specific recovery
- `system-recovery.yml`: System-wide recovery

## 🔒 Security Considerations

- Webhook endpoint uses basic authentication
- Containers run with non-root users where possible
- Network isolation via Docker networks
- Log file permissions restricted

## 📋 Troubleshooting

### Common Issues

**Services not starting:**
```bash
# Check Docker status
docker info

# Check container logs
docker-compose logs [service-name]
```

**Alerts not firing:**
```bash
# Check Prometheus targets
curl http://localhost:9090/api/v1/targets

# Check alert rules
curl http://localhost:9090/api/v1/rules
```

**Webhook not receiving alerts:**
```bash
# Check Alertmanager config
curl http://localhost:9093/api/v1/status

# Test webhook directly
curl -X POST http://localhost:5000/webhook -H "Content-Type: application/json" -d '{}'
```

## 📚 Learning Resources

- [Prometheus Documentation](https://prometheus.io/docs/)
- [Alertmanager Guide](https://prometheus.io/docs/alerting/latest/alertmanager/)
- [Ansible Playbooks](https://docs.ansible.com/ansible/latest/user_guide/playbooks.html)
- [Docker Compose Reference](https://docs.docker.com/compose/)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add your improvements
4. Test thoroughly
5. Submit a pull request

## 📄 License

MIT License - feel free to use this project for learning and production deployments.

---

**🎉 Happy Monitoring and Auto-Healing!** 


This project demonstrates the power of combining monitoring, alerting, and automation to create resilient infrastructure that can heal itself when problems occur.
