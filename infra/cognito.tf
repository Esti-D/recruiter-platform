resource "aws_cognito_user_pool" "recruiter_pool" {
  name = "recruiter-user-pool"

  alias_attributes = ["email"]

  schema {
    name                = "email"
    attribute_data_type = "String"
    required            = true
    mutable             = false

    string_attribute_constraints {
      min_length = 5
      max_length = 2048
    }
  }

  schema {
    name                = "role"
    attribute_data_type = "String"
    required            = false
    mutable             = true

    string_attribute_constraints {
      min_length = 3
      max_length = 20
    }
  }

  schema {
    name                = "userId"
    attribute_data_type = "String"
    required            = false
    mutable             = true

    string_attribute_constraints {
      min_length = 3
      max_length = 50
    }
  }

  auto_verified_attributes = ["email"]
}


resource "aws_cognito_user_pool_client" "frontend" {
  name         = "frontend-client"
  user_pool_id = aws_cognito_user_pool.recruiter_pool.id

  allowed_oauth_flows = ["implicit"]
  allowed_oauth_scopes = [
    "openid",
    "email",
    "profile"
  ]
  allowed_oauth_flows_user_pool_client = true

  callback_urls = [
    "http://localhost:5173/",
  ]

  logout_urls = [
    "http://localhost:5173/",
  ]

  supported_identity_providers = ["COGNITO"]

  generate_secret = false
}

resource "aws_cognito_user_pool_domain" "recruiter_domain" {
  domain = "recruiter-dev"
  user_pool_id = aws_cognito_user_pool.recruiter_pool.id
}
