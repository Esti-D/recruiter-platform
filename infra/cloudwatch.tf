# ==========================================
# CloudWatch + SNS – Monitoring completo
# ==========================================

# Región actual (para el dashboard)
data "aws_region" "current" {}

# ==========================================
# SNS – Topic y suscripción por email
# ==========================================

resource "aws_sns_topic" "alerts" {
  name = "recruiter-platform-alerts"
}

resource "aws_sns_topic_subscription" "alerts_email" {
  topic_arn = aws_sns_topic.alerts.arn
  protocol  = "email"
  endpoint  = "solutionsarchitectst@gmail.com"
}


# ==========================================
# Alarmas Lambda – Errors
# ==========================================

resource "aws_cloudwatch_metric_alarm" "lambda_recruiter_core_errors" {
  alarm_name          = "recruiter-core-lambda-errors"
  alarm_description   = "Errors detected in recruiter-core-lambda"
  namespace           = "AWS/Lambda"
  metric_name         = "Errors"
  statistic           = "Sum"
  period              = 300
  evaluation_periods  = 1
  comparison_operator = "GreaterThanThreshold"
  threshold           = 0

  dimensions = {
    FunctionName = aws_lambda_function.recruiter_core.function_name
  }

  treat_missing_data = "notBreaching"

  alarm_actions = [aws_sns_topic.alerts.arn]
}

resource "aws_cloudwatch_metric_alarm" "lambda_process_errors" {
  alarm_name          = "process-lambda-errors"
  alarm_description   = "Errors detected in process-lambda"
  namespace           = "AWS/Lambda"
  metric_name         = "Errors"
  statistic           = "Sum"
  period              = 300
  evaluation_periods  = 1
  comparison_operator = "GreaterThanThreshold"
  threshold           = 0

  dimensions = {
    FunctionName = aws_lambda_function.process.function_name
  }

  treat_missing_data = "notBreaching"

  alarm_actions = [aws_sns_topic.alerts.arn]
}

# ==========================================
# Alarmas Lambda – Duration (umbral 5s)
# ==========================================

resource "aws_cloudwatch_metric_alarm" "lambda_recruiter_core_duration" {
  alarm_name          = "recruiter-core-lambda-duration-high"
  alarm_description   = "High average duration in recruiter-core-lambda"
  namespace           = "AWS/Lambda"
  metric_name         = "Duration"
  statistic           = "Average"
  period              = 300
  evaluation_periods  = 1
  comparison_operator = "GreaterThanThreshold"
  threshold           = 5000 # milisegundos

  dimensions = {
    FunctionName = aws_lambda_function.recruiter_core.function_name
  }

  treat_missing_data = "notBreaching"

  alarm_actions = [aws_sns_topic.alerts.arn]
}

resource "aws_cloudwatch_metric_alarm" "lambda_process_duration" {
  alarm_name          = "process-lambda-duration-high"
  alarm_description   = "High average duration in process-lambda"
  namespace           = "AWS/Lambda"
  metric_name         = "Duration"
  statistic           = "Average"
  period              = 300
  evaluation_periods  = 1
  comparison_operator = "GreaterThanThreshold"
  threshold           = 5000 # milisegundos

  dimensions = {
    FunctionName = aws_lambda_function.process.function_name
  }

  treat_missing_data = "notBreaching"

  alarm_actions = [aws_sns_topic.alerts.arn]
}

# ==========================================
# Alarma HTTP API – 5xx
# ==========================================

resource "aws_cloudwatch_metric_alarm" "http_api_5xx" {
  alarm_name          = "http-api-5xx-errors"
  alarm_description   = "HTTP API is returning 5xx server errors"
  namespace           = "AWS/ApiGateway"
  metric_name         = "5xx"
  statistic           = "Sum"
  period              = 300
  evaluation_periods  = 1
  comparison_operator = "GreaterThanThreshold"
  threshold           = 0

  dimensions = {
    ApiId = aws_apigatewayv2_api.http_api.id
    Stage = aws_apigatewayv2_stage.http_stage.name
  }

  treat_missing_data = "notBreaching"

  alarm_actions = [aws_sns_topic.alerts.arn]
}

# ==========================================
# Alarmas DynamoDB – ThrottledRequests
# ==========================================

resource "aws_cloudwatch_metric_alarm" "dynamodb_candidates_throttled" {
  alarm_name          = "dynamodb-candidates-throttled"
  alarm_description   = "Throttled requests on candidates table"
  namespace           = "AWS/DynamoDB"
  metric_name         = "ThrottledRequests"
  statistic           = "Sum"
  period              = 300
  evaluation_periods  = 1
  comparison_operator = "GreaterThanThreshold"
  threshold           = 0

  dimensions = {
    TableName = aws_dynamodb_table.candidates.name
  }

  treat_missing_data = "notBreaching"

  alarm_actions = [aws_sns_topic.alerts.arn]
}

resource "aws_cloudwatch_metric_alarm" "dynamodb_offers_throttled" {
  alarm_name          = "dynamodb-offers-throttled"
  alarm_description   = "Throttled requests on offers table"
  namespace           = "AWS/DynamoDB"
  metric_name         = "ThrottledRequests"
  statistic           = "Sum"
  period              = 300
  evaluation_periods  = 1
  comparison_operator = "GreaterThanThreshold"
  threshold           = 0

  dimensions = {
    TableName = aws_dynamodb_table.offers.name
  }

  treat_missing_data = "notBreaching"

  alarm_actions = [aws_sns_topic.alerts.arn]
}

resource "aws_cloudwatch_metric_alarm" "dynamodb_roles_throttled" {
  alarm_name          = "dynamodb-roles-throttled"
  alarm_description   = "Throttled requests on roles table"
  namespace           = "AWS/DynamoDB"
  metric_name         = "ThrottledRequests"
  statistic           = "Sum"
  period              = 300
  evaluation_periods  = 1
  comparison_operator = "GreaterThanThreshold"
  threshold           = 0

  dimensions = {
    TableName = aws_dynamodb_table.roles.name
  }

  treat_missing_data = "notBreaching"

  alarm_actions = [aws_sns_topic.alerts.arn]
}

resource "aws_cloudwatch_metric_alarm" "dynamodb_processes_throttled" {
  alarm_name          = "dynamodb-processes-throttled"
  alarm_description   = "Throttled requests on processes table"
  namespace           = "AWS/DynamoDB"
  metric_name         = "ThrottledRequests"
  statistic           = "Sum"
  period              = 300
  evaluation_periods  = 1
  comparison_operator = "GreaterThanThreshold"
  threshold           = 0

  dimensions = {
    TableName = aws_dynamodb_table.processes.name
  }

  treat_missing_data = "notBreaching"

  alarm_actions = [aws_sns_topic.alerts.arn]
}

# ==========================================
# Dashboard CloudWatch
# ==========================================

resource "aws_cloudwatch_dashboard" "main" {
  dashboard_name = "recruiter-platform-dashboard"

  dashboard_body = jsonencode({
    widgets = [
      {
        type   = "metric"
        x      = 0
        y      = 0
        width  = 12
        height = 6

        properties = {
          title  = "Lambda Invocations & Errors"
          region = data.aws_region.current.name
          stat   = "Sum"
          view   = "timeSeries"

          metrics = [
            ["AWS/Lambda", "Invocations", "FunctionName", aws_lambda_function.recruiter_core.function_name],
            ["AWS/Lambda", "Invocations", "FunctionName", aws_lambda_function.process.function_name],
            [".", "Errors", "FunctionName", aws_lambda_function.recruiter_core.function_name],
            [".", "Errors", "FunctionName", aws_lambda_function.process.function_name]
          ]
        }
      },
      {
        type   = "metric"
        x      = 12
        y      = 0
        width  = 12
        height = 6

        properties = {
          title  = "HTTP API 4xx / 5xx"
          region = data.aws_region.current.name
          stat   = "Sum"
          view   = "timeSeries"

          metrics = [
            ["AWS/ApiGateway", "4xx", "ApiId", aws_apigatewayv2_api.http_api.id, "Stage", aws_apigatewayv2_stage.http_stage.name],
            ["AWS/ApiGateway", "5xx", "ApiId", aws_apigatewayv2_api.http_api.id, "Stage", aws_apigatewayv2_stage.http_stage.name]
          ]
        }
      },
      {
        type   = "metric"
        x      = 0
        y      = 6
        width  = 24
        height = 6

        properties = {
          title  = "DynamoDB ThrottledRequests"
          region = data.aws_region.current.name
          stat   = "Sum"
          view   = "timeSeries"

          metrics = [
            ["AWS/DynamoDB", "ThrottledRequests", "TableName", aws_dynamodb_table.candidates.name],
            ["AWS/DynamoDB", "ThrottledRequests", "TableName", aws_dynamodb_table.offers.name],
            ["AWS/DynamoDB", "ThrottledRequests", "TableName", aws_dynamodb_table.roles.name],
            ["AWS/DynamoDB", "ThrottledRequests", "TableName", aws_dynamodb_table.processes.name]
          ]
        }
      }
    ]
  })
}
