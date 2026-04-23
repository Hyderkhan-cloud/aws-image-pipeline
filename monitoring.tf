resource "aws_cloudwatch_log_group" "lambda_logs" {
  name              = "/aws/lambda/image-resize-function"
  retention_in_days = 7
}

resource "aws_cloudwatch_metric_alarm" "lambda_errors" {
  alarm_name          = "lambda-errors"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = 1
  metric_name         = "Errors"
  namespace           = "AWS/Lambda"
  period              = 60
  statistic           = "Sum"
  threshold           = 1

  dimensions = {
    FunctionName = aws_lambda_function.image_resize.function_name
  }
}