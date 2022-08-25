# NATS-STAC-INGESTER

## Introduction

This component is meant to be to ingest STAC metadata into stac-compliant api obtained from subscribed NATS topic payload.

The metadata types supported are:
- Catalogs (list of collections)
- Collections
- Items

## How can be used?

Using [nats-cli](https://github.com/nats-io/natscli) from localhost.

### Ingesting a Catalog

```bash
cat examples/mpc-catalog.json | nats pub nats_stac_ingester.catalo
```

### Ingesting a Collection

```bash
cat examples/landsat-c2-l2_collection.json | nats pub nats_stac_ingester.collection
```

### Ingesting an Item

```bash
cat examples/landsat-c2-l2_item.json | nats pub nats_stac_ingester.item
```
