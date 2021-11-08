import asyncio
import logging
import signal

from nats.aio.client import Client as NATS
from config import LOG_LEVEL, LOG_FORMAT, get_nats_url, get_api_url, get_s3_url
from stac_fastapi_ingest import ingest_catalog, ingest_collection, ingest_item

logging.basicConfig(level=LOG_LEVEL, format=LOG_FORMAT)
logger = logging.getLogger(__name__)


async def run(loop):
    nc = NATS()

    async def closed_cb():
        logger.info("Connection to NATS is closed.")
        await asyncio.sleep(0.1, loop=loop)
        loop.stop()

    options = {
        "servers": [get_nats_url()],
        "loop": loop,
        "closed_cb": closed_cb
    }

    await nc.connect(**options)
    logger.info(f"Connected to NATS at {nc.connected_url.netloc}...")

    async def message_handler(msg):
        subject = msg.subject
        data = msg.data.decode()
        logger.info(f"Received a message on '{subject}': {data}")
        r = {
            'catalog': ingest_catalog,
            'collection': ingest_collection,
            'item': ingest_item
        }
        message_type = subject.split('.')[1]
        if message_type in r.keys():
            for k, func in r.items():
                if k in subject:
                    url = f"{get_s3_url()}/{data}"
                    try:
                        func(get_api_url(), url)
                        logger.info("DONE")
                    except Exception as e:
                        logger.warning(e)

    await nc.subscribe("stac_indexer.*", cb=message_handler)

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
