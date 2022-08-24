import json.decoder
from urllib.parse import urljoin

import requests
import logging

from configuration import LOG_LEVEL, LOG_FORMAT

logging.basicConfig(level=LOG_LEVEL, format=LOG_FORMAT)
logger = logging.getLogger(__name__)


def ingest_catalog(data):
    print(data)
    # catalog = get_json_from_url(url=catalog_url)

    # if catalog.get('type') != 'Catalog':
    #     raise RuntimeError(f"{catalog_url} is not a STAC Catalog.")

    # logger.info("Ingesting catalog...")

    # for link in catalog.get('links'):
    #     if link.get('rel') == 'child':
    #         ingest_collection(app_host=app_host, collection_url=link.get('href'))


def ingest_collection(data):
    print(data)
    # collection = get_json_from_url(url=collection_url)

    # if [ln for ln in collection.get('links') if (ln.get('rel') == 'parent') and ('catalog' not in ln.get('href'))]:
    #     raise RuntimeError(f"{collection_url} is not a STAC Collection.")

    # logger.info(f"Ingesting {collection.get('id')} collection...")

    # post_or_put(urljoin(app_host, "/collections"), collection)

    # for link in collection.get('links'):
    #     if link.get('rel') == 'item':
    #         ingest_item(app_host=app_host, item_url=link.get('href'))


def ingest_item(data):
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
