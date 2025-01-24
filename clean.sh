#!/bin/bash

docker ps -a | grep "processor-" | awk '{print $1}' | xargs -r docker rm -f
