# script to build docker image

set -e

cat ~/my_docker_pass.txt | base64 -d | docker login -u brax2507 --password-stdin
docker build -t brax2507/dts-webapp:v1 .
docker push brax2507/dts-webapp:v1
