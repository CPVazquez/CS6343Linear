# Delivery Assigner

## Written By
Daniel Garcia

## Description
This component acts as the central manager for the workflow. It recieves the original requests from outside the system, from clients, and passes the data to the other components in the system. It maintains the inter-operation data flow between the order-verifier, delivery-assigner, and restocker components

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

### `POST /orders

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

Will return a `200 OK` if the pizza order has been accepted.


requires a json object with order_id

| field | type | required | description |
|-------|------|----------|---|
| order_id |string - format uuid| true |the id of the order that we are assigning an entity to|

### `GET /health`
returns string `healthy` if the service is healthy

[Main README](https://github.com/CPVazquez/CS6343)

