#!/bin/bash
# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


# Script to download a Git repository to a specified folder and checkout a specific commit.
# Exits immediately if any error occurs.

set -e

ask_yn() {
  local prompt="$1"
  local response

  while true; do
    read -p "$prompt (Y/N): " response
    response=$(echo "$response" | tr '[:upper:]' '[:lower:]') # Convert to lowercase

    case "$response" in
      y|yes)
        echo "User chose Yes."
        return 0 # Success (Yes)
        ;;
      n|no)
        echo "User chose No."
        return 1 # Failure (No)
        ;;
      *)
        echo "Invalid response. Please enter Y or N."
        ;;
    esac
  done
}

# --- Configuration ---
REPO_URL="https://chromium.googlesource.com/chromiumos/platform/tast-tests"
TARGET_FOLDER="$1"
COMMIT_SHA="$2"        # The specific commit SHA to checkout (required)

if [ -z "$COMMIT_SHA" ]; then
  echo "Error: Commit SHA is required as the first argument."
  exit 1
fi

# --- Target Folder Checks ---
if [ -d "$TARGET_FOLDER" ]; then
  echo "Warning: Target folder '$TARGET_FOLDER' already exists."
  if ask_yn "Do you want to remove folder and continue?"; then
    rm -rf $TARGET_FOLDER
  else
    exit 1
  fi
else
  echo "Creating target folder '$TARGET_FOLDER'..."
  mkdir -p "$TARGET_FOLDER"
  if [ ! -d "$TARGET_FOLDER" ]; then
    echo "Error: Failed to create target folder '$TARGET_FOLDER'."
    exit 1
  fi
fi

# --- Download and Checkout ---
echo "Cloning repository '$REPO_URL' into '$TARGET_FOLDER'..."
if ! git clone "$REPO_URL" "$TARGET_FOLDER"; then
  echo "Error: Failed to clone repository '$REPO_URL' into '$TARGET_FOLDER'."
  exit 1
fi

echo "Changing current directory to '$TARGET_FOLDER'..."
cd "$TARGET_FOLDER"

echo "Checking out commit '$COMMIT_SHA'..."
if ! git checkout "$COMMIT_SHA"; then
  echo "Error: Failed to checkout commit '$COMMIT_SHA'."
  exit 1
fi

# --- Verify Checked Out Commit ---
actual_commit=$(git rev-parse HEAD)

if [ "$actual_commit" != "$COMMIT_SHA" ]; then
  echo "Error: Checked out commit '$actual_commit' does not match the expected commit '$COMMIT_SHA'."
  exit 1
fi

echo "Successfully downloaded '$REPO_URL' and verified commit '$COMMIT_SHA' in '$TARGET_FOLDER'."

exit 0