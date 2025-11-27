# ==========================================
# DynamoDB
# ==========================================

# Tabla de locks para Terraform
resource "aws_dynamodb_table" "tf_locks" {
  name         = "terraform-locks"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "LockID"

  attribute {
    name = "LockID"
    type = "S"
  }
}

# 1. CANDIDATES
resource "aws_dynamodb_table" "candidates" {
  name         = "recruiter-candidates"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "candidateId"

  attribute {
    name = "candidateId"
    type = "S"
  }
}

# 2. OFFERS
resource "aws_dynamodb_table" "offers" {
  name         = "recruiter-offers"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "offerId"

  attribute {
    name = "offerId"
    type = "S"
  }
}

# 3. ROLES
resource "aws_dynamodb_table" "roles" {
  name         = "recruiter-roles"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "roleId"

  attribute {
    name = "roleId"
    type = "S"
  }
}

# 4. PROCESSES
resource "aws_dynamodb_table" "processes" {
  name         = "recruiter-processes"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "processId"

  attribute {
    name = "processId"
    type = "S"
  }
}
