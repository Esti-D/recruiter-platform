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

# Permisos básicos de ejecución (logs en CloudWatch)
resource "aws_iam_role_policy_attachment" "lambda_basic" {
  role       = aws_iam_role.lambda_exec.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

# (Opcional) Política para acceder a DynamoDB (por ahora tus lambdas usan memoria,
# pero dejamos esto listo para cuando las adaptemos a DynamoDB)
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

# OJO: Terraform se está ejecutando en:
#   C:\Users\estib\VSCODE\SOLUTIONS\recruiter-platform\infra
# Por eso el código está en ../backend/...

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
  runtime = "python3.12"
  handler = "handler.lambda_handler"

  filename         = data.archive_file.recruiter_core_zip.output_path
  source_code_hash = data.archive_file.recruiter_core_zip.output_base64sha256

  timeout = 10
}

# ==========================================
# Lambda: process-lambda
# ==========================================

resource "aws_lambda_function" "process" {
  function_name = "process-lambda"

  role    = aws_iam_role.lambda_exec.arn
  runtime = "python3.12"
  handler = "handler.lambda_handler"

  filename         = data.archive_file.process_zip.output_path
  source_code_hash = data.archive_file.process_zip.output_base64sha256

  timeout = 10
}
