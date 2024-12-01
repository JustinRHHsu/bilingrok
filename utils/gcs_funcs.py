from google.cloud import storage
from datetime import timedelta
import os
from config.config import Config


def generate_signed_url(bucket_name, blob_name, expiration=3600):
    """Generates a signed URL for a GCS blob."""
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)

    url = blob.generate_signed_url(
        expiration=timedelta(seconds=expiration),
        credentials=Config.GCP_CRED,
        version="v4"  # 使用 V4 簽名
    )
    
    return url