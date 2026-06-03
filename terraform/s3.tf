resource "aws_s3_bucket" "uploads" {
  bucket = var.upload_bucket

  tags = {
    Project = var.project
  }
}

resource "aws_s3_bucket" "thumbs" {
  bucket = var.thumb_bucket

  tags = {
    Project = var.project
  }
}

resource "aws_s3_bucket_versioning" "uploads" {
  bucket = aws_s3_bucket.uploads.id
  versioning_configuration {
    status = "Enabled"
  }
}