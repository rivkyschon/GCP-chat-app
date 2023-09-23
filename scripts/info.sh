#!/bin/bash

# Display containers
echo "---- Containers ---- \n"
docker ps -a

# Display images
echo "---- Images ---- \n"
docker images

# Display volumes
echo "---- Volumes ---- \n"
docker volume ls

# Display networks
echo "---- Networks ---- \n"
docker network ls
