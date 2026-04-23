import boto3
import json
import uuid
from datetime import datetime
import os
from PIL import Image
import io

dynamodb = boto3.resource('dynamodb')
s3 = boto3.client('s3')

SIZES = {
    'thumbnail': (150, 150),
    'medium': (800, 600),
    'large': (1920, 1080)
}

def lambda_handler(event, context):
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])
    
    record = event['Records'][0]
    bucket = record['s3']['bucket']['name']
    key = record['s3']['object']['key']
    size = record['s3']['object']['size']
    
    # ✅ Loop fix — resized images skip karo
    if key.startswith('resized/'):
        print(f"Skipping resized image: {key}")
        return {'statusCode': 200, 'body': 'Skipped'}
    
    # Original image download karo
    response = s3.get_object(Bucket=bucket, Key=key)
    image_data = response['Body'].read()
    image = Image.open(io.BytesIO(image_data))
    
    resized_urls = {}
    
    for size_name, dimensions in SIZES.items():
        resized = image.copy()
        resized.thumbnail(dimensions)
        
        buffer = io.BytesIO()
        resized.save(buffer, format='JPEG', quality=85)
        buffer.seek(0)
        
        new_key = f"resized/{size_name}/{key}"
        s3.put_object(
            Bucket=bucket,
            Key=new_key,
            Body=buffer,
            ContentType='image/jpeg'
        )
        resized_urls[size_name] = new_key
        print(f"Resized {size_name}: {new_key}")
    
    image_id = str(uuid.uuid4())
    table.put_item(Item={
        'image_id': image_id,
        'file_name': key,
        'bucket': bucket,
        'original_size': size,
        'uploaded_at': datetime.utcnow().isoformat(),
        'status': 'processed',
        'resized_urls': resized_urls
    })
    
    return {
        'statusCode': 200,
        'body': json.dumps({
            'message': 'Image processed!',
            'image_id': image_id,
            'resized_urls': resized_urls
        })
    }
