# AWS cloudtrail to elasticsearch

workflow looks like


Cloudtrail -> S3 bucket -> SQS Queue <- container -> elasticsearch

## SQS policy

```json
{
  "Version": "2012-10-17",
  "Id": "arn:aws:sqs:YOUR-AWS-REGION:YOUR-AWS-ACCOUNT-ID:YOUR-QUEUE-NAME/SQSDefaultPolicy",
  "Statement": [
    {
      "Sid": "example-statement-ID",
      "Effect": "Allow",
      "Principal": {
        "AWS": "*"
      },
      "Action": "SQS:SendMessage",
      "Resource": "arn:aws:sqs:YOUR-AWS-REGION:YOUR-AWS-ACCOUNT-ID:YOUR-QUEUE-NAME",
      "Condition": {
        "ArnLike": {
          "aws:SourceArn": "arn:aws:s3:*:*:YOUR-S3-BUCKET"
        }
      }
    }
  ]
  ```

  ## S3 bucket prefix for events

  > AWSLogs/107995894928/CloudTrail/