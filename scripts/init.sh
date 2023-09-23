#!/bin/bash

echo "Enter the version to build and run:"
read version

# Ensure the version input is not empty
if [ -z "$version" ]; then
    echo "Version cannot be empty. Exiting..."
    exit 1
fi

# Your Docker build and run commands using the provided version
docker build -t myapp:$version .

docker run -d --name myapp-$version -p 5000:5000 --cpus "2.0" --memory "1g" -v rooms:/app/rooms myapp:$version
