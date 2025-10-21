# 🚀 Self-Healing Infrastructure with Prometheus, Alertmanager & Ansible

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=flat&logo=docker&logoColor=white)](https://www.docker.com/)
[![Prometheus](https://img.shields.io/badge/Prometheus-E6522C?style=flat&logo=Prometheus&logoColor=white)](https://prometheus.io/)
[![Ansible](https://img.shields.io/badge/ansible-%231A1918.svg?style=flat&logo=ansible&logoColor=white)](https://www.ansible.com/)

A complete self-healing infrastructure project that automatically detects service failures and recovers them using monitoring alerts and automation. This production-ready solution demonstrates DevOps best practices for building resilient, self-managing systems.

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
- **Linux** (Ubuntu 20.04+ / Debian 11+ / CentOS 8+ / RHEL 8+)
- **Docker** (v20.10+)
- **Docker Compose** (v2.0+)
- **Bash** shell
- **curl** (for health checks)
- **Git** (for cloning repository)
- **sudo** access (for Docker operations)

### 1. Clone and Setup
```bash
git clone https://github.com/rushiphalke247/Self-healing-Project.git
cd Self-healing-Project
```

### 2. Start the Infrastructure
```bash
# Make script executable and start
chmod +x start.sh
./start.sh
```

**Alternative Manual Start:**
```bash
# Build and start all services
docker-compose up --build -d
```

### 3. Verify Deployment
After startup, all services should be accessible:
- **🔍 Prometheus**: http://localhost:9090
- **📢 Alertmanager**: http://localhost:9093
- **🌐 NGINX Demo**: http://localhost
- **📡 Node Exporter**: http://localhost:9100
- **🔗 Webhook Health**: http://localhost:5000/health

### 4. Test Auto-Healing
```bash
# Test 1: Stop NGINX service
docker stop nginx
# Expected: Service automatically restarts within 30 seconds 

# Test 2: Watch healing in action
docker-compose logs -f webhook

# Test 3: Verify service recovery
curl http://localhost/
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
Self-healing-Project/
├── 📁 .vscode/             # VS Code development settings
│   └── tasks.json          # Automated tasks (dev only)
├── 📁 .github/             # GitHub configuration
│   └── copilot-instructions.md
├── 📁 prometheus/          # 🔍 Monitoring configuration
│   ├── prometheus.yml      # Main Prometheus config
│   └── alert_rules.yml     # Alert definitions & thresholds
├── 📁 alertmanager/        # 📢 Alert management
│   └── alertmanager.yml    # Routing and webhook config
├── 📁 ansible/             # 🔧 Automation playbooks
│   ├── heal-nginx.yml      # Service healing automation
│   └── system-recovery.yml # System-wide recovery
├── 📁 webhook/             # 🔗 Webhook microservice
│   ├── webhook_handler.py  # Flask webhook application
│   ├── requirements.txt    # Python dependencies
│   └── Dockerfile          # Container image definition
├── 📁 services/            # 🌐 Sample services
│   ├── nginx.conf          # NGINX configuration
│   └── index.html          # Demo status page
├── docker-compose.yml      # 🐳 Container orchestration
├── start.sh               # 🐧 Linux/macOS startup script
└── README.md              # 📖 Project documentation
```

## 🛠️ VS Code Integration

This project includes VS Code tasks for easy development and testing:

**Available Tasks** (`Ctrl+Shift+P` → "Tasks: Run Task"):
- **🚀 Start Self-Healing Infrastructure**: Launch complete stack
- **🛑 Stop Infrastructure**: Gracefully stop all services
- **📊 View Infrastructure Logs**: Real-time log monitoring
- **🧪 Test Auto-Healing**: Simulate NGINX failure
- **📋 Check Service Status**: Container health overview

**Note**: `.vscode/` folder is for development only and not needed for production deployments.

## 🚀 Deployment Options

### 🐳 Local Development (Docker)
```bash
# Quick start with startup script
chmod +x start.sh
./start.sh

# Or manually
docker-compose up --build -d
```

### ☁️ Cloud Deployment

#### AWS EC2 / Google Cloud Compute / Azure VM
```bash
# 1. Provision Linux VM (Ubuntu 20.04+ recommended) with Docker installed
# 2. Clone repository
git clone --depth 1 https://github.com/rushiphalke247/Self-healing-Project.git
cd Self-healing-Project

# 3. Start services
chmod +x start.sh
./start.sh

# 4. Configure firewall (open ports: 80, 9090, 9093, 5000)
```

#### Kubernetes Deployment
```bash
# Convert docker-compose to k8s manifests
kompose convert

# Deploy to cluster
kubectl apply -f .
```

#### Docker Swarm
```bash
# Initialize swarm
docker swarm init

# Deploy stack
docker stack deploy -c docker-compose.yml monitoring
```

### 🔐 Production Considerations

#### Security Hardening
- Change default webhook credentials in `alertmanager.yml`
- Use TLS/SSL certificates for external access
- Implement proper firewall rules (UFW/iptables)
- Use secrets management for sensitive data
- Configure SELinux/AppArmor policies 
- Restrict Docker daemon access

#### Scaling & Performance
- Add load balancers (HAProxy/NGINX) for high availability
- Use persistent volumes for data retention
- Configure systemd service units for auto-start
- Implement log rotation with logrotate
- Configure resource limits in docker-compose.yml
- Implement log rotation policies

#### Monitoring Extensions
- Add more exporters (Redis, PostgreSQL, etc.)
- Integrate with external alerting (Slack, PagerDuty)
- Implement custom metrics for your applications
- Set up long-term storage (Thanos, Cortex)

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

### 4. Complete System Test
```bash
# Run comprehensive test suite
./start.sh

# Wait for all services to be ready
sleep 60

# Test each component
curl http://localhost:9090/-/healthy    # Prometheus
curl http://localhost:9093/-/healthy    # Alertmanager  
curl http://localhost/                  # NGINX
curl http://localhost:5000/health       # Webhook

# Test auto-healing
docker stop nginx
sleep 45
docker ps | grep nginx                  # Should show running
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

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

### Development Guidelines
- Follow existing code style and conventions
- Add tests for new features
- Update documentation as needed
- Ensure all containers build successfully
- Test the startup script on different Linux distributions

### Reporting Issues
Please use GitHub Issues to report bugs or request features. Include:
- Detailed description of the problem
- Steps to reproduce
- Expected vs actual behavior
- Environment details (OS, Docker version, etc.)

## 🌟 Roadmap

- [ ] **Grafana Integration**: Visual dashboards for metrics
- [ ] **Multi-Cloud Support**: AWS, GCP, Azure deployment guides
- [ ] **Kubernetes Helm Charts**: Easy k8s deployment
- [ ] **Additional Services**: Redis, PostgreSQL monitoring examples
- [ ] **CI/CD Pipeline**: GitHub Actions workflow
- [ ] **Security Scanning**: Container vulnerability checks
- [ ] **Performance Testing**: Load testing automation
- [ ] **Documentation**: Video tutorials and blog posts

## 🙏 Acknowledgments

- **Prometheus Community** for excellent monitoring tools
- **Ansible Community** for powerful automation platform
- **Docker Team** for containerization technology
- **Open Source Contributors** who make projects like this possible

## 📊 Project Stats

- **Components**: 6 microservices
- **Technologies**: Docker, Prometheus, Ansible, Python, NGINX
- **Deployment Time**: < 2 minutes
- **Recovery Time**: < 30 seconds
- **Platforms**: Linux, macOS, Cloud
