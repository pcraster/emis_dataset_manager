#!/usr/bin/env bash
set -e


docker build -t test/emis_dataset_manager .
docker run \
    --env EMIS_CONFIGURATION=development \
    -p5000:5000 \
    -v$(pwd)/emis_dataset_manager:/emis_dataset_manager \
    test/emis_dataset_manager
