#!/usr/bin/env bash
set -e


docker build -t test/data_manager .
docker run --env ENV=TEST -p5000:5000 test/data_manager
