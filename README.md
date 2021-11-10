# PDA-STAC-INGESTER

## Introduction

This component is meant to be used alongside  [stac-fastapi](https://github.com/stac-utils/stac-fastapi) and it is used 
to ingest new STAC metadata into it. The metadata types supported are:
- Catalogs
- Collections
- Items

## How can be used?

A test environment can be found in the [docker-compose](./docker-compose.yml) file that deploys the stac-fastapi as well
as [nats](https://nats.io/) server. In this scenario, **PDA-STAC-Indexer** will be subscribed to the `stac_indexer.*`
topic and supports the three different operations mentioned above.

Using [nats-cli](https://github.com/nats-io/natscli) from localhost, and assuming the whole environment has been 
deployed using docker-compose:

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

**NOTE**: This example is using the *https://s3-uk-1.sa-catapult.co.uk* endpoint and *public-eo-data* bucket given by 
environmental variables within the docker-compose file. The tool will receive this as part of the deployment process and
assumes the objects are available through https without authentication.