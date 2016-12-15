#!/usr/bin/env bash
set -e
docker build -t test/dataset_manager .
docker run --env ENV=DEVELOPMENT -p5000:5000 -v$(pwd)/dataset_manager:/dataset_manager test/dataset_manager
