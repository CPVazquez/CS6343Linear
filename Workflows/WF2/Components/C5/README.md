# Restocker

## Written By
Carla Vazquez

## Description
This component receives restock-orders. The restock-orders follow the format of the restock-order.shema.json file in the schema folder. The component also scans the database every 5 minutes to check for items that might need to be restocked.

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

To build the image:

```
docker build --rm -t trishaire/restocker:tag path_to_c5_dockerfile
```
To update the repository:
```
sudo docker login
docker push trishaire/restocker:tag
```
To create the service type the following command:
```
docker service create --name restocker --network myNet --publish 5000:5000 --env CASS_DB=VIP_of_Cass_Service trishaire/restocker:tag
```
where `VIP_of_Cass_Service` is the VIP of `myNet` overlay network

To run locally make sure you have environment variables `CASS_DB=0.0.0.0` and `FLASK_ENV=development` set

## Endpoints

### `POST /restock`

#### Body

requires a [`restock-order`](https://github.com/CPVazquez/CS6343/blob/master/Workflows/WF2/Components/C5/src/restock-order.schema.json) json object
 

`restock-order` 

| field | type | required | description |
|-------|------|----------|-------------|
| storeID | string - format uuid | true | The store that needs the restocking order filled |
| restock-list | [`restock-item`](#restock-item) array | true | A list of items to restock and their quantities|

<a name="restock-item">`restock-item`</a>
| field | type | required | description |
|-------|------|----------|-------------|
| item-name | string | true |the item that needs restocking|
| quantity | integer | true |the number of the item we want restocked |

### `GET /health`

returns string `healthy` if the service is healthy

## Testing

This component uses pytest to run unit test. you must be connected to a Cassandra instance to run the tests correctly. I'm still trying to figure out how to mock Cassandra. 

use the following command to run tests:
```
pytest --cov=src tests
```
[Main README](https://github.com/CPVazquez/CS6343)
