data "aws_vpc" "selected_vpc" {
  filter {
    name   = "tag:Name"
    values = ["${var.vpc_name}"]
  }
}

data "aws_subnet_ids" "public_subnet1" {
  filter {
      name = "tag:Name"
      values = [ "${var.subnet_name1}" ]
  }
}

data "aws_subnet_ids" "public_subnet2" {
  filter {
      name = "tag:Name"
      values = [ "${var.subnet_name2}" ]
  }
}

data "aws_security_group" "vign_security_group" {
  filter {
    name   = "tag:Name"
    values = ["vign-sg"]
  }
}



