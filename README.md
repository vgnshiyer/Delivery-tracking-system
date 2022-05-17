# Delivery Tracking System

This github repository is a attempt to deploy a kafka cluster using the open source Helm Charts provided by Confluent.
We create the below microservice architecture in this tutorial.
![Untitled Diagram drawio](https://user-images.githubusercontent.com/39982819/168741632-da8dcda2-22fb-4c81-ab72-44a2ba1bf517.png)

The queue in the architecture was earlier the kafka cluster mentioned above. 

This system runs on an EKS cluster on AWS.
There are steps in appropriate directories for deploying the architecture in KOPS, minikube, EKS.
This also has terraform and cloudformation configs for EKS cluster. 
