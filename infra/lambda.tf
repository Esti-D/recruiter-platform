# ==========================================
# IAM role para las Lambdas
# ==========================================

resource "aws_iam_role" "lambda_exec" {
  name = "recruiter-lambda-exec"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Principal = {
          Service = "lambda.amazonaws.com"
        },
        Action = "sts:AssumeRole"
      }
    ]
  })
}

# Logs en CloudWatch
resource "aws_iam_role_policy_attachment" "lambda_basic" {
  role       = aws_iam_role.lambda_exec.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

# Acceso a DynamoDB
resource "aws_iam_policy" "lambda_dynamodb" {
  name        = "recruiter-lambda-dynamodb"
  description = "Permisos de lectura/escritura en tablas DynamoDB de Recruiter Platform"

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Action = [
          "dynamodb:GetItem",
          "dynamodb:PutItem",
          "dynamodb:UpdateItem",
          "dynamodb:DeleteItem",
          "dynamodb:Scan",
          "dynamodb:Query",
          "dynamodb:BatchWriteItem"
        ],
        Resource = [
          aws_dynamodb_table.candidates.arn,
          aws_dynamodb_table.offers.arn,
          aws_dynamodb_table.roles.arn,
          aws_dynamodb_table.processes.arn
        ]
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "lambda_dynamodb_attach" {
  role       = aws_iam_role.lambda_exec.name
  policy_arn = aws_iam_policy.lambda_dynamodb.arn
}

# ==========================================
# Empaquetar código de las Lambdas
# ==========================================

data "archive_file" "recruiter_core_zip" {
  type        = "zip"
  source_dir  = "../backend/recruiter-core-lambda"
  output_path = "${path.module}/build/recruiter-core-lambda.zip"
}

data "archive_file" "process_zip" {
  type        = "zip"
  source_dir  = "../backend/process-lambda"
  output_path = "${path.module}/build/process-lambda.zip"
}

# ==========================================
# Lambda: recruiter-core-lambda
# ==========================================

resource "aws_lambda_function" "recruiter_core" {
  function_name = "recruiter-core-lambda"

  role    = aws_iam_role.lambda_exec.arn
  runtime = "python3.11"
  handler = "handler.lambda_handler"

  filename         = data.archive_file.recruiter_core_zip.output_path
  source_code_hash = data.archive_file.recruiter_core_zip.output_base64sha256

  timeout = 10

  environment {
    variables = {
      CANDIDATES_TABLE = aws_dynamodb_table.candidates.name
      OFFERS_TABLE     = aws_dynamodb_table.offers.name
      ROLES_TABLE      = aws_dynamodb_table.roles.name
      PROCESSES_TABLE  = aws_dynamodb_table.processes.name
    }
  }
}

# ==========================================
# Lambda: process-lambda
# ==========================================

resource "aws_lambda_function" "process" {
  function_name = "process-lambda"

  role    = aws_iam_role.lambda_exec.arn
  runtime = "python3.11"
  handler = "handler.lambda_handler"

  filename         = data.archive_file.process_zip.output_path
  source_code_hash = data.archive_file.process_zip.output_base64sha256

  timeout = 10

  environment {
    variables = {
      PROCESSES_TABLE  = aws_dynamodb_table.processes.name
      CANDIDATES_TABLE = aws_dynamodb_table.candidates.name
    }
  }
}
