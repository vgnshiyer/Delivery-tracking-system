#!/bin/bash
# set -e

ls -lrth

# Run k8s manifests

# switch to namespace dts
kubectl create ns dts --dry-run=client -o yaml | kubectl apply -f -
kubectl config set-context --current --namespace="dts"

# configmap
kubectl apply -f .env/configmap.yaml

# database
kubectl apply -f ./Database/deployment/kube/.

# queue
kubectl apply -f ./Queue/deployment/kube/.

# webapp
kubectl apply -f ./Web-App/deployment/kube/.

# API gateway
kubectl apply -f ./APIGateway/deployment/kube/.

# Delivery tracker
kubectl apply -f ./DeliveryTracker_toBeDecommisioned/deployment/kube/.

# Telemetry Service
kubectl apply -f ./TelemetryService/deployment/kube/.

# Delivery Simulator
kubectl apply -f ./DeliverySimulator/deployment/kube/.