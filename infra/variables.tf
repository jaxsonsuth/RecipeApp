variable "aws_region" {
  default = "us-east-1"
}

variable "ami_id" {
  default = "ami-0fc5d935ebf8bc3bc"  # Ubuntu 22.04 in us-east-1
}

variable "instance_type" {
  default = "t3.micro"
}

variable "key_name" {
  type = string
  description = "Name of the EC2 key pair"
}

variable "private_key_path" {
  type = string
  description = "Path to your private SSH key"
}
