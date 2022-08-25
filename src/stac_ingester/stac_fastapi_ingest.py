import json.decoder
import logging
import os
from logging import INFO
from urllib.parse import urljoin

import requests

LOG_FORMAT = '%(asctime)s - %(levelname)6s - %(message)s'
LOG_LEVEL = INFO

logging.basicConfig(level=LOG_LEVEL, format=LOG_FORMAT)
logger = logging.getLogger(__name__)

STAC_SERVER_URL = os.environ.get("NATS_STAC_INGESTER_STAC_SERVER_URL", "http://localhost:8082/")
STAC_SERVER_PROVIDER_NAME = os.environ.get("NATS_STAC_INGESTER_STAC_SERVER_PROVIDER_NAME", "")
STAC_SERVER_PROVIDER_URL = os.environ.get("NATS_STAC_INGESTER_STAC_SERVER_PROVIDER_URL", "")


def ingest_catalog(data):
    pass


def ingest_collection(data_as_string: str) -> None:
    """
    Ingest a collection into the STAC server.
    :param data_as_string: Collection represented as a JSON string.
    :return: None
    :raise KeyError: If the link is not present in the list of links inside collection.

    """
    data = json.loads(data_as_string)
    data["links"] = remove_unwanted_links(data["links"])
    data["providers"] = add_our_provider_to_list_of_providers(data["providers"])
    post_or_put(urljoin(STAC_SERVER_URL, "collections"), data)


def ingest_item(data_as_string: str) -> None:
    """
    Ingest an item into the STAC server.

    :param data_as_string: Item represented as a JSON string.
    :return: None

    :raise KeyError: If the collection reference is not present in the item.
    :raise KeyError: If the link is not present in the list of links inside item.
    """
    data = json.loads(data_as_string)
    collection = data["collection"]
    data["links"] = remove_unwanted_links(data["links"])
    post_or_put(urljoin(STAC_SERVER_URL, f"collections/{collection}/items"), data)


def post_or_put(url: str, data: dict):
    """
    Post or put data to the given url.
    :param url: Url to make the request to.
    :param data: Data to use in body of request.
    :return: None

    :raise RuntimeError: If the request fails.
    """
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


def remove_unwanted_links(links: list) -> list:
    """
    Remove unwanted links from a list of links.

    Before ingesting items or collections into the STAC server, we need to remove the unwanted links that
    point to the original data source so our stac-api can recreate them with appropriate links.

    Args:
    :param links: List of links to remove unwanted links from.
    :return: List of links with unwanted links removed.
    """
    rels_that_need_removing = ["items", "parent", "root", "self", "collection"]
    # filter out the rels that we don't want to ingest
    links = [link for link in links if link["rel"]
             not in rels_that_need_removing]
    return links


def add_our_provider_to_list_of_providers(providers: list) -> list:
    """
    Add our provider to the list of providers.

    The provider and it's url are obtained from the environment variables called
    NATS_STAC_INGESTER_STAC_SERVER_PROVIDER_NAME and
    NATS_STAC_INGESTER_STAC_SERVER_PROVIDER_URL.

    Args:
    :param providers: List of providers.
    :return: List of providers with our provider added.
    """
    if STAC_SERVER_PROVIDER_NAME and STAC_SERVER_PROVIDER_URL:
        providers.append({"name": STAC_SERVER_PROVIDER_NAME, "url": STAC_SERVER_PROVIDER_URL, "roles": ["host"]})
    return providers
