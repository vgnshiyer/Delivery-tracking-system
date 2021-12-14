resource "aws_eks_cluster" "kafka_eks" {
  name     = "abg-kafka-k8s-cluster-sandbox"
  vpc_config {
    subnet_ids = [module.data.subnet_name_1, module.data.subnet_name_2]
  }
}

resource "aws_eks_node_group" "kafka_eks_node" {
  cluster_name    = aws_eks_cluster.kafka_eks.name
  node_group_name = "kafka-k8s-workers"
  subnet_ids      = [module.data.subnet_name_1, module.data.subnet_name_2]

  scaling_config {
    desired_size = 1
    max_size     = 1
    min_size     = 1
  }

  instance_types = [ "t2.medium" ]
  source_security_group_ids = [module.data.security_group_name]
}