#take $1 $2
# $1 is a destination pass for tast folder, should be mobly-cros repo
# $2 is a hash to use to download tast-tests repo and generate from it

REPO_URL="https://chromium.googlesource.com/chromiumos/platform/tast-tests"
DEST_DIR="/tmp/tast"
BASE_DIR=$DEST_DIR
DIR_TO_ITERATE="$BASE_DIR/cros/services/cros"
GENERATED_FOLDER_PATH=$1

mkdir -p $DEST_DIR
# DOWNLOAD A GIT REPO
# Check if the destination folder already exists
if [ -d "$DEST_DIR" ]; then
    echo "Directory $DEST_DIR already exists. Ignoring it"
    # rm -r $DEST_DIR
else
    echo "Cloning the repository into $DEST_DIR..."
    git clone "$REPO_URL" "$DEST_DIR"
fi

# Folders with Services used in mobly-cros
sub_folders=(
"ui"
"bluetooth"
"wifi"
"audio"
"policy"
"inputs"
)

for sub_folder in "${sub_folders[@]}"; do
    dir=$DIR_TO_ITERATE/$sub_folder
    if [ -n "$(find $dir -maxdepth 1 -name *.proto)" ]; then
        echo "Processing .proto files in directory: $dir"

        folder_name=$(basename "$dir")
        out_path=$GENERATED_FOLDER_PATH
        
        # Run the grpc_tools.protoc command
        python -m grpc_tools.protoc -I=/tmp --plugin=protoc-gen-mypy=/usr/local/google/home/astrouski/temp_scripts/venv/bin/protoc-gen-mypy --python_out=$out_path --mypy_out=$out_path --grpc_python_out=$out_path $dir/*.proto
        touch "$dir/__init__.py" 
    else
        echo "No .proto files found in directory: $dir"
    fi
done
