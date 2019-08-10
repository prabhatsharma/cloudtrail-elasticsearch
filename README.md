# AWS cloudtrail to elasticsearch

## Problem statement
Search AWS cloudtrail logs

## Solution
Push cloudtrail logs to an elasticsearch cluster and use kibana to search logs.

## Implementation:

1. [Enable cloudtrail](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-create-a-trail-using-the-console-first-time.html) so it can push logs to an S3 bucket.
1. Enable S3 to push events on writes to an SQS queue - Keep the filter "AWSLogs/{account-number-format-11123123123}/CloudTrail/"
1. Am using [draft](https://github.com/Azure/draft) for development. Deploy the helm chart using "draft up" . This is development build.

In my case I have an elasticsearch cluster deployed in my kubernetes cluster. You can refer the [blog](https://prabhatsharma.in/blog/logging-in-kubernetes-using-elasticsearch-the-easy-way/) to install elasticsearch in your kubernetes cluster the easy way.

workflow looks like

Cloudtrail -> S3 bucket -> SQS Queue <- container -> elasticsearch

> Make sure that you have a [Dead-Letter-Queue](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-dead-letter-queues.html) to capture events that you are not able to process.

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
 }
  ```
