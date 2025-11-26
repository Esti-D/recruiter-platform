terraform {
  backend "s3" {
    bucket         = "recruiterplatform-tf-state-esti"   # tu bucket
    key            = "terraform.tfstate"
    region         = "eu-west-1"
    dynamodb_table = "terraform-locks"
    encrypt        = true
  }
}
