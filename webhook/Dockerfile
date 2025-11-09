FROM python:3.11-slim

# -------------------------------------------------------
# 1. Install system dependencies and Docker CLI
# -------------------------------------------------------
RUN apt-get update && apt-get install -y \
    ansible \
    curl \
    docker.io \
    docker-compose \
    python3-dev \
    gcc \
    libffi-dev \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# -------------------------------------------------------
# 2. Set working directory
# -------------------------------------------------------
WORKDIR /app

# -------------------------------------------------------
# 3. Copy Python dependencies and install
# -------------------------------------------------------
COPY requirements.txt .

# Install all Python dependencies + Docker SDK + Unix socket support
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir \
        docker[ssh]==7.1.0 \
        requests \
        urllib3 \
        requests-unixsocket \
        ansible \
        --upgrade

# -------------------------------------------------------
# 4. Copy the application code
# -------------------------------------------------------
COPY webhook_handler.py .

# -------------------------------------------------------
# 5. Create log directory and set permissions
# -------------------------------------------------------
RUN mkdir -p /app/logs /var/log && \
    chmod -R 777 /app/logs /var/log

# -------------------------------------------------------
# 6. Create non-root user and give Docker socket permissions
# -------------------------------------------------------
RUN useradd -m webhook && \
    usermod -aG docker webhook && \
    chmod 777 /var/run/docker.sock || true && \
    chown -R webhook:webhook /app /var/log

# -------------------------------------------------------
# 7. Install Ansible Docker collection
# -------------------------------------------------------
RUN ansible-galaxy collection install community.docker --force

# -------------------------------------------------------
# 8. Set environment variables
# -------------------------------------------------------
ENV LOG_DIR=/app/logs
ENV DOCKER_HOST=unix:///var/run/docker.sock
ENV FLASK_ENV=production

# -------------------------------------------------------
# 9. Expose port for Flask/Gunicorn
# -------------------------------------------------------
EXPOSE 5000

# -------------------------------------------------------
# 10. Switch to non-root user
# -------------------------------------------------------
USER webhook

# -------------------------------------------------------
# 11. Run the application with Gunicorn
# -------------------------------------------------------
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "webhook_handler:app"]

