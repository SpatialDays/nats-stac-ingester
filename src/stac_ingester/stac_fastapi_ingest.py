import json.decoder
from urllib.parse import urljoin
import os
import requests
import logging
from logging import INFO
LOG_FORMAT = '%(asctime)s - %(levelname)6s - %(message)s'
LOG_LEVEL = INFO


logging.basicConfig(level=LOG_LEVEL, format=LOG_FORMAT)
logger = logging.getLogger(__name__)

STAC_SERVER_URL = os.environ.get(
    "NATS_STAC_INGESTER_STAC_SERVER_URL", "http://localhost:8082/")


def ingest_catalog(data):
    print(data)
    # catalog = get_json_from_url(url=catalog_url)

    # if catalog.get('type') != 'Catalog':
    #     raise RuntimeError(f"{catalog_url} is not a STAC Catalog.")

    # logger.info("Ingesting catalog...")

    # for link in catalog.get('links'):
    #     if link.get('rel') == 'child':
    #         ingest_collection(app_host=app_host, collection_url=link.get('href'))


def ingest_collection(data_as_string):
    data = json.loads(data_as_string)
    # print(data)
    links = data["links"]

    RELS_THAT_NEED_REMOVING = ["items", "parent", "root", "self", "collection"]

    # filter out the rels that we don't want to ingest
    links = [link for link in links if link["rel"]
             not in RELS_THAT_NEED_REMOVING]
    # put the links back into the data
    data["links"] = links
    # print data in json format indented
    # print(json.dumps(data, indent=4))
    post_or_put(urljoin(STAC_SERVER_URL, "collections"), data)


def ingest_item(data_as_string):
    data = json.loads(data_as_string)
    print(data)
    # item = get_json_from_url(url=item_url)

    # if item.get('type') != 'Feature':
    #     raise RuntimeError(f"{item_url} is not a STAC Item.")

    # logger.info(f"Ingesting {item.get('id')} item...")

    # post_or_put(urljoin(app_host, f"collections/{item.get('collection')}/items"), item)


def post_or_put(url: str, data: dict):
    """Post or put data to url."""
    try:
        r = requests.post(url, json=data)
        if r.status_code == 409:
            # Exists, so update
            r = requests.put(url, json=data)
            # Unchanged may throw a 404
            if not r.status_code == 404:
                r.raise_for_status()
        else:
            r.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Error while data ingesting: {e}")
