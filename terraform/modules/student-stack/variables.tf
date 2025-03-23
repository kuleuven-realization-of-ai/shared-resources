variable "ec2_key_pair_name" {
  type        = string
  description = "The name of the key pair to assign to the EC2 instance."
}

variable "ec2_ami_id" {
  type        = string
  description = "The AMI ID of the EC2 instance."
  default     = "ami-0ca5ef73451e16dc1" #Amazon Linux 2 AMI (HVM) - Kernel 5.10, SSD Volume Type
}

variable "ec2_instance_type" {
  type        = string
  description = "The instance type of the EC2 instance."
  default     = "t3.small"
  validation {
    condition     = contains(["t3.nano", "t3.micro", "t3.small"], var.ec2_instance_type)
    error_message = "Allowed values for input_parameter are \"t3.nano\", \"t3.micro\", or \"t3.small\"."
  }
}

variable "ec2_root_block_device_size_in_gb" {
  type        = number
  description = "The size of the root block device in GB."
  default     = 15
}

variable "route53_kulroai_domain_name" {
  type        = string
  description = "The Route53 Hosted Zone name for the KUL ROAI course. Automatically created by AWS after domain registration."
  default     = "realization-of-ai.com"
}