# SYNOPSIS

### BEFORE YOU BEGIN

* Data will be extracted from json file in public/delivery-vans/ dir
* Package VehicleDataGenerator will be used to refine the data in the below format.
'''json
{
        vehicle_name(filename): {
            queuename: someotherthing,
            trucknumber: #,
            trucktype: sometype,
            truckCoords: [
                [
                    72.9715347290039,
                    19.1967292074432
                ],
                ...
            ]
        },
        ...
}
'''
* Parallel proccessing of data will be triggered with the help of another function.
* Package kafkaSimulator/ActiveMQSimulator can be used according to the use-case.(queue/stream svc).
* Each parallel processing will be run as a thread in the background to infinitely simulate the movement of delivery vans.

## Steps to run

1. Build docker image

```
docker build -t dts/simulator .
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

