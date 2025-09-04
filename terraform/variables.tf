variable "region" {
  default = "ap-south-1"
}

variable "instance_type" {
  default = "t3.micro"
}

variable "key_name" {
  description = "Name of existing AWS key pair"
  default     = "terraform-key" 
}

variable "ami" {
  description = "AMI ID for the EC2 instance"
  default     = "ami-0861f4e788f5069dd"
}
