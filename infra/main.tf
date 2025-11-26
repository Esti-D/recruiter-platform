terraform {
  required_version = ">= 1.6.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  
  archive = {
      source  = "hashicorp/archive"
      version = "~> 2.0"
    }
  }
}


provider "aws" {
  region = "eu-west-1"
}


# =========================================================
# Estado de Terraform (ya creado)
# =========================================================

# Bucket S3 para guardar el estado de Terraform (lo usaremos más adelante como backend remoto)
resource "aws_s3_bucket" "tf_state" {
  bucket = "recruiterplatform-tf-state-esti"  # cambia el nombre si te da conflicto
}

# Tabla DynamoDB para los locks de Terraform
resource "aws_dynamodb_table" "tf_locks" {
  name         = "terraform-locks"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "LockID"

  attribute {
    name = "LockID"
    type = "S"
  }
}


# =========================================================
# Tablas de la aplicación Recruiter Platform
# =========================================================

# 1. CANDIDATE
# Campos (a nivel lógico): candidateId, name, dni, role, location, status, notes,
# experience, strength, salaryRange, createdAt, updatedAt
resource "aws_dynamodb_table" "candidates" {
  name         = "recruiter-candidates"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "candidateId"

  attribute {
    name = "candidateId"
    type = "S"
  }
}

# 2. OFFER
# Campos lógicos: offerId, companyName, contactPerson, role, modality,
# location, description, createdAt, updatedAt
resource "aws_dynamodb_table" "offers" {
  name         = "recruiter-offers"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "offerId"

  attribute {
    name = "offerId"
    type = "S"
  }
}

# 3. ROLE (catálogo de roles)
# Campos: roleId, name, createdAt
resource "aws_dynamodb_table" "roles" {
  name         = "recruiter-roles"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "roleId"

  attribute {
    name = "roleId"
    type = "S"
  }
}

# 4. PROCESS (procesos de selección)
# Campos lógicos: processId, offerId, roleOffer, similarRoles, recruiter,
# notes, status, createdAt, closedAt, candidates[]
resource "aws_dynamodb_table" "processes" {
  name         = "recruiter-processes"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "processId"

  attribute {
    name = "processId"
    type = "S"
  }

  # Guardamos offerId como atributo normal (no hace falta declararlo aquí
  # si no lo usamos de clave). Más adelante se puede añadir un GSI por offerId.
}