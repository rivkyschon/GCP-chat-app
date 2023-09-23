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

# Get commit message from the user
read -p "Enter a commit message: " commit_message

# Commit and push the changes to Git
git add .
git commit -m "$commit_message" || handle_error "Failed to commit changes"
git push origin main || handle_error "Failed to push changes to GitHub"
echo "changes have been pushed to GitHub."

# Ask if you want to add a tag
if ask_yes_no "Do you want to add a tag to this commit?"; then
  # Get the tag name from the user
  read -p "Enter a tag name: " tag_name

  # Tag the latest commit
  git tag "$tag_name" || handle_error "Failed to tag the commit"
  git push origin "$tag_name" || handle_error "Failed to push the tag to GitHub"
  echo "Tag $tag_name added and pushed to GitHub."
fi

# Success message
echo "tag has been pushed to GitHub."
