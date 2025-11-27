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
      "X-Api-Key"
    ]
  }
}

resource "aws_apigatewayv2_stage" "http_stage" {
  api_id      = aws_apigatewayv2_api.http_api.id
  name        = "prod"
  auto_deploy = true
}

# ==========================================
# Integraciones
# ==========================================

# recruiter-core-lambda (offers, candidates, roles, settings…)
resource "aws_apigatewayv2_integration" "http_core" {
  api_id           = aws_apigatewayv2_api.http_api.id
  integration_type = "AWS_PROXY"
  integration_uri  = aws_lambda_function.recruiter_core.arn
  integration_method = "POST"
  payload_format_version = "2.0"
}

# process-lambda (processes)
resource "aws_apigatewayv2_integration" "http_process" {
  api_id           = aws_apigatewayv2_api.http_api.id
  integration_type = "AWS_PROXY"
  integration_uri  = aws_lambda_function.process.arn
  integration_method = "POST"
  payload_format_version = "2.0"
}

# ==========================================
# Rutas para recruiter-core-lambda
# ==========================================

resource "aws_apigatewayv2_route" "offers_root" {
  api_id    = aws_apigatewayv2_api.http_api.id
  route_key = "ANY /offers"
  target    = "integrations/${aws_apigatewayv2_integration.http_core.id}"
}

resource "aws_apigatewayv2_route" "offers_proxy" {
  api_id    = aws_apigatewayv2_api.http_api.id
  route_key = "ANY /offers/{proxy+}"
  target    = "integrations/${aws_apigatewayv2_integration.http_core.id}"
}

resource "aws_apigatewayv2_route" "candidates_root" {
  api_id    = aws_apigatewayv2_api.http_api.id
  route_key = "ANY /candidates"
  target    = "integrations/${aws_apigatewayv2_integration.http_core.id}"
}

resource "aws_apigatewayv2_route" "candidates_proxy" {
  api_id    = aws_apigatewayv2_api.http_api.id
  route_key = "ANY /candidates/{proxy+}"
  target    = "integrations/${aws_apigatewayv2_integration.http_core.id}"
}

resource "aws_apigatewayv2_route" "roles_root" {
  api_id    = aws_apigatewayv2_api.http_api.id
  route_key = "ANY /roles"
  target    = "integrations/${aws_apigatewayv2_integration.http_core.id}"
}

resource "aws_apigatewayv2_route" "roles_proxy" {
  api_id    = aws_apigatewayv2_api.http_api.id
  route_key = "ANY /roles/{proxy+}"
  target    = "integrations/${aws_apigatewayv2_integration.http_core.id}"
}

# ==========================================
# Rutas para process-lambda
# ==========================================

resource "aws_apigatewayv2_route" "processes_root" {
  api_id    = aws_apigatewayv2_api.http_api.id
  route_key = "ANY /processes"
  target    = "integrations/${aws_apigatewayv2_integration.http_process.id}"
}

resource "aws_apigatewayv2_route" "processes_proxy" {
  api_id    = aws_apigatewayv2_api.http_api.id
  route_key = "ANY /processes/{proxy+}"
  target    = "integrations/${aws_apigatewayv2_integration.http_process.id}"
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
