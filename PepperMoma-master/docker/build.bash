#!/bin/bash

# Use  ./build.bash [version] [Dockerfile] [--no-cache]

IMAGENAME=marrtino-pepper-hri

VERSION=0.5
if [ ! "$1" == "" ]; then
  VERSION=$1
fi

DOCKERFILE=Dockerfile
if [ ! "$2" == "" ]; then
  DOCKERFILE=$2
fi

NAOQI=""
if [ -f downloads/naoqi-sdk-2.5.5.5-linux64.tar.gz ]; then
    NAOQI="OK"
fi

docker build $3 -t $IMAGENAME:$VERSION --build-arg NAOQI=$NAOQI -f $DOCKERFILE .

docker tag $IMAGENAME:$VERSION $IMAGENAME:latest

