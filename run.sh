#!/bin/bash

# Arguments
JSON_FILE=$1           # Source JSON file
SPLIT_COUNT=$2         # Number of splits/dockers
MONGODB_URI=$3         # MongoDB URI
API_URL=$4             # API URL
DOCKER_IMAGE=$5        # Docker image to use
LOGS_DIR=$6            # Logs directory

# Create logs directory if not exists
mkdir -p "$LOGS_DIR"

# Create temporary working directory
WORK_DIR=$(mktemp -d)
trap 'rm -rf "$WORK_DIR"' EXIT

# Split JSON file
jq -c '.[]' "$JSON_FILE" | split -l $(($(jq length "$JSON_FILE") / SPLIT_COUNT + 1)) - "$WORK_DIR/split_"

# Generate split JSON files
for file in "$WORK_DIR"/split_*; do
    jq -s '.' "$file" > "${file}.json"
done

# Launch containers
for i in $(seq 0 $((SPLIT_COUNT-1))); do
    docker run -d \
        -v "$WORK_DIR/split_${i}.json:/data/list.json" \
        -v "$LOGS_DIR:/logs" \
        -e MONGODB_URI="$MONGODB_URI" \
        -e API_URL="$API_URL" \
        --name "processor-$i" \
        "$DOCKER_IMAGE" &
done

wait

echo "Processing completed"
