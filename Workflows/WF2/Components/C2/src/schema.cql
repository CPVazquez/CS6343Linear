CREATE KEYSPACE IF NOT EXISTS pizza_grocery
WITH REPLICATION = { 'class' : 'SimpleStrategy', 'replication_factor' : 3 };

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

INSERT INTO stores (storeID, latitude, longitude, sellsPizza) VALUES ('7098813e-4624-462a-81a1-7e0e4e67631d', 32.8456, -96.9172, true);
INSERT INTO stores (storeID, latitude, longitude, sellsPizza) VALUES ('5a2bb99f-88d2-4612-ac60-774aea9b8de4', 30.2672, -97.7431, true);
INSERT INTO stores (storeID, latitude, longitude, sellsPizza) VALUES ('b18b3932-a4ef-485c-a182-8e67b04c208c', 29.7604, -95.3698, true);

CREATE TABLE items (
  name TEXT,
  price FLOAT,
  PRIMARY KEY (name),
); 

INSERT INTO items (name, price) VALUES ("Pepperoni", 1.50);
INSERT INTO items (name, price) VALUES ("Sausage", 1.55);
INSERT INTO items (name, price) VALUES ("Beef", 1.40);
INSERT INTO items (name, price) VALUES ("Onion", 0.30);
INSERT INTO items (name, price) VALUES ("Chicken", 1.35);
INSERT INTO items (name, price) VALUES ("Peppers", 0.55);
INSERT INTO items (name, price) VALUES ("Olives", 0.30);
INSERT INTO items (name, price) VALUES ("Bacon", 1.55); 
INSERT INTO items (name, price) VALUES ("Pineapple", 0.48);
INSERT INTO items (name, price) VALUES ("Mushrooms", 0.75);
INSERT INTO items (name, price) VALUES ("Dough", 4.00);
INSERT INTO items (name, price) VALUES ("Cheese", 1.00);
INSERT INTO items (name, price) VALUES ("SpicySauce", 1.10);
INSERT INTO items (name, price) VALUES ("TraditionalSauce", 1.20);

CREATE TABLE stock (
  storeID UUID,
  itemName TEXT,
  quantity FLOAT,
  PRIMARY KEY (storeID, itemName),
);

BEGIN BATCH
INSERT INTO items (name, price) VALUES ('7098813e-4624-462a-81a1-7e0e4e67631d', "Pepperoni", 20);
INSERT INTO items (name, price) VALUES ('7098813e-4624-462a-81a1-7e0e4e67631d', "Sausage", 20);
INSERT INTO items (name, price) VALUES ('7098813e-4624-462a-81a1-7e0e4e67631d', "Beef", 20);
INSERT INTO items (name, price) VALUES ('7098813e-4624-462a-81a1-7e0e4e67631d', "Onion", 20);
INSERT INTO items (name, price) VALUES ('7098813e-4624-462a-81a1-7e0e4e67631d', "Chicken", 20);
INSERT INTO items (name, price) VALUES ('7098813e-4624-462a-81a1-7e0e4e67631d', "Peppers", 20);
INSERT INTO items (name, price) VALUES ('7098813e-4624-462a-81a1-7e0e4e67631d', "Olives", 20);
INSERT INTO items (name, price) VALUES ('7098813e-4624-462a-81a1-7e0e4e67631d', "Bacon", 20); 
INSERT INTO items (name, price) VALUES ('7098813e-4624-462a-81a1-7e0e4e67631d', "Pineapple", 20);
INSERT INTO items (name, price) VALUES ('7098813e-4624-462a-81a1-7e0e4e67631d', "Mushrooms", 20);
INSERT INTO items (name, price) VALUES ('7098813e-4624-462a-81a1-7e0e4e67631d', "Dough", 20);
INSERT INTO items (name, price) VALUES ('7098813e-4624-462a-81a1-7e0e4e67631d', "Cheese", 20);
INSERT INTO items (name, price) VALUES ('7098813e-4624-462a-81a1-7e0e4e67631d', "SpicySauce", 20);
INSERT INTO items (name, price) VALUES ('7098813e-4624-462a-81a1-7e0e4e67631d', "TraditionalSauce", 20);
APPLY BATCH;

BEGIN BATCH
INSERT INTO items (name, price) VALUES ('5a2bb99f-88d2-4612-ac60-774aea9b8de4', "Pepperoni", 20);
INSERT INTO items (name, price) VALUES ('5a2bb99f-88d2-4612-ac60-774aea9b8de4', "Sausage", 20);
INSERT INTO items (name, price) VALUES ('5a2bb99f-88d2-4612-ac60-774aea9b8de4', "Beef", 20);
INSERT INTO items (name, price) VALUES ('5a2bb99f-88d2-4612-ac60-774aea9b8de4', "Onion", 20);
INSERT INTO items (name, price) VALUES ('5a2bb99f-88d2-4612-ac60-774aea9b8de4', "Chicken", 20);
INSERT INTO items (name, price) VALUES ('5a2bb99f-88d2-4612-ac60-774aea9b8de4', "Peppers", 20);
INSERT INTO items (name, price) VALUES ('5a2bb99f-88d2-4612-ac60-774aea9b8de4', "Olives", 20);
INSERT INTO items (name, price) VALUES ('5a2bb99f-88d2-4612-ac60-774aea9b8de4', "Bacon", 20); 
INSERT INTO items (name, price) VALUES ('5a2bb99f-88d2-4612-ac60-774aea9b8de4', "Pineapple", 20);
INSERT INTO items (name, price) VALUES ('5a2bb99f-88d2-4612-ac60-774aea9b8de4', "Mushrooms", 20);
INSERT INTO items (name, price) VALUES ('5a2bb99f-88d2-4612-ac60-774aea9b8de4', "Dough", 20);
INSERT INTO items (name, price) VALUES ('5a2bb99f-88d2-4612-ac60-774aea9b8de4', "Cheese", 20);
INSERT INTO items (name, price) VALUES ('5a2bb99f-88d2-4612-ac60-774aea9b8de4', "SpicySauce", 20);
INSERT INTO items (name, price) VALUES ('5a2bb99f-88d2-4612-ac60-774aea9b8de4', "TraditionalSauce", 20);
APPLY BATCH;

BEGIN BATCH
INSERT INTO items (name, price) VALUES ('b18b3932-a4ef-485c-a182-8e67b04c208c', "Pepperoni", 20);
INSERT INTO items (name, price) VALUES ('b18b3932-a4ef-485c-a182-8e67b04c208c', "Sausage", 20);
INSERT INTO items (name, price) VALUES ('b18b3932-a4ef-485c-a182-8e67b04c208c', "Beef", 20);
INSERT INTO items (name, price) VALUES ('b18b3932-a4ef-485c-a182-8e67b04c208c', "Onion", 20);
INSERT INTO items (name, price) VALUES ('b18b3932-a4ef-485c-a182-8e67b04c208c', "Chicken", 20);
INSERT INTO items (name, price) VALUES ('b18b3932-a4ef-485c-a182-8e67b04c208c', "Peppers", 20);
INSERT INTO items (name, price) VALUES ('b18b3932-a4ef-485c-a182-8e67b04c208c', "Olives", 20);
INSERT INTO items (name, price) VALUES ('b18b3932-a4ef-485c-a182-8e67b04c208c', "Bacon", 20); 
INSERT INTO items (name, price) VALUES ('b18b3932-a4ef-485c-a182-8e67b04c208c', "Pineapple", 20);
INSERT INTO items (name, price) VALUES ('b18b3932-a4ef-485c-a182-8e67b04c208c', "Mushrooms", 20);
INSERT INTO items (name, price) VALUES ('b18b3932-a4ef-485c-a182-8e67b04c208c', "Dough", 20);
INSERT INTO items (name, price) VALUES ('b18b3932-a4ef-485c-a182-8e67b04c208c', "Cheese", 20);
INSERT INTO items (name, price) VALUES ('b18b3932-a4ef-485c-a182-8e67b04c208c', "SpicySauce", 20);
INSERT INTO items (name, price) VALUES ('b18b3932-a4ef-485c-a182-8e67b04c208c', "TraditionalSauce", 20);
APPLY BATCH;

CREATE TABLE pizzas (
  pizzaID UUID,
  toppings SET<TUPLE<TEXT, INT>>,
  cost FLOAT,
  PRIMARY KEY (pizzaID)
);

CREATE TABLE deliveryEntitesByStore (
  storeID UUID,
  name TEXT,
  latitude FLOAT
  longitude FLOAT,
  status TEXT,
  onDelivery BOOLEAN,
  PRIMARY KEY (storeID, name)
);

BEGIN BATCH
INSERT INTO stores (storeID, latitude, longitude, onDelivery, name, staus) VALUES ('7098813e-4624-462a-81a1-7e0e4e67631d', 32.8456, -96.9172, false, 'de11', 'AVAILABLE' );
INSERT INTO stores (storeID, latitude, longitude, onDelivery, name, staus) VALUES ('7098813e-4624-462a-81a1-7e0e4e67631d', 32.8456, -96.9172, false, 'de12', 'AVAILABLE' );
INSERT INTO stores (storeID, latitude, longitude, onDelivery, name, staus) VALUES ('7098813e-4624-462a-81a1-7e0e4e67631d', 32.8456, -96.9172, false, 'de13', 'AVAILABLE' );
INSERT INTO stores (storeID, latitude, longitude, onDelivery, name, staus) VALUES ('7098813e-4624-462a-81a1-7e0e4e67631d', 32.8456, -96.9172, false, 'de14', 'AVAILABLE' );
INSERT INTO stores (storeID, latitude, longitude, onDelivery, name, staus) VALUES ('7098813e-4624-462a-81a1-7e0e4e67631d', 32.8456, -96.9172, false, 'de15', 'AVAILABLE' );
APPLY BATCH;

BEGIN BATCH
INSERT INTO stores (storeID, latitude, longitude, onDelivery, name, staus) VALUES ('5a2bb99f-88d2-4612-ac60-774aea9b8de4', 30.2672, -97.7431, false, 'de21', 'AVAILABLE' );
INSERT INTO stores (storeID, latitude, longitude, onDelivery, name, staus) VALUES ('5a2bb99f-88d2-4612-ac60-774aea9b8de4', 30.2672, -97.7431, false, 'de22', 'AVAILABLE' );
INSERT INTO stores (storeID, latitude, longitude, onDelivery, name, staus) VALUES ('5a2bb99f-88d2-4612-ac60-774aea9b8de4', 30.2672, -97.7431, false, 'de23', 'AVAILABLE' );
INSERT INTO stores (storeID, latitude, longitude, onDelivery, name, staus) VALUES ('5a2bb99f-88d2-4612-ac60-774aea9b8de4', 30.2672, -97.7431, false, 'de24', 'AVAILABLE' );
INSERT INTO stores (storeID, latitude, longitude, onDelivery, name, staus) VALUES ('5a2bb99f-88d2-4612-ac60-774aea9b8de4', 30.2672, -97.7431, false, 'de25', 'AVAILABLE' );
APPLY BATCH;

BEGIN BATCH
INSERT INTO stores (storeID, latitude, longitude, onDelivery, name, staus) VALUES ('b18b3932-a4ef-485c-a182-8e67b04c208c', 29.7604, -95.3698, false, 'de31', 'AVAILABLE' );
INSERT INTO stores (storeID, latitude, longitude, onDelivery, name, staus) VALUES ('b18b3932-a4ef-485c-a182-8e67b04c208c', 29.7604, -95.3698, false, 'de32', 'AVAILABLE' );
INSERT INTO stores (storeID, latitude, longitude, onDelivery, name, staus) VALUES ('b18b3932-a4ef-485c-a182-8e67b04c208c', 29.7604, -95.3698, false, 'de33', 'AVAILABLE' );
INSERT INTO stores (storeID, latitude, longitude, onDelivery, name, staus) VALUES ('b18b3932-a4ef-485c-a182-8e67b04c208c', 29.7604, -95.3698, false, 'de34', 'AVAILABLE' );
INSERT INTO stores (storeID, latitude, longitude, onDelivery, name, staus) VALUES ('b18b3932-a4ef-485c-a182-8e67b04c208c', 29.7604, -95.3698, false, 'de35', 'AVAILABLE' );
APPLY BATCH;


CREATE TABLE payments (
    paymentToken UUID,
    method TEXT, 
    PRIMARY KEY (storeID)
);

CREATE TABLE order (
  orderID UUID,
  orderedFrom UUID,
  orderedBy TEXT,
  delivieredBy TEXT,
  containsPizzas SET<UUID>,
  containsItems SET<TUPLE<TEXT, IN>>
  paymentID UUID,
  placedAT TIMESTAMP,
  active BOOLEAN,
  PRIMARY KEY (orderID)
);

CREATE TABLE orderByStore (
  orderedFrom UUID,
  placedAT TIMESTAMP,
  orderID UUID,
  PRIMARY KEY (orderedFrom, placedAt)
);

CREATE TABLE orderByDeliveryEntity (
  deliveredBy TEXT,
  placedAT TIMESTAMP,
  orderID UUID,
  PRIMARY KEY (deliveredBy, placedAt)
);

CREATE TABLE orderByCustomer (
  orderedBy TEXT,
  placedAT TIMESTAMP,
  orderID UUID,
  PRIMARY KEY (orderedBy, placedAt)
);