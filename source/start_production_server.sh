#!/usr/bin/env bash
set -e


docker build -t test/data_manager .
docker run -p3031:3031 test/data_manager
