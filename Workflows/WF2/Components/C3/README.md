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
docker build --rm -t trishaire/delivery-assigner:tag path_to_c3_dockerfile
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

### `PUT /workflow-requests/<storeId>`

#### Parameters

| parameter | type | required | description |
|-------|------|----|---|
|storeId | string| true| the id of the store issuing the workflow request|

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
|201|Created| workflow successfully created|
|409|Conflict|a workflow already exists for the specified store, and thus a new one cannot be created|

### `DELETE /workflow-requests/<storeId>`

#### Parameters

| parameter | type | required | description |
|-------|------|----|---|
|storeId | string| true| the id of the store whose workflow we want to delete|

#### Responses

| status code | status | meaning|
|---|---|---|
|204|No Content| the specified workflow was deleted successfully |
|404|Not Found| the specified workflow does not exist or has already been deleted

### `GET /workflow-requests/<storeId>`

#### Parameters

| parameter | type | required | description |
|-------|------|----|---|
|storeId | string| true| the id of the store whose workflow we want to retrieve|

#### Responses

| status code | status | meaning|
|---|---|---|
|200| OK | returns the `workflow-request`|
|404| Not Found| the specified `workflow-request` does not exist and could not be retrieved|

### `GET /workflow-requests`

#### Responses

| status code | status | meaning|
|---|---|---|
|200| OK | returns all the `workflow-request`s on the workflow manager|


### `GET /assign-entity/<storeId>`

#### Parameters

| parameter | type | required | description |
|-------|------|----|---|
|storeId | string| true| the id of the store issuing the workflow request|

#### Body

requires a `order` json object. 

`order`
| field | type | options | required | description |
|-------|------|---------|----|---|
| storeId | string(UUID) | N/A | true | the workflow store ID |
| custName | string| Name | true | the name of the customer |
| paymentToken | string(UUID) | N/A | true | the payment token |
| paymentTokenType | string | N/A | true | The type of payment |
| custLocation | dict(lat, long) | N/A | true | the latitude and longitude of the customer |
| pizzaList | list | N/A | true | the list of pizzas|

#### Responses

| status code | status | meaning|
|---|---|---|
|200|OK| Updated order json|
|204|No Content| No delivery entity available|
|404|Not Found| the workflow doesnt exist for delivery assigner |
|409|Conflict| storeID not found in database |
|502|Bad Gateway| erroneous response from database, erroneous response from Google API|

`order`
| field | type | options | required | description |
|-------|------|---------|----|---|
| storeId | string(UUID) | N/A | true | the workflow store ID |
| custName | string| N/A | true | the name of the customer |
| paymentToken | string(UUID) | N/A | true | the payment token |
| paymentTokenType | string | N/A | true | The type of payment |
| custLocation | dict(lat, long) | N/A | true | the latitude and longitude of the customer |
| pizzaList | list | N/A | true | the list of pizzas|
| deliveredBy | string | N/A | true | the name of the delivery entity|
| estimatedTime | int | N/A | true | the estimated time for delivery in mintues|

### `GET /health`
returns string `healthy` if the service is healthy

[Main README](https://github.com/CPVazquez/CS6343)

