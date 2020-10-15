# Delivery Assigner

## Written By
Daniel Garcia and
Carla Vazquez

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
* cassandra-driver

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

### `POST /workflow-request`

requires a `workflow-request`

`workflow-request`
| field | type | options | required | description |
|-------|------|---------|----|---|
| storeId | string - format uuid | N/A | true | the id of the resturant issuing the workflow request|
| method | enum | persistent, edge | true | the workflow deployment method |
| component-list| enum array| order-verifier, cass, delivery-assigner, auto-restocker, restocker | true | the components the workflow is requesting|

Responses

on `200 OK` returns a message indicating successful workflow deployement

on `400 Bad Request` indicates the workflow-request was ill formated

on `403 Forbidden` the desired workflow could not be deployed due to component dependencies

### `GET /health`
returns string `healthy` if the service is healthy

[Main README](https://github.com/CPVazquez/CS6343)

