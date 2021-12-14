output "vpc_name_1" {
  value = data.aws_vpc.selected_vpc.ids
}

output "subnet_name_1" {
  value = data.aws_subnet_ids.public_subnet1.ids
}

output "subnet_name_2" {
  value = data.aws_subnet_ids.public_subnet2.ids
}

output "security_group_name" {
  value = data.aws_security_group.vign_security_group.ids
}