#!/bin/sh -e

source .env

docker build . -t ${IMAGE_NAME}