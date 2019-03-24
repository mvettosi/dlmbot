#! /bin/bash

DIR=$(realpath $(dirname run.sh ))

if [[ -z $(docker images -q dlmbot) ]]; then
    echo "Building docker image..."
    docker build -t dlmbot ${DIR}
fi

docker run -it --rm --volume ${DIR}:/app dlmbot