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
