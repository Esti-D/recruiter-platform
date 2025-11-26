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
      "content-type",
      "authorization",
      "x-requested-with",
      "x-api-key"
    ]

    expose_headers = []
    max_age        = 3600
  }
}

# Stage por defecto, con auto_deploy
resource "aws_apigatewayv2_stage" "default" {
  api_id      = aws_apigatewayv2_api.http_api.id
  name        = "$default"
  auto_deploy = true
}

# ==========================================
# Integraciones con Lambda
# ==========================================

# recruiter-core-lambda (roles, offers, candidates)
resource "aws_apigatewayv2_integration" "core_integration" {
  api_id                 = aws_apigatewayv2_api.http_api.id
  integration_type       = "AWS_PROXY"
  integration_uri        = aws_lambda_function.recruiter_core.invoke_arn
  integration_method     = "POST"
  payload_format_version = "2.0"
}

# process-lambda (processes)
resource "aws_apigatewayv2_integration" "process_integration" {
  api_id                 = aws_apigatewayv2_api.http_api.id
  integration_type       = "AWS_PROXY"
  integration_uri        = aws_lambda_function.process.invoke_arn
  integration_method     = "POST"
  payload_format_version = "2.0"
}

# ==========================================
# Rutas
# ==========================================

# Todas las rutas salvo /processes... → recruiter-core-lambda
resource "aws_apigatewayv2_route" "core_proxy" {
  api_id    = aws_apigatewayv2_api.http_api.id
  route_key = "ANY /{proxy+}"
  target    = "integrations/${aws_apigatewayv2_integration.core_integration.id}"
}

# /processes → process-lambda
resource "aws_apigatewayv2_route" "process_root" {
  api_id    = aws_apigatewayv2_api.http_api.id
  route_key = "ANY /processes"
  target    = "integrations/${aws_apigatewayv2_integration.process_integration.id}"
}

# /processes/... → process-lambda
resource "aws_apigatewayv2_route" "process_proxy" {
  api_id    = aws_apigatewayv2_api.http_api.id
  route_key = "ANY /processes/{proxy+}"
  target    = "integrations/${aws_apigatewayv2_integration.process_integration.id}"
}

# ==========================================
# Permisos para que API Gateway pueda invocar las Lambdas
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
