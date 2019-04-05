#!/bin/sh
set +ex

docker build --tag data-api .
docker run --detach \
    --net=host -api \
    --restart=always \
    --name data-api data-api
