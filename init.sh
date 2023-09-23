#!/bin/bash

# Prompt the user for the Docker image tag
read -p "Enter the Docker image tag: " IMAGE_TAG

# Check if the tag is not empty
if [ -z "$IMAGE_TAG" ]; then
    echo "Image tag cannot be empty. Exiting."
    exit 1
fi

# Build the Docker image with the specified tag
docker build -t chat-app:$IMAGE_TAG .

# Check if the image build was successful
if [ $? -ne 0 ]; then
    echo "Docker image build failed. Exiting."
    exit 1
fi

# Set the CUSTOM_IMAGE environment variable for docker-compose
export CUSTOM_IMAGE=chat-app:$IMAGE_TAG

# Run docker-compose with the specified image tag
docker-compose up

# Cleanup: Unset the CUSTOM_IMAGE environment variable
unset CUSTOM_IMAGE
