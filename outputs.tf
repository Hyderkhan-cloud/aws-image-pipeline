output "bucket_name" {
  value = aws_s3_bucket.images.bucket
}

output "cloudfront_url" {
  value = aws_cloudfront_distribution.cdn.domain_name
}