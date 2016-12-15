#!/usr/bin/env bash
set -e


docker build -t test/dataset_manager .
docker run -p3031:3031 test/dataset_manager
