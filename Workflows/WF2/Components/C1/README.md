# Pizza Order Verifier
Workflow 2, Component 1

## Written By
Christopher Michael Scott

## Description
This component receives pizza orders routed from the workflow manager (WFM). Orders are compliant with the pizza-order.schema.json format. Upon receiving an order, C1 validates the order, checks if sufficient stock exists, and if the stock exists, then it creates the order. If sufficient stock is not available, C1 creates a restock order and provides it as a response to the WFM.

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

## Commands
* To build the docker image, use the following command in the folder containing the Dockerfile:
  ```
  docker build --rm -t trishaire/order-verifier path_to_c1_dockerfile
  ```
* To update Dockerhub repository:

  ```
  sudo docker login
  docker push trishaire/order-verifier:tag
  ```

* To create the image as a service run the following command:

  ```
  docker service create --name order-verifier --network myNet --publish port:port --env CASS_DB=cass_service_vip trishaire/order-verifier
  ```

  * Where `port` is `1000` for order-verifier and `cass_service_vip` is the VIP of `myNet` overlay network.

## Endpoints

### `POST /order`

requires a [`pizza-order`](https://github.com/CPVazquez/CS6343/blob/master/Workflows/WF2/Components/C1/src/pizza-order.schema.json) json object

`pizza-order` 

| field | type | required | description |
|-------|------|-----------|--------------|
| storeId | string - format uuid | true | A base64 ID given to each store to identify it|
| custName | string | true | The name of the customer, as a single string for both first/last name |
| paymentToken | string - format uuid | true |The token for the third-party payment service that the customer is paying with|
| paymentTokenType | string | true |The type of token accepted (paypal, google pay, etc) |
| custLocation | `location` | true | The location of the customer, in degrees latitude and longitude |
| pizzaList | `pizza` array | true | The list of pizzas that have been ordered|

`location`

| field | type | required | description |
|-------|------|----------|---|
| lat | number | false | latitude |
| lon | number | false | longitude |

`pizza`
| field | type | options | required | description |
|-------|------|---------|----|---|
| crustType | enum | Thin, Traditional | false | The type of crust |
| sauceType | enum | Spicy, Traditional | false | The type of sauce |
| cheeseAmt | enum | None, Light, Normal, Extra | false | The amount of cheese on the pizza |
| toppingList | enum array | Pepperoni, Sausage, Beef, Onion, Chicken, Peppers, Olives, Bacon, Pineapple, Mushrooms | false | The list of toppings added at extra cost. Cost verified by server |

Responses

on `200 OK` returns a json object with the order id of the pizza order

on `403 Forbidden` returns a [`restock-order`](https://github.com/CPVazquez/CS6343/blob/master/Workflows/WF2/Components/C5/src/restock-order.schema.json) json object

### `GET /health`

returns string `healthy` if the service is healthy

[Main README](https://github.com/CPVazquez/CS6343)


