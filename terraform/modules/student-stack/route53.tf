data "aws_route53_zone" "kulroai_hostedzone" {
  name         = var.route53_kulroai_domain_name
}

resource "aws_route53_record" "username_subdomain" {
  type    = "CNAME"
  name    = "${local.deployer_name}"
  ttl     = "300"
  zone_id = data.aws_route53_zone.kulroai_hostedzone.zone_id
  records = ["${aws_instance.ec2.public_dns}"]
}