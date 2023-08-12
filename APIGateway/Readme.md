## Steps to run

1. Build docker image

```
docker build -t dts/apigw .
```

**Note:** If you are using local k8s cluster like minikube, you need to point minikube to local docker daemon for pulling images using below command.

```
eval $(minikube docker-env)
# rebuild the image
```

2. Run k8s manifests

```
kubectl apply -f ./deployments/kube/.
```

3. Explore all components of the cluster

```
kubectl get all
```

