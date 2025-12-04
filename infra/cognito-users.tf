resource "aws_cognito_user" "recruiter" {
  user_pool_id = aws_cognito_user_pool.recruiter_pool.id
  username     = "recruiter"          # <- ANTES recruiter@example.com

  attributes = {
    email             = "recruiter@example.com"
    email_verified    = "true"
    "custom:role"     = "recruiter"
    "custom:userId"   = "recruiter-1"
  }

  temporary_password = "Password123!"
}

resource "aws_cognito_user" "company" {
  user_pool_id = aws_cognito_user_pool.recruiter_pool.id
  username     = "company"

  attributes = {
    email             = "company@example.com"
    email_verified    = "true"
    "custom:role"     = "company"
    "custom:userId"   = "company-1"
  }

  temporary_password = "Password123!"
}

resource "aws_cognito_user" "candidate" {
  user_pool_id = aws_cognito_user_pool.recruiter_pool.id
  username     = "candidate"

  attributes = {
    email             = "candidate@example.com"
    email_verified    = "true"
    "custom:role"     = "candidate"
    "custom:userId"   = "candidate-1"
  }

  temporary_password = "Password123!"
}

resource "aws_cognito_user" "admin" {
  user_pool_id = aws_cognito_user_pool.recruiter_pool.id
  username     = "admin"

  attributes = {
    email             = "admin@example.com"
    email_verified    = "true"
    "custom:role"     = "admin"
    "custom:userId"   = "admin-1"
  }

  temporary_password = "Password123!"
}
