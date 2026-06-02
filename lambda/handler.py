import io
import os
import json
import boto3
import datetime as dt
import uuid
from PIL import Image

def _s3():
    return boto3.client('s3')

def _table():
    return boto3.resource('dynamodb').Table(os.environ['TABLE_NAME'])

def lambda_handler(event, context):
    record = event['Records'][0]["s3"]
    src_bucket = record['bucket']['name']
    src_key = record['object']['key']
    thumb_bucket = os.environ['THUMB_BUCKET']

    s3 = _s3()
    obj = s3.get_object(Bucket=src_bucket, Key=src_key)
    body = obj['Body'].read()
    original_size = len(body)
    content_type = obj.get('ContentType', 'image/jpeg')

    image = Image.open(io.BytesIO(body))
    image_format = image.format or "JPEG"
    width, height = image.size

    image.thumbnail((300, 300))
    buf = io.BytesIO()
    image.save(buf, format=image_format)
    thumb_bytes = buf.getvalue()

    thumb_key = f"thumbs/{src_key}"
    s3.put_object(
        Bucket=thumb_bucket,
        Key=thumb_key,
        Body=thumb_bytes,
        ContentType=content_type,
    )

    record_id = str(uuid.uuid4())
    _table().put_item(Item={
        "id": record_id,
        "filename": src_key,
        "original_size": original_size,
        "thumb_key": thumb_key,
        "thumb_size": len(thumb_bytes),
        "width": width,
        "height": height,
        "uploaded_at": dt.datetime.utcnow().isoformat(),
    })

    return {
        "statusCode": 200,
        "body": json.dumps({"id": record_id, "thumb_key": thumb_key}),
    }