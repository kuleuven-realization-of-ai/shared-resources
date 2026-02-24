data "aws_caller_identity" "current" {}

data "aws_arn" "iam_user_arn" {
  arn = data.aws_caller_identity.current.arn
}

locals {
  deployer_name = replace(trimprefix(data.aws_arn.iam_user_arn.resource, "user/"), "_", "")
}
