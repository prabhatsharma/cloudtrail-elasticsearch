import boto3
import json, gzip

from elasticsearch import Elasticsearch

# Get the service resource
sqs = boto3.resource('sqs', region_name='us-east-1')
s3 = boto3.client('s3')

elasticsearch_base_url = 'elasticsearch-apps-client.elasticsearch.svc.cluster.local'
es = Elasticsearch([{'host': elasticsearch_base_url, 'port': 9200}])

# Get the queue
queue = sqs.get_queue_by_name(QueueName='cloudtrail')

print('Starting cloudtrail-elasticsearch')

i=0

while True:
    messages = queue.receive_messages(
        WaitTimeSeconds=20, MaxNumberOfMessages=1)
    i+=1

    # Process messages by printing out body
    for message in messages:
        data = json.loads(message.body)
        s3Bucket = data['Records'][0]['s3']['bucket']['name']
        s3ObjectKey = data['Records'][0]['s3']['object']['key']

        log = {
            "processing_file": s3ObjectKey,
            "loop": i
        }

        print(log)
        
        response = s3.get_object(Bucket=s3Bucket, Key=s3ObjectKey)  # get file data from s3
        bytestream = response['Body'].read()    # read the s3 response to bytes
        byte_records =  gzip.decompress(bytestream) # decompress gzip file in-memory
        records = byte_records.decode("utf-8")  # converts byte records to text
        json_records = json.loads(records) # convert text records to json

        # push to elasticsearch one by one
        for record in json_records['Records']:
            recordJson = json.dumps(record)
            es.index(index="cloudtrail1", doc_type='record', id=record['eventID'], body=recordJson)

        # Let the queue know that the message is processed
        message.delete()
        