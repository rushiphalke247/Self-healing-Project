#!/usr/bin/env python3
"""
Webhook service to receive Alertmanager notifications and trigger Ansible playbooks
"""

import json
import logging
import subprocess
import os
from datetime import datetime
from flask import Flask, request, jsonify

app = Flask(__name__)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/app/logs/webhook.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# Mapping of alert names to Ansible playbooks (Docker-specific)
ALERT_PLAYBOOK_MAP = {
    'NginxDown': '/app/ansible/heal-nginx.yml',
    'NginxServiceUnhealthy': '/app/ansible/heal-nginx.yml',
    'NginxHighCPU': '/app/ansible/system-recovery.yml',
    'NginxHighMemory': '/app/ansible/system-recovery.yml',
    # Docker-specific alerts
    'ContainerDown': '/app/ansible/restart-container.yml',
    'StackUnhealthy': '/app/ansible/heal-docker-stack.yml'
}

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'service': 'webhook-handler'
    })

@app.route('/webhook', methods=['POST'])
def handle_webhook():
    """Handle incoming webhook from Alertmanager"""
    try:
        data = request.get_json()

        if not data:
            logger.error("No JSON data received")
            return jsonify({'error': 'No JSON data'}), 400

        logger.info(f"Received webhook: {json.dumps(data, indent=2)}")

        # Process each alert
        for alert in data.get('alerts', []):
            alert_name = alert.get('labels', {}).get('alertname')
            status = alert.get('status')

            logger.info(f"Processing alert: {alert_name} with status: {status}")

            # Only process firing alerts
            if status == 'firing' and alert_name in ALERT_PLAYBOOK_MAP:
                playbook_path = ALERT_PLAYBOOK_MAP[alert_name]
                success = execute_playbook(playbook_path, alert_name, alert)

                if success:
                    logger.info(f"Successfully executed healing for {alert_name}")
                else:
                    logger.error(f"Failed to execute healing for {alert_name}")

            elif status == 'resolved':
                logger.info(f"Alert {alert_name} has been resolved")

        return jsonify({
            'status': 'success',
            'message': 'Webhook processed successfully',
            'alerts_processed': len(data.get('alerts', []))
        })

    except Exception as e:
        logger.error(f"Error processing webhook: {str(e)}")
        return jsonify({'error': str(e)}), 500

def execute_playbook(playbook_path, alert_name, alert_data):
    """Execute Ansible playbook for healing"""
    try:
        # Check if playbook exists
        if not os.path.exists(playbook_path):
            logger.error(f"Playbook not found: {playbook_path}")
            return False

        # Prepare extra variables for Ansible
        extra_vars = {
            'alert_name': alert_name,
            'alert_instance': alert_data.get('labels', {}).get('instance', 'unknown'),
            'alert_severity': alert_data.get('labels', {}).get('severity', 'unknown')
        }

        # Build Ansible command
        cmd = [
            'ansible-playbook',
            playbook_path,
            '-i', 'localhost,',
            '--connection', 'local',
            '--extra-vars', json.dumps(extra_vars)
        ]

        logger.info(f"Executing command: {' '.join(cmd)}")

        # Execute playbook
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=300  # 5 minute timeout
        )

        if result.returncode == 0:
            logger.info(f"Playbook executed successfully: {result.stdout}")
            log_healing_action(alert_name, 'SUCCESS', result.stdout)
            return True
        else:
            logger.error(f"Playbook execution failed: {result.stderr}")
            log_healing_action(alert_name, 'FAILED', result.stderr)
            return False

    except subprocess.TimeoutExpired:
        logger.error(f"Playbook execution timed out for {alert_name}")
        log_healing_action(alert_name, 'TIMEOUT', 'Playbook execution timed out')
        return False
    except Exception as e:
        logger.error(f"Error executing playbook: {str(e)}")
        log_healing_action(alert_name, 'ERROR', str(e))
        return False

def log_healing_action(alert_name, status, details):
    """Log healing actions to file"""
    try:
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'alert_name': alert_name,
            'status': status,
            'details': details
        }

        with open('/app/logs/healing-actions.log', 'a') as f:
            f.write(json.dumps(log_entry) + '\n')

    except Exception as e:
        logger.error(f"Failed to log healing action: {str(e)}")

if __name__ == '__main__':
    logger.info("Starting webhook service...")
    app.run(host='0.0.0.0', port=5000, debug=False)
