# Delivery Tracking System

The primary objective of this project is to create a highly scalable and reliable microservice architecture for a delivery tracking system.

The centerpiece of the system is the Kafka cluster, which acts as a distributed messaging queue. It enables seamless communication and data exchange between various microservices within the architecture. By leveraging Kafka's robustness and fault tolerance, the delivery tracking system can handle high volumes of data and ensure reliable message processing. The architecure of the system is depicted in the diagram provided below.

![Untitled drawio](https://github.com/vgnshiyer/Delivery-tracking-system/assets/39982819/6ef1f75d-8134-4112-823a-edd9016daa5f)

The deployment of this architecture is tailored to run on an Elastic Kubernetes Service (EKS) cluster within the Amazon Web Services (AWS) environment. However, the repository also provides instructions and appropriate directories for deploying the system on other platforms such as KOPS and Minikube.
The above mentioned instructions can be found in the DevOps/ directory.

The repository also includes Terraform and CloudFormation configurations specifically designed for setting up the EKS cluster on AWS. These configurations automate the provisioning of the necessary infrastructure resources, such as EC2 instances, networking components, and security groups, to ensure a smooth deployment process.

By following the steps outlined in the repository, you can deploy the microservice architecture and leverage the powerful features of Kafka to build a robust delivery tracking system. The architecture's scalability, fault tolerance, and decoupled nature enable efficient handling of various components, such as order management, inventory tracking, and notifications, contributing to an overall seamless delivery experience for customers.
