FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    ansible \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY webhook_handler.py .

# Create log directory
RUN mkdir -p /var/log
RUN mkdir -p /app/logs

# Expose port
EXPOSE 5000

# Create non-root user
RUN useradd -m webhook && chown -R webhook:webhook /app /var/log  /app/logs
USER webhook

# Run the application
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "webhook_handler:app"]