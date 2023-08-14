#!/bin/bash
set -e

# setup minikube Docker environment
eval $(minikube docker-env)

ls -lrth

# Build images

# webapp
docker build -t dts/webapp Web-App/.

# API gateway
docker build -t dts/api-gw APIGateway/.

# Delivery tracker
docker build -t dts/tracker DeliveryTracker_toBeDecommisioned/.

# Telemetry Service
docker build -t dts/telemetry TelemetryService/.

# Delivery Simulator
docker build -t dts/simulator DeliverySimulator/.