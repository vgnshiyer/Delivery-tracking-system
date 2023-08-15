# Delivery Tracking System

<img src=".github/gif/app.gif?raw=true" width="400px">

---
The primary objective of this project is to create a highly scalable and reliable microservice architecture for a delivery tracking system.

The centerpiece of the system is the RabbitMQ service, which acts as a distributed messaging queue. It enables seamless communication and data exchange between various microservices within the architecture. By leveraging RabbitMQ's robustness and fault tolerance, the delivery tracking system can handle high volumes of data and ensure reliable message processing. The architecure of the system is depicted in the diagram provided below.

![Untitled drawio](https://github.com/vgnshiyer/Delivery-tracking-system/assets/39982819/34dc10c9-aedf-4dc3-83a0-b14900359110)

The deployment of this architecture is tailored to run on an Elastic Kubernetes Service (EKS) cluster within the Amazon Web Services (AWS) environment. However, the repository also provides instructions and appropriate directories for deploying the system on other platforms such as KOPS and Minikube.
The above mentioned instructions can be found in the DevOps/ directory.

The repository also includes Terraform and CloudFormation configurations specifically designed for setting up the EKS cluster on AWS. These configurations automate the provisioning of the necessary infrastructure resources, such as EC2 instances, networking components, and security groups, to ensure a smooth deployment process.

By following the steps outlined in the repository, you can deploy the microservice architecture and leverage the powerful features of RabbitMQ to build a robust delivery tracking system. The architecture's scalability, fault tolerance, and decoupled nature enable efficient handling of various components, such as order management, inventory tracking, and notifications, contributing to an overall seamless delivery experience for customers.

### Run it on a local minikube cluster.

1. Assuming that you have minikube installed, start a minikube cluster.

```
minikube start
```

2. Run docker builds.

```
chmod +x ./github/workflows/scripts/build_images.sh
./github/workflows/scripts/build_images.sh
```

3. Run k8s application manifests

```
chmod +x ./github/workflows/scripts/deploy.sh
./github/workflows/scripts/deploy.sh
```

4. Verify all k8s resources are created in the minikube cluster.

```
kubectl get all
```

5. Serve the webpage and open the app on the browser.

```
minikube service webapp
```
This command will automatically open the webapp on your browser window.