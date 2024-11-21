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

# Ensure the subfolder exists
if [ ! -d "$SUBFOLDER" ]; then
  echo "Error: Subfolder '$SUBFOLDER' does not exist."
  exit 1
fi

# Navigate to the subfolder
cd "$SUBFOLDER"

# Print the current working directory for debugging
echo "Deploying content from: $(pwd)"

# Add deployment logic here
# For example, deploying with Reflex CLI
if ! command -v reflex &> /dev/null; then
  echo "Error: Reflex CLI not found. Please ensure it is installed."
  exit 1
fi

echo "Starting deployment..."
echo "DebugAuthToken= $REFLEX_AUTH_TOKEN"
# reflex deploy  # Adjust with actual Reflex deploy command
echo "Deployment for '$SUBFOLDER' completed successfully. [FAKED]"
