#!/usr/bin/env bash
set -e
docker build -t test/data_manager .
docker run --env ENV=DEVELOPMENT -p5000:5000 -v$(pwd)/data_manager:/data_manager test/data_manager
