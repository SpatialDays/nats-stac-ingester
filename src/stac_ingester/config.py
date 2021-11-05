import os
from logging import INFO
from urllib.parse import urljoin

LOG_FORMAT = '%(asctime)s - %(levelname)6s - %(message)s'
LOG_LEVEL = INFO


def get_nats_url():
    host = os.environ.get("NATS_HOST", "localhost")
    return f"nats://{host}:4222"


def get_api_url():
    host = os.environ.get("API_HOST", 'localhost')
    port = os.environ.get("API_PORT", 8082)
    return f"http://{host}:{port}"


def get_s3_url():
    endpoint = os.environ.get("S3_ENDPOINT", 'https://s3-uk-1.sa-catapult.co.uk')
    bucket = os.environ.get("S3_BUCKET", 'public-eo-data')
    return urljoin(endpoint, bucket)
