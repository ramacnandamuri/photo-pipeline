import os
import boto3
from flask import Flask, render_template
from botocore.exceptions import ClientError

app = Flask(__name__)

THUMB_BUCKET = os.environ.get("THUMB_BUCKET", "photo-pipeline-thumbs")
TABLE_NAME = os.environ.get("TABLE_NAME", "photo-pipeline-metadata")
AWS_REGION = os.environ.get("AWS_DEFAULT_REGION", "eu-west-2")


def get_dynamodb_items():
    ddb = boto3.resource("dynamodb", region_name=AWS_REGION)
    table = ddb.Table(TABLE_NAME)
    response = table.scan()
    return response.get("Items", [])


def get_signed_url(key):
    s3 = boto3.client("s3", region_name=AWS_REGION)
    try:
        url = s3.generate_presigned_url(
            "get_object",
            Params={"Bucket": THUMB_BUCKET, "Key": key},
            ExpiresIn=3600,
        )
        return url
    except ClientError:
        return None


@app.route("/")
def gallery():
    items = get_dynamodb_items()
    for item in items:
        item["url"] = get_signed_url(item["thumb_key"])
    return render_template("gallery.html", images=items)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)