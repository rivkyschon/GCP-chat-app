# #!/bin/bash

# # Function to handle errors
# handle_error() {
#   echo "Error: $1"
#   exit 1
# }

# # Get version from user
# read -p "Enter version: " version

# # Get commit hash from user
# read -p "Enter commit hash: " commit_hash

# # Tag the commit
# git tag "$version" "$commit_hash" || handle_error "Failed to tag the commit"

# # Build the image
# docker build -t chat-app:$version . || handle_error "Failed to build the image"

# #push the tag to github repository
# git push origin "$version" || handle_error "failed to push to github"

# # Success message
# echo "Deployment successful!"


#!/bin/bash

# Function to handle errors
handle_error() {
  echo "Error: $1"
  exit 1
}

# Function to ask yes/no questions
ask_yes_no() {
  while true; do
    read -p "$1 [y/n]: " yn
    case $yn in
      [Yy]* ) return 0;;  # User answered "yes"
      [Nn]* ) return 1;;  # User answered "no"
      * ) echo "Please answer y or n.";;
    esac
  done
}

# Get version from user
read -p "Enter version: " version

# Get commit hash from user
read -p "Enter commit hash: " commit_hash

# Check if the image with the specified version already exists
if docker image inspect my-chat-app:$version &> /dev/null; then
  echo "Image chat-app:$version already exists."
  if ask_yes_no "Do you want to rebuild the image?"; then
    # Remove the existing image
    docker rmi chat-app:$version
    echo "Building new image."
    # Build the image
    docker build -t chat-app:$version . || handle_error "Failed to build the image"

  else
    # Use the existing image
    echo "Using the existing image."
  fi
fi


# Check if the commit hash exists
if [ -n "$commit_hash" ]; then
  # Tag the commit
  git tag "$version" "$commit_hash" || handle_error "Failed to tag the commit"
fi

# Ask the user if they want to push the image to the Artifact Registry
if ask_yes_no "Do you want to push the image to the Artifact Registry?"; then
  # Use gcloud auth activate-service-account to impersonate the "artifact-admin-sa" service account.
  # Replace <your-service-account-key-file.json> with the path to your service account key file.
  gcloud auth activate-service-account --key-file=<your-service-account-key-file.json>
  
  # Push the image to the Artifact Registry
  gcloud auth configure-docker gcr.io
  docker tag chat-app:$version gcr.io/your-project/chat-app:$version
  docker push gcr.io/your-project/chat-app:$version

  echo "Image pushed to Artifact Registry."
fi

# Success message
echo "Deployment successful!"
