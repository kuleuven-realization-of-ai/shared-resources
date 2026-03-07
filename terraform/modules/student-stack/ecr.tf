resource "aws_ecr_repository" "ecr_repo" {
  name                 = local.deployer_name
  image_tag_mutability = "MUTABLE"
}

resource "aws_ecr_lifecycle_policy" "component" {
  repository = aws_ecr_repository.ecr_repo.name
  policy     = <<EOF
    {
        "rules": [
            {
                "rulePriority": 1,
                "description": "Keep last 30 images",
                "selection": {
                    "tagStatus": "any",
                    "countType": "imageCountMoreThan",
                    "countNumber": 10
                },
                "action": {
                    "type": "expire"
                }
            }
        ]
    }
  EOF
}
