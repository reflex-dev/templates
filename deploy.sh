#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Validate input
if [ -z "$1" ]; then
  echo "Error: No subfolder specified."
  echo "Usage: $0 <subfolder>"
  exit 1
fi

SUBFOLDER=$1
EXTRA_ENV=$2

# Ensure the subfolder exists
if [ ! -d "$SUBFOLDER" ]; then
  echo "Error: Subfolder '$SUBFOLDER' does not exist."
  exit 1
fi

# Navigate to the subfolder
cd "$SUBFOLDER"

# Print the current working directory for debugging
echo "Deploying content from: $(pwd)"

# Check if reflex CLI is installed
if ! command -v reflex &> /dev/null; then
  echo "Error: Reflex CLI not found. Please ensure it is installed."
  exit 1
fi

# Store the project ID in a variable
template_id=$(reflex apps project-list --token $REFLEX_AUTH_TOKEN | awk '/templates/ {print $1}')

echo "Starting deployment..."
reflex deployv2 --token $REFLEX_AUTH_TOKEN --project $template_id --no-interactive $EXTRA_ENV
echo "Deployment for '$SUBFOLDER' completed successfully."
