# NATS-STAC-INGESTER

## Introduction

This component is meant to be to ingest STAC metadata into stac-compliant api obtained from subscribed NATS topic payload.

The metadata types supported are:
- Catalogs (list of collections)
- Collections
- Items

## Environment variables
| Environment Variable | Used for | Default |
|---|---|---|
| NATS_STAC_INGESTER_NATS_SERVER_URL | Used for setting the NATS server we are listening to| http://localhost:4222 |
| NATS_STAC_INGESTER_STAC_SERVER_URL | Used for setting the address of STAC server we are ingesting STAC records into | http://localhost:8082 |
| NATS_STAC_INGESTER_STAC_SERVER_PROVIDER_NAME | Used for adding our STAC server as a provider (for the provider part) in the list of providers on STAC records we are storing. If ommited, our STAC server wont be added as a provider | ""|
| NATS_STAC_INGESTER_STAC_SERVER_PROVIDER_URL | Used for adding our STAC server as a provider (for the URL part) in the list of providers on STAC records we are storing. If ommited, our STAC server wont be added as a provider |""|

## How can be used?

Using [nats-cli](https://github.com/nats-io/natscli) from localhost.

### Ingesting a Catalog

```bash
cat examples/mpc-catalog.json | nats pub nats_stac_ingester.catalog
```

### Ingesting a Collection

```bash
cat examples/landsat-c2-l2_collection.json | nats pub nats_stac_ingester.collection
```

### Ingesting an Item

```bash
cat examples/landsat-c2-l2_item.json | nats pub nats_stac_ingester.item
```
