# 🚀 AWS Image Processing Pipeline

A serverless image upload system built using AWS Lambda, API Gateway, and S3.

---

## 🧠 Architecture

Client → API Gateway → Lambda → S3 → Public Image URL

---

## 🛠 Tech Stack

- AWS Lambda (Python)
- API Gateway
- Amazon S3
- Terraform (Infrastructure as Code)
- Boto3

---

## ⚙️ Features

- Upload images using Base64
- Store images in S3 bucket
- Generate public URL for access
- Fully serverless architecture
- Infrastructure automated using Terraform

---

## 📦 API Endpoint

POST /upload

---

## 📤 Sample Request

{
  "message": "uploaded",
  "url": "https://bucket-name.s3.region.amazonaws.com/file.jpg"
}

## 📁 Project Structure

aws-image-pipeline/
│
├── frontend/           # Frontend application (React / UI)
├── lambda/             # AWS Lambda function code
│   ├── handler.py
│   ├── api.py
│   ├── requirements.txt
│
├── src/                # (Optional) additional scripts / configs
│
├── main.tf             # Main Terraform configuration
├── lambda.tf           # Lambda resource definition
├── iam.tf              # IAM roles & permissions
├── cloudfront.tf       # CDN configuration (if used)
├── monitoring.tf       # CloudWatch monitoring
├── variables.tf        # Input variables
├── outputs.tf          # Output values
│
├── template.yaml       # SAM template (optional)
├── .gitignore
├── README.md
