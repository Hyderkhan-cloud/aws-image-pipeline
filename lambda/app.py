import json
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('ImageMetadata')

def lambda_handler(event, context):
    for record in event['Records']:
        key = record['s3']['object']['key']

        table.put_item(Item={
            'ImageID': key,
            'Status': 'Uploaded'
        })

    print("Saved to DynamoDB")

    return {
        'statusCode': 200,
        'body': json.dumps('Done')
    }
