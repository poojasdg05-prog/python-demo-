
import boto3
import json
import uuid
import mimetypes
from pathlib import Path

# Configuration
REGION = "us-east-1"
BUCKET = f"python-static-site-{uuid.uuid4().hex[:10]}"
WEBSITE_DIR = Path("website")


def create_bucket(s3):
    """Create an S3 bucket."""
    s3.create_bucket(Bucket=BUCKET)
    print("Bucket created:", BUCKET)


def configure_website(s3):
    """Enable static website hosting."""
    s3.put_bucket_website(
        Bucket=BUCKET,
        WebsiteConfiguration={
            "IndexDocument": {"Suffix": "index.html"}
        }
    )
    print("Website hosting enabled")


def allow_public_read(s3):
    """Allow visitors to read website files."""
    s3.put_public_access_block(
        Bucket=BUCKET,
        PublicAccessBlockConfiguration={
            "BlockPublicAcls": True,
            "IgnorePublicAcls": True,
            "BlockPublicPolicy": False,
            "RestrictPublicBuckets": False
        }
    )

    policy = {
        "Version": "2012-10-17",
        "Statement": [{
            "Effect": "Allow",
            "Principal": "*",
            "Action": "s3:GetObject",
            "Resource": f"arn:aws:s3:::{BUCKET}/*"
        }]
    }

    s3.put_bucket_policy(
        Bucket=BUCKET,
        Policy=json.dumps(policy)
    )
    print("Public read policy configured")


def upload_files(s3):
    """Upload website files to S3."""
    for file_path in WEBSITE_DIR.rglob("*"):
        if file_path.is_file():
            key = file_path.relative_to(WEBSITE_DIR).as_posix()
            content_type = (
                mimetypes.guess_type(file_path.name)[0]
                or "application/octet-stream"
            )

            s3.upload_file(
                str(file_path),
                BUCKET,
                key,
                ExtraArgs={"ContentType": content_type}
            )
            print("Uploaded:", key)


def main():
    s3 = boto3.client("s3", region_name=REGION)

    create_bucket(s3)
    allow_public_read(s3)
    configure_website(s3)
    upload_files(s3)

    url = (
        f"http://{BUCKET}.s3-website-{REGION}.amazonaws.com"
    )
    print("Website deployed:", url)


if __name__ == "__main__":
    main()

