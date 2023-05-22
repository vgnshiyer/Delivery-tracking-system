module "data" {
  source = "./modules/data"
  vpc_name = "${var.vpc_name}"
  subnet_name1 = "${var.subnet_name1}"
  subnet_name2 = "${var.subnet_name2}"
}