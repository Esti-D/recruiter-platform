# ==========================================
# HTTP API Gateway v2
# ==========================================

resource "aws_apigatewayv2_api" "http_api" {
  name          = "recruiter-http-api"
  protocol_type = "HTTP"

  cors_configuration {
    allow_origins = ["*"]

    allow_methods = [
      "GET",
      "POST",
      "PUT",
      "PATCH",
      "DELETE",
      "OPTIONS"
    ]

    allow_headers = [
      "Content-Type",
      "Authorization",
      "X-Requested-With",
      "X-Api-Key",
      "X-Role",
      "X-User-Id"
    ]
  }
}

resource "aws_apigatewayv2_stage" "http_stage" {
  api_id      = aws_apigatewayv2_api.http_api.id
  name        = "prod"
  auto_deploy = true
}

# ==========================================
# Cognito Authorizer (JWT)
# ==========================================

resource "aws_apigatewayv2_authorizer" "cognito" {
  name    = "recruiter-cognito-authorizer"
  api_id  = aws_apigatewayv2_api.http_api.id

  authorizer_type  = "JWT"
  identity_sources = ["$request.header.Authorization"]

  jwt_configuration {
    audience = [aws_cognito_user_pool_client.frontend.id]
    issuer   = "https://cognito-idp.eu-west-1.amazonaws.com/${aws_cognito_user_pool.recruiter_pool.id}"
  }
}

# ==========================================
# Integraciones
# ==========================================

# recruiter-core-lambda (offers, candidates, roles, settings…)
resource "aws_apigatewayv2_integration" "http_core" {
  api_id                 = aws_apigatewayv2_api.http_api.id
  integration_type       = "AWS_PROXY"
  integration_uri        = aws_lambda_function.recruiter_core.arn
  integration_method     = "POST"
  payload_format_version = "2.0"
}

# process-lambda (processes)
resource "aws_apigatewayv2_integration" "http_process" {
  api_id                 = aws_apigatewayv2_api.http_api.id
  integration_type       = "AWS_PROXY"
  integration_uri        = aws_lambda_function.process.arn
  integration_method     = "POST"
  payload_format_version = "2.0"
}

# ==========================================
# Rutas recruiter-core-lambda (con JWT)
# ==========================================

# OFFERS (ANY con JWT)
resource "aws_apigatewayv2_route" "offers_root" {
  api_id    = aws_apigatewayv2_api.http_api.id
  route_key = "ANY /offers"
  target    = "integrations/${aws_apigatewayv2_integration.http_core.id}"

  authorizer_id      = aws_apigatewayv2_authorizer.cognito.id
  authorization_type = "JWT"
}

resource "aws_apigatewayv2_route" "offers_proxy" {
  api_id    = aws_apigatewayv2_api.http_api.id
  route_key = "ANY /offers/{proxy+}"
  target    = "integrations/${aws_apigatewayv2_integration.http_core.id}"

  authorizer_id      = aws_apigatewayv2_authorizer.cognito.id
  authorization_type = "JWT"
}

# OFFERS (OPTIONS sin JWT)
resource "aws_apigatewayv2_route" "offers_options_root" {
  api_id    = aws_apigatewayv2_api.http_api.id
  route_key = "OPTIONS /offers"
  target    = "integrations/${aws_apigatewayv2_integration.http_core.id}"

  authorization_type = "NONE"
}

resource "aws_apigatewayv2_route" "offers_options_proxy" {
  api_id    = aws_apigatewayv2_api.http_api.id
  route_key = "OPTIONS /offers/{proxy+}"
  target    = "integrations/${aws_apigatewayv2_integration.http_core.id}"

  authorization_type = "NONE"
}

# CANDIDATES (ANY con JWT)
resource "aws_apigatewayv2_route" "candidates_root" {
  api_id    = aws_apigatewayv2_api.http_api.id
  route_key = "ANY /candidates"
  target    = "integrations/${aws_apigatewayv2_integration.http_core.id}"

  authorizer_id      = aws_apigatewayv2_authorizer.cognito.id
  authorization_type = "JWT"
}

resource "aws_apigatewayv2_route" "candidates_proxy" {
  api_id    = aws_apigatewayv2_api.http_api.id
  route_key = "ANY /candidates/{proxy+}"
  target    = "integrations/${aws_apigatewayv2_integration.http_core.id}"

  authorizer_id      = aws_apigatewayv2_authorizer.cognito.id
  authorization_type = "JWT"
}

# CANDIDATES (OPTIONS sin JWT)
resource "aws_apigatewayv2_route" "candidates_options_root" {
  api_id    = aws_apigatewayv2_api.http_api.id
  route_key = "OPTIONS /candidates"
  target    = "integrations/${aws_apigatewayv2_integration.http_core.id}"

  authorization_type = "NONE"
}

resource "aws_apigatewayv2_route" "candidates_options_proxy" {
  api_id    = aws_apigatewayv2_api.http_api.id
  route_key = "OPTIONS /candidates/{proxy+}"
  target    = "integrations/${aws_apigatewayv2_integration.http_core.id}"

  authorization_type = "NONE"
}

# ROLES (ANY con JWT)
resource "aws_apigatewayv2_route" "roles_root" {
  api_id    = aws_apigatewayv2_api.http_api.id
  route_key = "ANY /roles"
  target    = "integrations/${aws_apigatewayv2_integration.http_core.id}"

  authorizer_id      = aws_apigatewayv2_authorizer.cognito.id
  authorization_type = "JWT"
}

resource "aws_apigatewayv2_route" "roles_proxy" {
  api_id    = aws_apigatewayv2_api.http_api.id
  route_key = "ANY /roles/{proxy+}"
  target    = "integrations/${aws_apigatewayv2_integration.http_core.id}"

  authorizer_id      = aws_apigatewayv2_authorizer.cognito.id
  authorization_type = "JWT"
}

# ROLES (OPTIONS sin JWT)
resource "aws_apigatewayv2_route" "roles_options_root" {
  api_id    = aws_apigatewayv2_api.http_api.id
  route_key = "OPTIONS /roles"
  target    = "integrations/${aws_apigatewayv2_integration.http_core.id}"

  authorization_type = "NONE"
}

resource "aws_apigatewayv2_route" "roles_options_proxy" {
  api_id    = aws_apigatewayv2_api.http_api.id
  route_key = "OPTIONS /roles/{proxy+}"
  target    = "integrations/${aws_apigatewayv2_integration.http_core.id}"

  authorization_type = "NONE"
}

# ==========================================
# Rutas process-lambda (con JWT)
# ==========================================

# PROCESSES (ANY con JWT)
resource "aws_apigatewayv2_route" "processes_root" {
  api_id    = aws_apigatewayv2_api.http_api.id
  route_key = "ANY /processes"
  target    = "integrations/${aws_apigatewayv2_integration.http_process.id}"

  authorizer_id      = aws_apigatewayv2_authorizer.cognito.id
  authorization_type = "JWT"
}

resource "aws_apigatewayv2_route" "processes_proxy" {
  api_id    = aws_apigatewayv2_api.http_api.id
  route_key = "ANY /processes/{proxy+}"
  target    = "integrations/${aws_apigatewayv2_integration.http_process.id}"

  authorizer_id      = aws_apigatewayv2_authorizer.cognito.id
  authorization_type = "JWT"
}

# PROCESSES (OPTIONS sin JWT)
resource "aws_apigatewayv2_route" "processes_options_root" {
  api_id    = aws_apigatewayv2_api.http_api.id
  route_key = "OPTIONS /processes"
  target    = "integrations/${aws_apigatewayv2_integration.http_process.id}"

  authorization_type = "NONE"
}

resource "aws_apigatewayv2_route" "processes_options_proxy" {
  api_id    = aws_apigatewayv2_api.http_api.id
  route_key = "OPTIONS /processes/{proxy+}"
  target    = "integrations/${aws_apigatewayv2_integration.http_process.id}"

  authorization_type = "NONE"
}

# ==========================================
# Permisos Lambda <- API Gateway
# ==========================================

resource "aws_lambda_permission" "allow_apigw_core" {
  statement_id  = "AllowAPIGatewayInvokeCore"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.recruiter_core.arn
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_apigatewayv2_api.http_api.execution_arn}/*/*"
}

resource "aws_lambda_permission" "allow_apigw_process" {
  statement_id  = "AllowAPIGatewayInvokeProcess"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.process.arn
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_apigatewayv2_api.http_api.execution_arn}/*/*"
}
