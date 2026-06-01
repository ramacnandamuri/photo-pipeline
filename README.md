# photo-pipeline

A serverless image-processing pipeline with a containerised web gallery.

## What it does

A user uploads a photo through a small web app. The upload lands in an S3 bucket
and triggers a Python Lambda function, which resizes the image, writes the
thumbnail to a second S3 bucket, and records metadata in DynamoDB. The Flask
web app reads from DynamoDB and S3 to render the gallery.

## Architecture
┌────────────┐## Stack

Python · boto3 · Pillow · Flask · Docker · Terraform · GitHub Actions ·
AWS Lambda · S3 · DynamoDB · IAM · ECR · CloudWatch · Kubernetes (minikube)

## Status

Phase 1 — foundations.

## Project structure

See `ARCHITECTURE.md` for the full design.

## Local development

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Author

Rama Nandamuri — github.com/ramacnandamuri
