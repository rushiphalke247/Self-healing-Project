# Changelog

All notable changes to the Self-Healing Infrastructure project will be documented in this file.

## [1.1.0] - 2025-10-21

### Added
- **Windows Support**: Added `start.ps1` PowerShell script for Windows users
- **Docker Volume**: Created dedicated `webhook_logs` volume for cross-platform log storage
- **Python Dependencies**: Added missing `docker` and `ansible` packages to requirements.txt

### Changed
- **Cross-platform Compatibility**: Replaced hardcoded `/home/ec2-user` path with Docker volume
- **Webhook Service**: Removed redundant CMD override in docker-compose.yml (now uses Dockerfile CMD)
- **Documentation**: Updated README with Windows-specific instructions and prerequisites

### Fixed
- **Volume Mounts**: Fixed platform-specific path issues in docker-compose.yml
- **Dependencies**: Added missing Python packages required by Ansible playbooks
- **Service Startup**: Corrected webhook service configuration to use proper entrypoint

### Technical Details
- Changed log volume from host bind mount to named Docker volume for portability
- Updated README.md with separate instructions for Windows/Linux/macOS platforms
- Ensured Dockerfile CMD is used instead of being overridden in docker-compose.yml

## [1.0.0] - Initial Release

### Features
- Prometheus monitoring stack with 4 exporters
- Alertmanager integration with webhook routing
- Python Flask webhook service for alert processing
- 5 Ansible playbooks for automated healing
- Docker Compose orchestration for all services
- NGINX sample service with health monitoring
- Comprehensive alert rules for service monitoring
- Self-healing automation for service failures

