#!/bin/bash

JSON_FILE=$1           # Source JSON file
SPLIT_COUNT=$2         # Number of splits/dockers
MONGODB_URI=$3         # MongoDB URI
DOCKER_IMAGE=$4        # Docker image to use
URL_TEMPLATE=$5        # URL TEMPLATE
LOGS_DIR=$6            # Logs directory
WORK_DIR=./tmp

mkdir -p "$LOGS_DIR"
rm -rf "$WORK_DIR"
mkdir -p "$WORK_DIR"

jq -c '.[]' "$JSON_FILE" | split --numeric-suffixes=0 -l $(($(jq length "$JSON_FILE") / SPLIT_COUNT + 1)) - "$WORK_DIR/split_"

for file in "$WORK_DIR"/split_*; do
    jq -s '.' "$file" > "${file}.json"
done

find "$WORK_DIR" -type f ! -name '*.json' -delete

echo "Working directory: $WORK_DIR"

for i in $(seq 0 $((SPLIT_COUNT-1))); do
    SPLIT_FILE="$WORK_DIR/split_0${i}.json"
    if [[ ! -f "$SPLIT_FILE" ]]; then
        echo "Error: File $SPLIT_FILE does not exist. Skipping..."
        continue
    fi

    echo run -d \
        -v "$(realpath "$SPLIT_FILE"):/data/list.json" \
        -v "$(realpath "$LOGS_DIR"):/logs" \
        -e MONGODB_URI="$MONGODB_URI" \
        -e URL_TEMPLATE="$URL_TEMPLATE" \
        --name "processor-$i" \
        "$DOCKER_IMAGE"

    docker run -d \
        -v "$(realpath "$SPLIT_FILE"):/data/list.json" \
        -v "$(realpath "$LOGS_DIR"):/logs" \
        -e MONGODB_URI="$MONGODB_URI" \
        -e URL_TEMPLATE="$URL_TEMPLATE" \
        --name "processor-$i" \
        "$DOCKER_IMAGE"

    
done

echo "All dockers are started"
