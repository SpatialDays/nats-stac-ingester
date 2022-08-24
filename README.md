# NATS-STAC-INGESTER

## Introduction

This component is meant to be to ingest STAC metadata into stac-complieant api.

The metadata types supported are:
- Catalogs
- Collections
- Items

## How can be used?

Using [nats-cli](https://github.com/nats-io/natscli) from localhost.

### Ingesting a Catalog

```bash
nats pub -s nats://localhost:4222 stac_ingester.catalog stac_catalogs/novasar_test/catalog.json
```

### Ingesting a Collection

```bash
nats pub -s nats://localhost:4222 stac_ingester.collection stac_catalogs/novasar_test/novasar_scansar_20m/collection.json
```

### Ingesting an Item

```bash
nats pub -s nats://localhost:4222 stac_ingester.item stac_catalogs/novasar_test/novasar_scansar_20m/NovaSAR_01_16359_slc_11_201025_231831_HH_2_ML_TC_TF_cog/NovaSAR_01_16359_slc_11_201025_231831_HH_2_ML_TC_TF_cog.json
```
