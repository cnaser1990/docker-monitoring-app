import docker
import os

docker_host = os.getenv('DOCKER_HOST', 'unix:///var/run/docker.sock')
client = docker.DockerClient(base_url=docker_host)
