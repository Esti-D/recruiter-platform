output "http_api_url" {
  description = "URL base de la HTTP API"
  value       = aws_apigatewayv2_api.http_api.api_endpoint
}

output "frontend_bucket_name" {
  description = "Bucket S3 donde subir el build del frontend"
  value       = aws_s3_bucket.frontend.bucket
}

output "frontend_cloudfront_domain" {
  description = "Dominio público del frontend (CloudFront)"
  value       = aws_cloudfront_distribution.frontend.domain_name
}

output "cognito_user_pool_id" {
  description = "ID del User Pool de Cognito"
  value       = aws_cognito_user_pool.recruiter_pool.id
}

output "cognito_user_pool_client_id" {
  description = "ID del App Client de Cognito"
  value       = aws_cognito_user_pool_client.frontend.id
}

output "cognito_user_pool_domain" {
  description = "Dominio del Hosted UI de Cognito"
  value       = aws_cognito_user_pool_domain.recruiter_domain.domain
}
