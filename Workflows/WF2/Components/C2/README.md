# Cass

## Written By
Carla Patricia Vazquez

## Description
This is the database component for both workflow mangers. It gets cql requests from several other components. It uses the official docker image for Cassandra as a base and loads our keyspace (database) on to it. It has a flask webserver to listen to workflow-request. when it recieves a PUT for a new workflow-request it inserts the store, its stock, and its associated delivery entities into the Cassandra database.

## Setup
Machine requirements:
* Python 2.7
* Docker

Package requirements:
* pipenv

Packages installed on pipenv virtual environment:
* cassandra-driver
* jsonschema
* Flask
* docker

## Commands

* To build the image:

  ```
  docker build --rm -t trishaire/cass:tag path_to_c2_dockerfile
  ```
* To update the repository:
  ```
  sudo docker login
  docker push trishaire/cass:tag
  ```
* To create cassandra service:
  ```
  docker service create --name cass --network myNet --publish 9042:9042 --publish 2000:2000 trishaire/cass:linear
  ```

## Connecting to Cass from a python component

For connecting to cassandra:
```
docker service inspect cass
Copy the virtual ip of the cassandra service
```

pip install `cassandra-driver` or make a Dockerfile with this package
python code to connect -

```
from cassandra.cluster import Cluster

cluster = Cluster(['vip of cassandra'])
session = cluster.connect()
session.execute(query)
```

## Endpoints

### `GET /coordinates/<storeId>`

#### Parameters

| parameter | type | required | description |
|-----------|------|----------|-------------|
| storeId | string | true | the id of the store issuing the workflow request |

#### Responses

| status code | status | meaning| returned |
|-------------|--------|--------| -------- |
| 200 | OK | Coordinates retreived | `coordinate` object |
| 404 | Not Found | Store does not exist, could not retrieve coordinates | N/A|

`coordinate`

| field | type |
|-------|------|
| longitude | float |
| latitude | float |

### `PUT /workflow-requests/<storeId>`

#### Parameters

| parameter | type | required | description |
|-----------|------|----------|-------------|
| storeId | string | true | the id of the store issuing the workflow request |

#### Body

Requires a `workflow-request` json object. 

`workflow-request`

| field | type | options | required | description |
|-------|------|---------|----------|-------------|
| method | enum | persistent, edge | true | the workflow deployment method |
| component-list | enum array | order-verifier, cass, delivery-assigner, auto-restocker, restocker | true | the components the workflow is requesting |
| origin | string - format ip | N/A | true | the ip of the host issuing the request |

#### Responses

| status code | status | meaning|
|-------------|--------|--------|
| 201 | Created | workflow was successfully created |
| 400 | Bad Request | indicates the workflow-request was ill formatted |
| 409 | Conflict | a workflow already exists for the specified store, and thus a new one cannot be created |
| 422 | Unprocessable Entity | json is valid, but the workflow-request specifies an unsupported workflow |

### `DELETE /workflow-requests/<storeId>`

#### Parameters

| parameter | type | required | description |
|-----------|------|----------|-------------|
| storeId | string | true | the id of the store whose workflow we want to delete |

#### Responses

| status code | status | meaning|
|-------------|--------|--------|
| 204 | No Content | the specified workflow was deleted successfully |
| 404 | Not Found | the specified workflow does not exist or has already been deleted |

### `GET /workflow-requests/<storeId>`

#### Parameters

| parameter | type | required | description |
|-----------|------|----------|-------------|
| storeId | string | true | the id of the store whose workflow we want to retrieve |

#### Responses

| status code | status | meaning | 
|-------------|--------|---------|
| 200 | OK | returns the `workflow-request` |
| 404 | Not Found | the specified `workflow-request` does not exist and could not be retrieved |

### `GET /workflow-requests`

#### Responses

| status code | status | meaning |
|-------------|--------|---------|
| 200 | OK | returns all the `workflow-request`s on the workflow manager |

### `GET /health`

#### Responses

| status code | status | meaning |
|-------------|--------|---------|
| 200 | OK | the server is up and running |
| 503 | Service Unavailable | the server is not ready to handle requests yet |

Returns string `healthy` if the service is healthy, and string `unhealthy` if the service is unhealthy.

[Main README](https://github.com/CPVazquez/CS6343Linear)
