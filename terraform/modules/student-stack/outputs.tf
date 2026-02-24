output "ecr_repository_url" {
  value = aws_ecr_repository.ecr_repo.repository_url
}

output "ec2_instance_id" {
  value = aws_instance.ec2.id
}

output "ec2_instance_public_ip" {
  value = aws_instance.ec2.public_ip
}

output "ec2_instance_public_dns" {
  value = aws_instance.ec2.public_dns
}

output "s3_bucket_name" {
  value = aws_s3_bucket.bucket.id
}

output "domain_name" {
  value = aws_route53_record.username_subdomain.fqdn
}