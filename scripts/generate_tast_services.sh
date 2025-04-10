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


PACKAGE_NAME="tast"
DEST_DIR="/tmp/$PACKAGE_NAME"
GENERATED_FOLDER_PATH="/tmp/generated_services"
COMMIT_SHA=$(cat "TAST_COMMIT")

mkdir -p $GENERATED_FOLDER_PATH

# Download a Git repo
./download_tast_services_repo.sh "$DEST_DIR" "$COMMIT_SHA"

if [ $? -ne 0 ]; then
    echo "Error: Failed to download repo. Check the output to find a problem"
    exit 1
fi

# Folders with Services used in mobly-cros
USED_SERVICES=(
"cros/services/cros/ui"
"cros/services/cros/bluetooth"
"cros/services/cros/wifi"
"cros/services/cros/audio"
"cros/services/cros/policy"
"cros/services/cros/inputs"
)

for service in "${USED_SERVICES[@]}"; do
    current_dir="$DEST_DIR/$service"
    if [ -n "$(find $current_dir -maxdepth 1 -name *.proto)" ]; then
        echo "Processing .proto files in directory: $current_dir"
        out_path=$GENERATED_FOLDER_PATH

        # Replace a go-like import to python style keeping a current package structure
        find $current_dir -name "*.proto" -print0 | xargs -0 -I {} sed -i 's#import "go.chromium.org/tast-tests#import "tast#g' {}
        # Run the grpc_tools.protoc command
        python -m grpc_tools.protoc -I=/tmp --plugin=protoc-gen-mypy \
            --python_out=$out_path --mypy_out=$out_path --grpc_python_out=$out_path $current_dir/*.proto
        touch "$out_path/$PACKAGE_NAME/$service/__init__.py" 
    else
        echo "No .proto files found in directory: $current_dir"
    fi
done


MOBLY_CROS_PATH=$(dirname "$(dirname "$(realpath "$0")")")

# sync generated folder with one in mobly-cros repo
rsync -a --delete "$GENERATED_FOLDER_PATH/$PACKAGE_NAME/" "$MOBLY_CROS_PATH/$PACKAGE_NAME/"

# Remove generated folder
rm -rf $GENERATED_FOLDER_PATH