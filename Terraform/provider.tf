provider "aws"{
 region = var.aws_region
 access_key = var.aws_access_key
 secret_key = var.aws_secret_key
 
 assume_role {
  role_arn = "arn:aws:iam::206298038794:role/admin-etsandbox"
 }
}