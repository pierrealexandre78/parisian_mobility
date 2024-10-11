import json
from google.cloud import storage
from config import gcp_config

cloud_config = gcp_config.get_config()
project = cloud_config["project"]

# Initialize the Storage client
client = storage.Client(project=project)


def download_as_json(bucket, blob) -> json:
    """
    Download a blob from a bucket and return it as a string
    """
    bucket = client.bucket(bucket)
    blob = bucket.blob(blob)
    return json.loads(blob.download_as_string())
