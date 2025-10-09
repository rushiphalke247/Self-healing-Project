#!/bin/bash

# Self-Healing Infrastructure Startup Script for Linux

echo "🚀 Starting Self-Healing Infrastructure Stack..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Check if Docker is running
if ! docker info >/dev/null 2>&1; then
    echo -e "${RED}❌ Docker is not running. Please start Docker first.${NC}"
    exit 1
else
    echo -e "${GREEN}✅ Docker is running${NC}"
fi

# Check if docker-compose is available
if ! command -v docker-compose &> /dev/null; then
    echo -e "${RED}❌ docker-compose is not installed. Please install it first.${NC}"
    exit 1
else
    echo -e "${GREEN}✅ Docker Compose is available${NC}"
fi

# Stop any existing containers
echo -e "${YELLOW}🧹 Cleaning up existing containers...${NC}"
docker-compose down

# Build and start the stack
echo -e "${BLUE}📦 Building and starting containers...${NC}"
docker-compose up --build -d

# Wait for services to be ready
echo -e "${YELLOW}⏳ Waiting for services to start...${NC}"
sleep 30

# Check service health
echo -e "${BLUE}🔍 Checking service health...${NC}"

# Check Prometheus
if curl -s -f "http://localhost:9090/-/healthy" >/dev/null 2>&1; then
    echo -e "${GREEN}✅ Prometheus is healthy${NC}"
else
    echo -e "${RED}❌ Prometheus is not responding${NC}"
fi

# Check Alertmanager
if curl -s -f "http://localhost:9093/-/healthy" >/dev/null 2>&1; then
    echo -e "${GREEN}✅ Alertmanager is healthy${NC}"
else
    echo -e "${RED}❌ Alertmanager is not responding${NC}"
fi

# Check NGINX
if curl -s -f "http://localhost/" >/dev/null 2>&1; then
    echo -e "${GREEN}✅ NGINX is healthy${NC}"
else
    echo -e "${RED}❌ NGINX is not responding${NC}"
fi

# Check Webhook service
if curl -s -f "http://localhost:5000/health" >/dev/null 2>&1; then
    echo -e "${GREEN}✅ Webhook service is healthy${NC}"
else
    echo -e "${RED}❌ Webhook service is not responding${NC}"
fi

echo ""
echo -e "${GREEN}🎉 Self-Healing Infrastructure is ready!${NC}"
echo ""
echo -e "${CYAN}📊 Access URLs:${NC}"
echo "   • Prometheus: http://localhost:9090"
echo "   • Alertmanager: http://localhost:9093" 
echo "   • NGINX Demo: http://localhost"
echo "   • Node Exporter: http://localhost:9100"
echo "   • Webhook Health: http://localhost:5000/health"
echo ""
echo -e "${YELLOW}🧪 To test auto-healing:${NC}"
echo "   docker stop nginx"
echo "   # Watch the logs: docker-compose logs -f webhook"
echo ""
echo -e "${CYAN}📝 View logs:${NC}"
echo "   docker-compose logs -f"
echo ""