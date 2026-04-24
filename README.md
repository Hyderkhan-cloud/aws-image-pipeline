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
