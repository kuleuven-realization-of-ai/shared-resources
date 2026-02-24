resource "aws_s3_bucket" "bucket" {
  bucket = "${local.deployer_name}-kulroai-bucket"
}
