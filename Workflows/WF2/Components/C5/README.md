# Restocker

## Written By

Carla Patricia Vazquez, Christopher Michael Scott

## Description

This component recieves restocking orders sent to the workflow manager. The restock orders follow the format of the restock-order.shema.json file in the shema folder. The component also scans the database every 5 minutes to check for items that might need to be restocked.

## Setup

Machine requirements:
* Python 3.8
* Docker

Package requirements:
* pipenv

Packages installed on pipenv virtual environment:
* flask
* gunicorn
* jsonschema
* uuid
* cassandra-driver
* docker
* pytest
* mockito
* pytest-cov

## Commands

* To build the image:
    ```
    docker build --rm -t trishare/restocker:tag path_to_c5_dockerfile
    ```

* To update the repository:
    ```
    sudo docker login
    docker push trishaire/restocker:tag
    ```

* To create the service type the following command:
    ```
    docker service create --name restocker --network myNet --publish 5000:5000 --env CASS_DB=VIP_of_Cass_Service trishaire/restocker:tag
    ```
  * Where `VIP_of_Cass_Service` is the VIP of `myNet` overlay network.

To run localy, ensure these environment variables `CASS_DB=0.0.0.0` and `FLASK_ENV=development` are set.

## Endpoints

### `POST /restock`

requires a [`restock-order`](https://github.com/CPVazquez/CS6343/blob/master/Workflows/WF2/Components/C5/src/restock-order.schema.json) json object
 
`restock-order` 

| field | type | required | description |
|-------|------|----------|-------------|
| storeID | string - format uuid | true | the store that needs restocking |
| restock-list | `restock-item` array | true | A list of items to restock and their quantities |

`restock-item` 

| field | type | required| description |
|-------|------|---------|-------------|
| item-name | string | true | the item that needs restocking|
| quantity | integer | true | the number of the item we want restocked |

#### Responses

| status code | status | meaning|
|-------------|--------|--------|
| 200 | OK | restock-order successfully processed |
| 400 | Bad Request | indicates the restock-order was ill formatted |
| 422 | Unprocessable Entity | a workflow does not exist for the specified store, thus the restock-order cannot be processed |

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
| 201 | Created | pizza order successfully created |
| 400 | Bad Request | indicates the workflow-request was ill formatted |
| 409 | Conflict | a workflow already exists for the specified store, and thus a new one cannot be created |

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

Returns string `healthy` if the service is healthy

## Testing

This component uses pytest to run unit test. you must be connected to a Cassandra instance to run the tests correctly. I'm still trying to figure out how to mock Cassandra. 

Use the following command to run tests:
```
pytest --cov=src tests
```
[Main README](https://github.com/CPVazquez/CS6343)
