# Delivery Assigner

## Written By
Randeep Singh Ahlawat

## Description
This component receives an order from the workflow manager and does analysis between the delivery entities, the store, and customer location to determine which entity to assign to the order to get the shortest delivery time.

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
docker build --rm -t trishare/delivery-assigner:tag path_to_c3_dockerfile
```
To update the repository:
```
sudo docker login
docker push trishaire/delivery-assigner:tag
```
To create the service type the following command:
```
docker service create --name delivery-assigner --network myNet --publish 3000:3000 --env CASS_DB=VIP_of_Cass_Service trishaire/delivery-assigner:tag
```
where `VIP_of_Cass_Service` is the VIP of `myNet` overlay network

## Endpoints

### `POST /assign-entity`

requires a json object with order_id

| field | type | required | description |
|-------|------|----------|---|
| order_id |string - format uuid| true |the id of the order that we are assigning an entity to|

### `GET /health`
returns string `healthy` if the service is healthy

[Main README](https://github.com/CPVazquez/CS6343)

