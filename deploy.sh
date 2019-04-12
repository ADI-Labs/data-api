#!/bin/sh
set +ex

docker build --tag data-api .
docker run --detach \
    --net=host \
    --restart=always \
    --name data-api data-api
