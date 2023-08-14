#!/bin/bash
set -e

ls -lrth

# Run k8s manifests

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