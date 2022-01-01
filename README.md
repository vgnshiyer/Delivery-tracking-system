# Confluent_on_k8s

This github repository is a attempt to deploy a kafka cluster using the open source Helm Charts provided by Confluent.

Visit [https://docs.confluent.io/operator/current/co-quickstart.html] for more info.

To demonstrate the working of the Kafka cluster on kubernetes, we will also be deploying a whole microservice architecture which will have this kafka clsuter as it's backbone for data persistence, data replication, high availability and low latency. 

## Prequisites to deploy kafka cluster on kubernetes

* A Kubernetes Cluster (GKE, EKS, AKS, minikube)
* Helm3 installed
* Kubectl installed

Step 1: Create a different namespace for our kafka cluster
<br>
kubectl create namespace confluent

Step 2: Pull the Helm repo for confluent operator<br>
helm repo add confluentinc https://packages.confluent.io/helm<br>
helm repo update

Switch to confluent namespace to default<br>
kubectl config set-context --current --namespace confluent

Step 3: Install the Confluent operator using Helm3<br>
helm upgrade --install confluent-operator confluentinc/confluent-for-kubernetes

This will install and deploy multiple resources (CRDS, RBAC's for our cluster) including the confluent Operator.

After performing these steps, you should have the confluent operator running as a K8S deployment running in your cluster.

Now we can begin deploying some kafka specific resouces to the cluster(eg brokers, zookeepers, etc.)

Step 4: Navigate to the Confluent-Operator-deployment dir.

Step 5: Deploy the KafkaWorkloads.yaml file<br>
This is a development cluster in minikube. This has only one zookeeper, one broker, one control center.<br>
You can scale according to the size of your cluster.

kubectl apply -f KafkaWorkloads.yaml

Step 6: You should see a one zookeeper, one broker cluster running on your kubernetes cluster.<br>
kubectl get po

The confluent operator was responsible for creating the kafka broker and zookeeper pods.

Step 7: Deploy the client console pod.<br>
This pod is not necessary to be deployed if you have the control center pod running. This pod allows kafka admins to run kafka specific commands on the cluster.<br>
kubectl apply -f KafkaClientConsole.yaml

If all aforementioned steps were performed successfully, you should have a whole working kafka cluster running on your kubernetes engine.


