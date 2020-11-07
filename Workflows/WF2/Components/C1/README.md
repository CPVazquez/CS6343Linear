# Pizza Order Verifier

Workflow 2, Component 1

## Written By

Christopher Michael Scott

## Description

Upon receiving a Pizza Order, this component validates the order and checks the store's stock. If sufficient stock exists, Order Verifier decrements the store's stock and creates the order. Otherwise, Order Verifier requests a restock before decrementing stock and creating the order.

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
* cassandra-driver
* requests

## Commands

  * To build the docker image, use the following command in the folder containing the Dockerfile:
    ```
    docker build --rm -t trishaire/order-verifier:tag path_to_c1_dockerfile
    ```
  * To update Dockerhub repository:
    ```
    sudo docker login
    docker push trishaire/order-verifier:tag
    ```
  * To create the image as a service run the following command:
    ```
    docker service create --name order-verifier --network myNet --publish 1000:1000 --env CASS_DB=cass_service_vip trishaire/order-verifier:tag
    ```
    * Where `cass_service_vip` is the VIP of `myNet` overlay network.

## Endpoints

### `POST /order`

Requires a [`pizza-order`](https://github.com/CPVazquez/CS6343/blob/master/Workflows/WF2/Components/C1/src/pizza-order.schema.json) json object

`pizza-order` 

| field | type | required | description |
|-------|------|----------|-------------|
| orderId | string - format uuid | false | A base64 ID give to each order to identify it |
| storeId | string - format uuid | true | A base64 ID given to each store to identify it |
| custName | string | true | The name of the customer, as a single string for both first/last name |
| paymentToken | string - format uuid | true | The token for the third-party payment service that the customer is paying with |
| paymentTokenType | string | true | The type of token accepted (paypal, google pay, etc) |
| custLocation | `location` | true | The location of the customer, in degrees latitude and longitude |
| orderDate | string - date-time format | true | The date of order creation |
| pizzaList | `pizza` array | true | The list of pizzas that have been ordered |

`location`

| field | type | required | description |
|-------|------|----------|-------------|
| lat | number | false | latitude |
| lon | number | false | longitude |

`pizza`

| field | type | options | required | description |
|-------|------|---------|----|---|
| crustType | enum | Thin, Traditional | false | The type of crust |
| sauceType | enum | Spicy, Traditional | false | The type of sauce |
| cheeseAmt | enum | None, Light, Normal, Extra | false | The amount of cheese on the pizza |
| toppingList | enum array | Pepperoni, Sausage, Beef, Onion, Chicken, Peppers, Olives, Bacon, Pineapple, Mushrooms | false | The list of toppings added at extra cost. Cost verified by server |

#### Responses

| status code | status | meaning |
|-------------|--------|---------|
| 200 | Created | pizza-order successfully created |
| 400 | Bad Request | indicates the pizza-order was ill formatted |
| 404 | Not Found | insufficient stock at the specified store to create pizza-orer |
| 422 | Unprocessable Entity | a workflow does not exist for the specified store, thus the pizza-order cannot be created |
| 424 | Failed Dependency | request to another workflow component failed, therefore the pizza-order cannot be created | 

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

Returns string `healthy` if the service is healthy

[Main README](https://github.com/CPVazquez/CS6343)
