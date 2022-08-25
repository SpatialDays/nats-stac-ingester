import os
import asyncio
import logging
import signal
from logging import INFO

from nats.aio.client import Client as NATS
from stac_fastapi_ingest import ingest_catalog, ingest_collection, ingest_item

LOG_FORMAT = '%(asctime)s - %(levelname)6s - %(message)s'
LOG_LEVEL = INFO

logging.basicConfig(level=LOG_LEVEL, format=LOG_FORMAT)
logger = logging.getLogger(__name__)

NATS_SERVER_URL = os.environ.get("NATS_STAC_INGESTER_NATS_SERVER_URL", "nats://localhost:4222")


async def run(loop: asyncio.AbstractEventLoop) -> None:
    """
    Run the NATS client.
    :param loop: Asyncio event loop.
    :return: None
    """
    nc = NATS()

    async def closed_cb():
        logger.info("Connection to NATS is closed.")
        await asyncio.sleep(0.1, loop=loop)
        loop.stop()

    options = {
        "servers": [NATS_SERVER_URL],
        "loop": loop,
        "closed_cb": closed_cb
    }

    await nc.connect(**options)
    logger.info(f"Connected to NATS at {nc.connected_url.netloc}...")

    async def message_handler_ingest_catalog(msg):
        subject = msg.subject
        data = msg.data.decode()
        logger.info(f"Received a message on '{subject}'")
        ingest_catalog(data)

    async def message_handler_ingest_collection(msg):
        subject = msg.subject
        data = msg.data.decode()
        logger.info(f"Received a message on '{subject}'")
        ingest_collection(data)

    async def message_handler_ingest_item(msg):
        subject = msg.subject
        data = msg.data.decode()
        logger.info(f"Received a message on '{subject}'")
        ingest_item(data)

    # await nc.subscribe("nats_stac_ingester.*", cb=message_handler)
    await nc.subscribe("nats_stac_ingester.catalog", cb=message_handler_ingest_catalog)
    await nc.subscribe("nats_stac_ingester.collection", cb=message_handler_ingest_collection)
    await nc.subscribe("nats_stac_ingester.item", cb=message_handler_ingest_item)

    def signal_handler():
        if nc.is_closed:
            return
        logger.info("Disconnecting...")
        loop.create_task(nc.close())

    for sig in ('SIGINT', 'SIGTERM'):
        loop.add_signal_handler(getattr(signal, sig), signal_handler)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run(loop))
    try:
        loop.run_forever()
    finally:
        loop.close()
