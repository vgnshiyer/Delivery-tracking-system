# script to build docker image

set -e

cat ~/my_docker_pass.txt | base64 -d | docker login -u brax2507 --password-stdin
docker build -t brax2507/bus-1-tracker .
docker push brax2507/bus-1-tracker:latest