# Docker Monitor Dashboard

A self-hosted DevOps Monitoring Dashboard for real-time Docker container monitoring.

## Features
- **Container List**: Displays all running containers with name, status, and uptime.
- **Resource Monitoring**: Real-time CPU and memory usage charts.
- **Live Logs**: Streams logs for each container.
- **Alerts**: Notifies when containers crash or exceed CPU/memory thresholds (stored in memory, optional email support).

## Prerequisites
- Docker and Docker Compose installed
- Node.js and npm installed (for building the frontend)
- Python 3.9+ installed (for the FastAPI backend)

## Setup Instructions


```bash
git clone https://github.com/cnaser1990/docker-monitoring-app.git
cd docker-monitor-app
docker-compose up -d --build
visit localhost:9090
