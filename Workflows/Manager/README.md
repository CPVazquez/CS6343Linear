# Delivery Assigner

## Written By
Daniel Garcia and Carla Vazquez

## Description
This component acts as the central manager for the workflow. It recieves the original requests from outside the system, from clients.

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
* requests

## Commands
To build the image:

```
./build.sh
```
To update the repository:
```
sudo docker login
docker push trishaire/wkf-manager:tag
```
To create the service type the following command:
```
./service.sh
```

## Endpoints

### `POST /workflow-request/<storeId>`

#### Parameters

storeId - the id of the store issuing the workflow request

#### Body

requires a `workflow-request` json object. 

`workflow-request`
| field | type | options | required | description |
|-------|------|---------|----|---|
| method | enum | persistent, edge | true | the workflow deployment method |
| component-list| enum array| order-verifier, cass, delivery-assigner, auto-restocker, restocker | true | the components the workflow is requesting|
| origin | string - format ip | N/A| true | the ip of the host issuing the request|

#### Responses

| status code | status | meaning|
|---|---|---|
|201|Created| workflow succesfully created|
|400|Bad Request|indicates the workflow-request was ill formated|
|403|Forbidden|the desired workflow could not be deployed due to component dependencies|
|409|Conflict|a workflow already exists for the specified store, and thus a new one cannot be created|
|422|Unprocessable Entity| json is valid, but contains unsupported specifications, like edge deployment method|

### `DELETE /workflow-request/<storeId>`

#### Parameters

storeId - the id of the store issuing the workflow request

#### Responses

| status code | status | meaning|
|---|---|---|
|204|No Content|the specified workflow was deleted successfuly |
|404|Not Found|the specified workflow does not exist or has already been deleted

### `GET /health`

#### Responses
| status code | status | meaning|
|---|---|---|
|200| OK | the server is up and running|
returns string `healthy` if the service is healthy

[Main README](https://github.com/CPVazquez/CS6343)

