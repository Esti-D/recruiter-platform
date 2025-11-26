output "http_api_url" {
  description = "URL base de la HTTP API"
  value       = aws_apigatewayv2_api.http_api.api_endpoint
}
