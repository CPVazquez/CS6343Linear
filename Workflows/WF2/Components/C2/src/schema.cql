/**********************************************************************
author = "Carla Patricia Vazquez"
version = "1.0.0"
maintainer = "Carla Vazquez"
email = "cpv150030@utdallas.edu"
status = "Development"
***********************************************************************/

CREATE KEYSPACE IF NOT EXISTS pizza_grocery WITH REPLICATION = { 'class' : 'SimpleStrategy', 'replication_factor' : 1 };

USE pizza_grocery;

CREATE TABLE customers (
    customerName TEXT,
    latitude FLOAT,
    longitude FLOAT,
    PRIMARY KEY (customerName),
);

CREATE TABLE stores (
  storeID UUID,
  latitude FLOAT,
  longitude FLOAT,
  sellsPizza BOOLEAN,
  PRIMARY KEY (storeID)
);

CREATE TABLE items (
  name TEXT,
  price FLOAT,
  PRIMARY KEY (name),
); 

INSERT INTO items (name, price) VALUES ('Pepperoni', 1.50);
INSERT INTO items (name, price) VALUES ('Sausage', 1.55);
INSERT INTO items (name, price) VALUES ('Beef', 1.40);
INSERT INTO items (name, price) VALUES ('Onion', 0.30);
INSERT INTO items (name, price) VALUES ('Chicken', 1.35);
INSERT INTO items (name, price) VALUES ('Peppers', 0.55);
INSERT INTO items (name, price) VALUES ('Olives', 0.30);
INSERT INTO items (name, price) VALUES ('Bacon', 1.55); 
INSERT INTO items (name, price) VALUES ('Pineapple', 0.48);
INSERT INTO items (name, price) VALUES ('Mushrooms', 0.75);
INSERT INTO items (name, price) VALUES ('Dough', 4.00);
INSERT INTO items (name, price) VALUES ('Cheese', 1.00);
INSERT INTO items (name, price) VALUES ('SpicySauce', 1.10);
INSERT INTO items (name, price) VALUES ('TraditionalSauce', 1.20);

CREATE TABLE stock (
  storeID UUID,
  itemName TEXT,
  quantity FLOAT,
  PRIMARY KEY (storeID, itemName),
);

CREATE TABLE pizzas (
  pizzaID UUID,
  toppings SET<TUPLE<TEXT, INT>>,
  cost FLOAT,
  PRIMARY KEY (pizzaID)
);

CREATE TABLE deliveryEntitiesByStore (
  storeID UUID,
  name TEXT,
  latitude FLOAT,
  longitude FLOAT,
  status TEXT,
  onDelivery BOOLEAN,
  PRIMARY KEY (storeID, name)
);

CREATE TABLE payments (
    paymentToken UUID,
    method TEXT, 
    PRIMARY KEY (paymentToken)
);

CREATE TABLE orderTable (
  orderID UUID,
  orderedFrom UUID,
  orderedBy TEXT,
  deliveredBy TEXT,
  containsPizzas SET<UUID>,
  containsItems SET<TUPLE<TEXT, INT>>,
  paymentID UUID,
  placedAT TIMESTAMP,
  active BOOLEAN,
  estimatedDeliveryTime INT,
  PRIMARY KEY (orderID)
);

CREATE TABLE orderByStore (
  orderedFrom UUID,
  placedAT TIMESTAMP,
  orderID UUID,
  PRIMARY KEY (orderedFrom, orderID)
);

CREATE TABLE orderByDeliveryEntity (
  deliveredBy TEXT,
  placedAT TIMESTAMP,
  orderID UUID,
  PRIMARY KEY (deliveredBy, orderID)
);

CREATE TABLE stockTracker (
  storeID UUID,
  itemName TEXT,
  quantitySold FLOAT,
  dateSold TIMESTAMP,
  PRIMARY KEY (storeID, itemName, dateSold)
);

CREATE TABLE orderByCustomer (
  orderedBy TEXT,
  placedAT TIMESTAMP,
  orderID UUID,
  PRIMARY KEY (orderedBy, orderID)
);