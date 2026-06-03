import io
import os
import boto3
import pytest
from moto import mock_aws
from PIL import Image

@pytest.fixture
def aws_credentials():
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_DEFAULT_REGION"] = "eu-west-2"
    os.environ["THUMB_BUCKET"] = "test-thumbs"
    os.environ["TABLE_NAME"] = "test-metadata"

@pytest.fixture
def aws(aws_credentials):
    with mock_aws():
        s3 = boto3.client("s3", region_name="eu-west-2")
        s3.create_bucket(
            Bucket="test-uploads",
            CreateBucketConfiguration={"LocationConstraint": "eu-west-2"},
        )
        s3.create_bucket(
            Bucket="test-thumbs",
            CreateBucketConfiguration={"LocationConstraint": "eu-west-2"},
        )

        ddb = boto3.client("dynamodb", region_name="eu-west-2")
        ddb.create_table(
            TableName="test-metadata",
            KeySchema=[{"AttributeName": "id", "KeyType": "HASH"}],
            AttributeDefinitions=[{"AttributeName": "id", "AttributeType": "S"}],
            BillingMode="PAY_PER_REQUEST",
        )

        yield

@pytest.fixture
def uploaded_image(aws):
    img = Image.new("RGB", (1000, 800), color="blue")
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    buf.seek(0)

    s3 = boto3.client("s3", region_name="eu-west-2")
    s3.put_object(
        Bucket="test-uploads",
        Key="test-image.jpg",
        Body=buf.getvalue(),
        ContentType="image/jpeg",
    )
    return "test-image.jpg"

def test_handler_resizes_and_stores(uploaded_image):
    import handler

    event = {
        "Records": [{
            "s3": {
                "bucket": {"name": "test-uploads"},
                "object": {"key": uploaded_image},
            }
        }]
    }

    result = handler.lambda_handler(event, None)

    assert result["statusCode"] == 200

    s3 = boto3.client("s3", region_name="eu-west-2")
    thumb = s3.get_object(Bucket="test-thumbs", Key=f"thumbs/{uploaded_image}")
    thumb_image = Image.open(io.BytesIO(thumb["Body"].read()))

    assert thumb_image.width <= 300
    assert thumb_image.height <= 300

    ddb = boto3.resource("dynamodb", region_name="eu-west-2")
    table = ddb.Table("test-metadata")
    items = table.scan()["Items"]

    assert len(items) == 1
    assert items[0]["filename"] == uploaded_image