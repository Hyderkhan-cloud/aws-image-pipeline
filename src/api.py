import boto3
import json
import os
import uuid

dynamodb = boto3.resource('dynamodb')
s3 = boto3.client('s3')

BUCKET = os.environ['S3_BUCKET']
CLOUDFRONT = 'https://d2peqdhnemzj3n.cloudfront.net'

headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Headers': '*',
    'Access-Control-Allow-Methods': 'GET,POST,DELETE,OPTIONS',
    'Content-Type': 'application/json'
}

def clean_key(key):
    parts = key.split('/')
    return parts[-1]

def lambda_handler(event, context):
    path = event.get('path', '')
    method = event.get('httpMethod', '')

    if method == 'OPTIONS':
        return {'statusCode': 200, 'headers': headers, 'body': ''}

    # GET /images
    if path == '/images' and method == 'GET':
        table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])
        result = table.scan()
        items = result.get('Items', [])
        cleaned = []
        for item in items:
            fname = item.get('file_name', '')
            if fname.startswith('resized/'):
                continue
            if 'resized_urls' in item:
                for size in item['resized_urls']:
                    filename = clean_key(item['resized_urls'][size])
                    item['resized_urls'][size] = f"{CLOUDFRONT}/resized/{size}/{filename}"
            cleaned.append(item)
        return {'statusCode': 200, 'headers': headers, 'body': json.dumps(cleaned, default=str)}

    # GET /upload-url
    if path == '/upload-url' and method == 'GET':
        key = f"{uuid.uuid4()}.jpg"
        url = s3.generate_presigned_url(
            'put_object',
            Params={'Bucket': BUCKET, 'Key': key, 'ContentType': 'image/jpeg'},
            ExpiresIn=3600
        )
        return {'statusCode': 200, 'headers': headers, 'body': json.dumps({'url': url, 'key': key})}

    # DELETE /images/{id}
    if path.startswith('/images/') and method == 'DELETE':
        image_id = path.split('/')[-1]
        table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])
        
        # DynamoDB se item lo
        result = table.get_item(Key={'image_id': image_id})
        item = result.get('Item')
        
        if item:
            fname = item.get('file_name', '')
            # S3 se original delete karo
            try:
                s3.delete_object(Bucket=BUCKET, Key=fname)
                # Resized bhi delete karo
                for size in ['thumbnail', 'medium', 'large']:
                    s3.delete_object(Bucket=BUCKET, Key=f"resized/{size}/{fname}")
            except Exception as e:
                print(f"S3 delete error: {e}")
            
            # DynamoDB se delete karo
            table.delete_item(Key={'image_id': image_id})
        
        return {'statusCode': 200, 'headers': headers, 'body': json.dumps({'deleted': image_id})}

    return {'statusCode': 404, 'headers': headers, 'body': json.dumps({'error': 'Not found'})}
