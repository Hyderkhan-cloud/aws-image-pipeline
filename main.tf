provider "aws" {
  region = var.region
}

resource "aws_s3_bucket" "images" {
  bucket = "${var.project_name}-images-${random_id.rand.hex}"
}

resource "random_id" "rand" {
  byte_length = 4
}

resource "aws_dynamodb_table" "metadata" {
  name           = "ImageMetadata"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "ImageID"

  attribute {
    name = "ImageID"
    type = "S"
  }
}