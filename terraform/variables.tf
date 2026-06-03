variable "aws_region" {
  description = "AWS region to deploy into"
  default     = "eu-west-2"
}

variable "project" {
  description = "Project name used to name all resources"
  default     = "photo-pipeline"
}

variable "upload_bucket" {
  description = "S3 bucket for original uploads"
  default     = "photo-pipeline-uploads-rama"
}

variable "thumb_bucket" {
  description = "S3 bucket for thumbnails"
  default     = "photo-pipeline-thumbs"
}

variable "table_name" {
  description = "DynamoDB table for image metadata"
  default     = "photo-pipeline-metadata"
}