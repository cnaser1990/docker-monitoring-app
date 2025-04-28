# main.py
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import StreamingResponse, FileResponse
import docker
import os
import asyncio
import threading
import logging
import re
from alerts import add_alert, get_alerts
from utils import calculate_cpu_percent, calculate_memory_percent
from datetime import datetime, timezone

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Docker client initialization
docker_host = os.getenv('DOCKER_HOST', 'unix:///var/run/docker.sock')
logger.info("Initializing Docker client with DOCKER_HOST: %s", docker_host)
try:
    client = docker.DockerClient(base_url=docker_host)
    logger.info("Docker client initialized successfully.")
except Exception as e:
    logger.error("Failed to initialize Docker client: %s", e)
    raise

# Configurable thresholds
CPU_THRESHOLD = float(os.getenv('CPU_THRESHOLD', 80))
MEMORY_THRESHOLD = float(os.getenv('MEMORY_THRESHOLD', 80))
logger.info("CPU_THRESHOLD: %s, MEMORY_THRESHOLD: %s", CPU_THRESHOLD, MEMORY_THRESHOLD)

# Serve React build static files
app.mount(
    "/static",
    StaticFiles(directory="static/static"),
    name="static_assets"
)

@app.get("/", include_in_schema=False)
async def serve_index():
    """Serve React app entry point"""
    return FileResponse("static/index.html")

@app.get("/asset-manifest.json", include_in_schema=False)
async def serve_manifest():
    """Serve React asset manifest"""
    return FileResponse("static/asset-manifest.json")

@app.get("/api/containers")
async def get_containers():
    logger.info("Fetching container list")
    containers = client.containers.list()
    result = []
    for container in containers:
        ts = container.attrs['State']['StartedAt']
        if ts.endswith('Z'):
            ts = ts[:-1] + '+00:00'
        ts = re.sub(r'\.(\d{6})\d+', r'.\1', ts)
        started_at = datetime.fromisoformat(ts)

        uptime = str(datetime.now(timezone.utc) - started_at)
        result.append({
            "id": container.id,
            "name": container.name,
            "status": container.status,
            "uptime": uptime
        })
    return result

@app.get("/api/containers/{container_id}/stats")
async def get_container_stats(container_id: str):
    logger.info("Fetching stats for container: %s", container_id)
    container = client.containers.get(container_id)
    stats = container.stats(stream=False)
    cpu_percent = calculate_cpu_percent(stats)
    memory_percent = calculate_memory_percent(stats)
    return {"cpu_percent": cpu_percent, "memory_percent": memory_percent}

@app.get("/api/containers/{container_id}/logs")
async def get_container_logs(container_id: str):
    logger.info("Streaming logs for container: %s", container_id)
    container = client.containers.get(container_id)
    logs = container.logs(stream=True, follow=True)
    return StreamingResponse(logs, media_type="text/plain")

@app.get("/api/alerts")
async def get_alerts_endpoint():
    logger.info("Fetching alerts")
    return get_alerts()

async def monitor_stats():
    logger.info("Starting container stats monitoring")
    try:
        while True:
            containers = client.containers.list()
            for container in containers:
                stats = container.stats(stream=False)
                cpu_percent = calculate_cpu_percent(stats)
                memory_percent = calculate_memory_percent(stats)
                if cpu_percent > CPU_THRESHOLD:
                    add_alert(
                        f"Container {container.name} CPU usage {cpu_percent:.2f}% > {CPU_THRESHOLD}%"
                    )
                if memory_percent > MEMORY_THRESHOLD:
                    add_alert(
                        f"Container {container.name} memory usage {memory_percent:.2f}% > {MEMORY_THRESHOLD}%"
                    )
            await asyncio.sleep(5)
    except Exception as e:
        logger.error("Error in monitor_stats: %s", e)

# Helper: non-blocking Docker event monitor in a separate thread
def _event_thread():
    try:
        for event in client.events(decode=True):
            if event.get('Type') == 'container' and event.get('Action') == 'die':
                container_name = event['Actor']['Attributes'].get('name', '<unknown>')
                add_alert(f"Container {container_name} has stopped.")
    except Exception as e:
        logger.error("Event monitor thread crashed: %s", e)

@app.on_event("startup")
async def startup_event():
    logger.info("Starting background tasks")
    thread = threading.Thread(target=_event_thread, daemon=True)
    thread.start()
    asyncio.create_task(monitor_stats())
    logger.info("Background tasks started")

logger.info("Application setup complete")

