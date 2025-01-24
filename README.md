# Distributed Data Processing System

## Overview

Scalable Docker-based solution for parallel processing of large JSON datasets with MongoDB integration.

## Components

-   `process.py`: Python script for batch processing
-   `requirements.txt`: Python dependencies
-   Dockerfile for containerization
-   Bash scripts for orchestration

## Setup Requirements

-   Docker
-   Python 3.10+
-   MongoDB
-   `jq` CLI tool

## Usage

```bash
./script.sh <json_file> <split_count> <mongodb_uri> <docker_image> <url_template> <logs_dir>
```

### Parameters

-   `json_file`: Source data file
-   `split_count`: Number of parallel processors
-   `mongodb_uri`: MongoDB connection string
-   `docker_image`: Processing container image
-   `url_template`: URL with `_id_` placeholder
-   `logs_dir`: Directory for log files

## Logging

-   `/logs/processed_ids.txt`: Successfully processed items
-   `/logs/404_errors.txt`: Not Found errors
-   `/logs/request_errors.txt`: Other request errors

## Performance

-   Parallel processing
-   Batch insertions (1000 items)
-   Configurable worker count

## Error Handling

-   Skips failed items
-   Comprehensive error logging
