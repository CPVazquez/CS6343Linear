# Order Verifier Component

Workflow 2, Component 1

## Written By

Christopher Michael Scott

## Description

Upon receiving a `pizza-order` request, this component validates the received order request 
against the `pizza-order` jsonschema (pizza-order.schema.json). If the request is a valid 
`pizza-order`, then the request will be sent to the next component in the workflow, 
if one exists. If the request is determined to be invalid, then the request is rejected 
by this component and removed from the workflow.

## Setup

Machine requirements:
* Python 3.8
* Docker

Package requirements:
* pipenv

Packages installed on pipenv virtual environment:
* quart
* jsonschema
* requests

## Commands

* To build the image, use the following command in the folder containing the Dockerfile:
  ```
  ./build.sh
  ```

* To update Dockerhub repository:
  ```
  sudo docker login
  docker push trishaire/order-verifier:tag
  ```
  * Where `tag` is the tag of order-verifier image.

* To create the image as a service run the following command:
  ```
  docker service create --name order-verifier --network myNet --publish 1000:1000 --env CASS_DB=cass_service_vip trishaire/order-verifier:tag
  ```
  * Where `cass_service_vip` is the VIP of `myNet` overlay network and `tag` is the tag of order-verifier image.

## Endpoints

### `POST /order`

#### Body

Requires a JSON object containing a [`pizza-order`](https://github.com/CPVazquez/CS6343Linear/blob/main/Workflows/WF2/Components/C1/src/pizza-order.schema.json) JSON object.

| field | type | required | description |
|-------|------|----------|-------------|
| pizza-order | `pizza-order` | true | the pizza order object |

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
| lat | number | false | Customer latitude in degrees |
| lon | number | false | Customer longitude in degrees |

`pizza`

| field | type | options | required | description |
|-------|------|---------|----|---|
| crustType | enum | Thin, Traditional | false | The type of crust |
| sauceType | enum | Spicy, Traditional | false | The type of sauce |
| cheeseAmt | enum | None, Light, Normal, Extra | false | The amount of cheese on the pizza |
| toppingList | enum array | Pepperoni, Sausage, Beef, Onion, Chicken, Peppers, Olives, Bacon, Pineapple, Mushrooms | false | The list of toppings added at extra cost (verified by server) |

#### Responses

| status code | status | meaning |
|-------------|--------|---------|
| 200 | OK | `pizza-order` successfully validated |
| 208 | Error Already Reported | Indicates an error occurred in a subsequent component, just return the response |
| 400 | Bad Request | Indicates the `pizza-order` was ill-formatted and the request was rejected |
| 422 | Unprocessable Entity | A workflow does not exist for the specified store, thus the `pizza-order` cannot be created |

#### Forwarding

adds the following fields to the initally received JSON object before forwarding it on to the next component or returning it back to the data source.

| field | type | required | description |
|-------|------|----------|-------------|
| valid | boolean | true | a field indicating if the recieved `pizza-order` is valid |


### `PUT /workflow-requests/<storeId>`

#### Parameters

| parameter | type | required | description |
|-----------|------|----------|-------------|
| storeId | string - format uuid | true | the id of the store issuing the workflow request |

#### Body

Requires a [`workflow-request`](https://github.com/CPVazquez/CS6343Linear/blob/main/Workflows/WF2/Components/C1/src/workflow-request.schema.json) JSON object. 

`workflow-request`

| field | type | options | required | description |
|-------|------|---------|----------|-------------|
| method | enum | persistent, edge | true | The workflow deployment method |
| component-list | enum array | order-verifier, cass, delivery-assigner, stock-analyzer, restocker, order-processor | true | The components the workflow is requesting |
| origin | string - format ip | N/A | true | The IP address of the host issuing the request |
| workflow-offset| integer | N/A | false | Generated by the workflow manager and passed to other components |

#### Responses

| status code | status | meaning|
|-------------|--------|--------|
| 201 | Created | The workflow was successfully created |
| 400 | Bad Request | Indicates the `workflow-request` was ill-formatted |
| 409 | Conflict | A workflow already exists for the specified store, and thus a new one cannot be created |
| 422 | Unprocessable Entity | Request JSON is valid, but the `workflow-request` specifies an unsupported workflow |

### `PUT /workflow-update/<storeId>`

#### Parameters

| parameter | type | required | description |
|-----------|------|----------|-------------|
| storeId | string - format uuid | true | the id of the store issuing the workflow request |

#### Body

Requires a [`workflow-request`](https://github.com/CPVazquez/CS6343Linear/blob/main/Workflows/WF2/Components/C1/src/workflow-request.schema.json) JSON object. 

`workflow-request`

| field | type | options | required | description |
|-------|------|---------|----------|-------------|
| method | enum | persistent, edge | true | The workflow deployment method |
| component-list | enum array | order-verifier, cass, delivery-assigner, stock-analyzer, restocker, order-processor | true | The components the workflow is requesting |
| origin | string - format ip | N/A | true | The IP address of the host issuing the request |
| workflow-offset| integer | N/A | false | Generated by the workflow manager and passed to other components |

#### Responses

| status code | status | meaning|
|-------------|--------|--------|
| 200 | OK | The workflow was successfully updated |
| 400 | Bad Request | Indicates the `workflow-request` was ill-formatted |
| 422 | Unprocessable Entity | Request JSON is valid, but the `workflow-request` specifies an unsupported workflow |

### `DELETE /workflow-requests/<storeId>`

#### Parameters

| parameter | type | required | description |
|-----------|------|----------|-------------|
| storeId | string - format uuid | true | The ID of the store whose workflow is to be deleted |

#### Responses

| status code | status | meaning|
|-------------|--------|--------|
| 204 | No Content | The specified workflow was deleted successfully |
| 404 | Not Found | The specified workflow does not exist or has already been deleted |

### `GET /workflow-requests/<storeId>`

#### Parameters

| parameter | type | required | description |
|-----------|------|----------|-------------|
| storeId | string - format uuid | true | The ID of the store whose workflow is to be retrieved |

#### Responses

| status code | status | meaning | 
|-------------|--------|---------|
| 200 | OK | Returns the `workflow-request` |
| 404 | Not Found | The specified `workflow-request` does not exist and could not be retrieved |

### `GET /workflow-requests`

#### Responses

| status code | status | meaning |
|-------------|--------|---------|
| 200 | OK | Returns all the `workflow-request`s on the order verifier component |

### `GET /health`

#### Responses

| status code | status | meaning |
|-------------|--------|---------|
| 200 | OK | The server is up and running |

Returns string `healthy` if the service is healthy.

[Main README](https://github.com/CPVazquez/CS6343Linear)
