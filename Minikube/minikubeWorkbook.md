## point minikube to local docker registry
## --ONLY FOR DEVELOPMENT PURPOSE-- ##
minikube docker-env
SET DOCKER_TLS_VERIFY=1
SET DOCKER_HOST=tcp://127.0.0.1:62010
SET DOCKER_CERT_PATH=C:\Users\vgnsh\.minikube\certs
SET MINIKUBE_ACTIVE_DOCKERD=minikube
REM To point your shell to minikube's docker-daemon, run:
REM @FOR /f "tokens=*" %i IN ('minikube -p minikube docker-env') DO @%i