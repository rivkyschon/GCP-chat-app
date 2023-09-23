#!/bin/bash

# Prune containers
docker container prune -f

# Prune images (including dangling images)
docker image prune -af

# Prune volumes
docker volume prune -f

# Prune networks
docker network prune -f
