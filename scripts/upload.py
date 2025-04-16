import os
import json
import boto3
from botocore.client import Config
import mimetypes
import uuid

# Read credentials and config from environment variables
R2_ACCESS_KEY_ID = os.environ["R2_ACCESS_KEY_ID"]
R2_SECRET_ACCESS_KEY = os.environ["R2_SECRET_ACCESS_KEY"]
R2_BUCKET = os.environ["R2_BUCKET"]
R2_ENDPOINT = os.environ["R2_ENDPOINT"]

session = boto3.session.Session()
s3 = session.client(
    service_name="s3",
    aws_access_key_id=R2_ACCESS_KEY_ID,
    aws_secret_access_key=R2_SECRET_ACCESS_KEY,
    endpoint_url=R2_ENDPOINT,
    config=Config(signature_version="s3v4"),
)

def upload_file(local_path, s3_key):
    content_type, _ = mimetypes.guess_type(local_path)
    extra_args = {"ContentType": content_type} if content_type else {}
    with open(local_path, "rb") as f:
        s3.upload_fileobj(f, R2_BUCKET, s3_key, ExtraArgs=extra_args)

def upload_preview_file(local_path, bucket, s3_key):
    content_type, _ = mimetypes.guess_type(local_path)
    extra_args = {"ContentType": content_type} if content_type else {}
    # Use the same credentials and endpoint, but different bucket
    with open(local_path, "rb") as f:
        s3.upload_fileobj(f, bucket, s3_key, ExtraArgs=extra_args)

def main():
    root = os.path.dirname(os.path.abspath(__file__))
    base = os.path.abspath(os.path.join(root, ".."))
    templates_json = os.path.join(base, "templates.json")
    with open(templates_json, "r") as f:
        templates = json.load(f)["templates"]
    # Only publish templates with reflex_build true
    for t in templates:
        if not t.get("reflex_build", False):
            continue
        template_name = t["name"]
        template_id = str(uuid.uuid5(uuid.NAMESPACE_DNS, template_name))
        template_path = os.path.join(base, template_name)
        if os.path.isdir(template_path):
            purge_id_path(template_id)
            for dirpath, _, filenames in os.walk(template_path):
                for filename in filenames:
                    if filename.endswith(".zip"):
                        continue
                    local_path = os.path.join(dirpath, filename)
                    rel_path = os.path.relpath(local_path, template_path)
                    s3_key = f"{template_id}/{rel_path}"
                    upload_file(local_path, s3_key)
            # Upload preview.png if it exists in the base of the template directory
            preview_path = os.path.join(template_path, "preview.png")
            if os.path.isfile(preview_path):
                preview_bucket = "preview-images-dev"
                preview_s3_key = f"{template_id}/00000000-0000-0000-0000-000000000000.png"
                upload_preview_file(preview_path, preview_bucket, preview_s3_key)

def purge_id_path(template_id):
    print(f"Purging s3://{R2_BUCKET}/{template_id}/ ...")
    paginator = s3.get_paginator("list_objects_v2")
    for page in paginator.paginate(Bucket=R2_BUCKET, Prefix=f"{template_id}/"):
        objects = page.get("Contents", [])
        if objects:
            delete_keys = [{"Key": obj["Key"]} for obj in objects]
            s3.delete_objects(Bucket=R2_BUCKET, Delete={"Objects": delete_keys})
            print(f"Deleted {len(delete_keys)} objects from {template_id}/")

if __name__ == "__main__":
    main()
