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
    port = os.environ.get("API_PORT", 8081)
    return f"http://{host}:{port}"
