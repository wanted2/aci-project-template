#!/bin/sh -e

source .env

VERSION=$(date +%Y-%m-%d-%H:%M:%S-%Z)

az login
az acr login --name ${AZ_REPO}

docker login ${AZ_REPO}.azurecr.io

docker tag ${IMAGE_NAME}:latest ${AZ_REPO}.azurecr.io/samples/aci-nvidia-gpu:${VERSION}

docker push ${AZ_REPO}.azurecr.io/samples/aci-nvidia-gpu:${VERSION}

echo -e "Pushed image to Azure Container Registry"