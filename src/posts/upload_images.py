import json
import os
import boto3
import uuid
import base64

images_bucket = os.environ['petsBucket']

def upload_images(event, context):
    if 'body' in event:
        s3 = boto3.client('s3')
        try:
            image_data_base64 = event['body']
            image_data = base64.b64decode(image_data_base64)
            image_key = f"{str(uuid.uuid4())}.png"
            s3.put_object(Bucket=images_bucket, Key=image_key, Body=image_data, ContentType='image/png')
            image_url = f"https://{images_bucket}.s3.amazonaws.com/{image_key}"
            return {
                'statusCode': 200,
                'body': json.dumps({'image_url': image_url})
            }
        except Exception as e:
            return {
                'statusCode': 500,
                'body': json.dumps({'error': str(e)})
            }
    else:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'No se ha proporcionado una imagen'})
        }
