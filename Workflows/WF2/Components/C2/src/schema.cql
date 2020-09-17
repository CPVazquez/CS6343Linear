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

INSERT INTO stores (storeID, latitude, longitude, sellsPizza) VALUES (7098813e-4624-462a-81a1-7e0e4e67631d, 32.8456, -96.9172, true);
INSERT INTO stores (storeID, latitude, longitude, sellsPizza) VALUES (5a2bb99f-88d2-4612-ac60-774aea9b8de4, 30.2672, -97.7431, true);
INSERT INTO stores (storeID, latitude, longitude, sellsPizza) VALUES (b18b3932-a4ef-485c-a182-8e67b04c208c, 29.7604, -95.3698, true);

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

INSERT INTO stock (storeID, itemName, quantity) VALUES (7098813e-4624-462a-81a1-7e0e4e67631d, 'Pepperoni', 20);
INSERT INTO stock (storeID, itemName, quantity) VALUES (7098813e-4624-462a-81a1-7e0e4e67631d, 'Sausage', 20);
INSERT INTO stock (storeID, itemName, quantity) VALUES (7098813e-4624-462a-81a1-7e0e4e67631d, 'Beef', 20);
INSERT INTO stock (storeID, itemName, quantity) VALUES (7098813e-4624-462a-81a1-7e0e4e67631d, 'Onion', 20);
INSERT INTO stock (storeID, itemName, quantity) VALUES (7098813e-4624-462a-81a1-7e0e4e67631d, 'Chicken', 20);
INSERT INTO stock (storeID, itemName, quantity) VALUES (7098813e-4624-462a-81a1-7e0e4e67631d, 'Peppers', 20);
INSERT INTO stock (storeID, itemName, quantity) VALUES (7098813e-4624-462a-81a1-7e0e4e67631d, 'Olives', 20);
INSERT INTO stock (storeID, itemName, quantity) VALUES (7098813e-4624-462a-81a1-7e0e4e67631d, 'Bacon', 20); 
INSERT INTO stock (storeID, itemName, quantity) VALUES (7098813e-4624-462a-81a1-7e0e4e67631d, 'Pineapple', 20);
INSERT INTO stock (storeID, itemName, quantity) VALUES (7098813e-4624-462a-81a1-7e0e4e67631d, 'Mushrooms', 20);
INSERT INTO stock (storeID, itemName, quantity) VALUES (7098813e-4624-462a-81a1-7e0e4e67631d, 'Dough', 20);
INSERT INTO stock (storeID, itemName, quantity) VALUES (7098813e-4624-462a-81a1-7e0e4e67631d, 'Cheese', 20);
INSERT INTO stock (storeID, itemName, quantity) VALUES (7098813e-4624-462a-81a1-7e0e4e67631d, 'SpicySauce', 20);
INSERT INTO stock (storeID, itemName, quantity) VALUES (7098813e-4624-462a-81a1-7e0e4e67631d, 'TraditionalSauce', 20);

INSERT INTO stock (storeID, itemName, quantity) VALUES (5a2bb99f-88d2-4612-ac60-774aea9b8de4, 'Pepperoni', 20);
INSERT INTO stock (storeID, itemName, quantity) VALUES (5a2bb99f-88d2-4612-ac60-774aea9b8de4, 'Sausage', 20);
INSERT INTO stock (storeID, itemName, quantity) VALUES (5a2bb99f-88d2-4612-ac60-774aea9b8de4, 'Beef', 20);
INSERT INTO stock (storeID, itemName, quantity) VALUES (5a2bb99f-88d2-4612-ac60-774aea9b8de4, 'Onion', 20);
INSERT INTO stock (storeID, itemName, quantity) VALUES (5a2bb99f-88d2-4612-ac60-774aea9b8de4, 'Chicken', 20);
INSERT INTO stock (storeID, itemName, quantity) VALUES (5a2bb99f-88d2-4612-ac60-774aea9b8de4, 'Peppers', 20);
INSERT INTO stock (storeID, itemName, quantity) VALUES (5a2bb99f-88d2-4612-ac60-774aea9b8de4, 'Olives', 20);
INSERT INTO stock (storeID, itemName, quantity) VALUES (5a2bb99f-88d2-4612-ac60-774aea9b8de4, 'Bacon', 20); 
INSERT INTO stock (storeID, itemName, quantity) VALUES (5a2bb99f-88d2-4612-ac60-774aea9b8de4, 'Pineapple', 20);
INSERT INTO stock (storeID, itemName, quantity) VALUES (5a2bb99f-88d2-4612-ac60-774aea9b8de4, 'Mushrooms', 20);
INSERT INTO stock (storeID, itemName, quantity) VALUES (5a2bb99f-88d2-4612-ac60-774aea9b8de4, 'Dough', 20);
INSERT INTO stock (storeID, itemName, quantity) VALUES (5a2bb99f-88d2-4612-ac60-774aea9b8de4, 'Cheese', 20);
INSERT INTO stock (storeID, itemName, quantity) VALUES (5a2bb99f-88d2-4612-ac60-774aea9b8de4, 'SpicySauce', 20);
INSERT INTO stock (storeID, itemName, quantity) VALUES (5a2bb99f-88d2-4612-ac60-774aea9b8de4, 'TraditionalSauce', 20);

INSERT INTO stock (storeID, itemName, quantity) VALUES (b18b3932-a4ef-485c-a182-8e67b04c208c, 'Pepperoni', 20);
INSERT INTO stock (storeID, itemName, quantity) VALUES (b18b3932-a4ef-485c-a182-8e67b04c208c, 'Sausage', 20);
INSERT INTO stock (storeID, itemName, quantity) VALUES (b18b3932-a4ef-485c-a182-8e67b04c208c, 'Beef', 20);
INSERT INTO stock (storeID, itemName, quantity) VALUES (b18b3932-a4ef-485c-a182-8e67b04c208c, 'Onion', 20);
INSERT INTO stock (storeID, itemName, quantity) VALUES (b18b3932-a4ef-485c-a182-8e67b04c208c, 'Chicken', 20);
INSERT INTO stock (storeID, itemName, quantity) VALUES (b18b3932-a4ef-485c-a182-8e67b04c208c, 'Peppers', 20);
INSERT INTO stock (storeID, itemName, quantity) VALUES (b18b3932-a4ef-485c-a182-8e67b04c208c, 'Olives', 20);
INSERT INTO stock (storeID, itemName, quantity) VALUES (b18b3932-a4ef-485c-a182-8e67b04c208c, 'Bacon', 20); 
INSERT INTO stock (storeID, itemName, quantity) VALUES (b18b3932-a4ef-485c-a182-8e67b04c208c, 'Pineapple', 20);
INSERT INTO stock (storeID, itemName, quantity) VALUES (b18b3932-a4ef-485c-a182-8e67b04c208c, 'Mushrooms', 20);
INSERT INTO stock (storeID, itemName, quantity) VALUES (b18b3932-a4ef-485c-a182-8e67b04c208c, 'Dough', 20);
INSERT INTO stock (storeID, itemName, quantity) VALUES (b18b3932-a4ef-485c-a182-8e67b04c208c, 'Cheese', 20);
INSERT INTO stock (storeID, itemName, quantity) VALUES (b18b3932-a4ef-485c-a182-8e67b04c208c, 'SpicySauce', 20);
INSERT INTO stock (storeID, itemName, quantity) VALUES (b18b3932-a4ef-485c-a182-8e67b04c208c, 'TraditionalSauce', 20);

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

INSERT INTO deliveryEntitiesByStore (storeID, name, latitude, longitude, status, onDelivery) VALUES (7098813e-4624-462a-81a1-7e0e4e67631d, 'de11', 32.8456, -96.9172, 'AVAILABLE', false);
INSERT INTO deliveryEntitiesByStore (storeID, name, latitude, longitude, status, onDelivery) VALUES (7098813e-4624-462a-81a1-7e0e4e67631d, 'de12', 32.8456, -96.9172, 'AVAILABLE', false);
INSERT INTO deliveryEntitiesByStore (storeID, name, latitude, longitude, status, onDelivery) VALUES (7098813e-4624-462a-81a1-7e0e4e67631d, 'de13', 32.8456, -96.9172, 'AVAILABLE', false);
INSERT INTO deliveryEntitiesByStore (storeID, name, latitude, longitude, status, onDelivery) VALUES (7098813e-4624-462a-81a1-7e0e4e67631d, 'de14', 32.8456, -96.9172, 'AVAILABLE', false);
INSERT INTO deliveryEntitiesByStore (storeID, name, latitude, longitude, status, onDelivery) VALUES (7098813e-4624-462a-81a1-7e0e4e67631d, 'de15', 32.8456, -96.9172, 'AVAILABLE', false);

INSERT INTO deliveryEntitiesByStore (storeID, name, latitude, longitude, status, onDelivery) VALUES (5a2bb99f-88d2-4612-ac60-774aea9b8de4, 'de21', 30.2672, -97.7431, 'AVAILABLE', false);
INSERT INTO deliveryEntitiesByStore (storeID, name, latitude, longitude, status, onDelivery) VALUES (5a2bb99f-88d2-4612-ac60-774aea9b8de4, 'de22', 30.2672, -97.7431, 'AVAILABLE', false);
INSERT INTO deliveryEntitiesByStore (storeID, name, latitude, longitude, status, onDelivery) VALUES (5a2bb99f-88d2-4612-ac60-774aea9b8de4, 'de23', 30.2672, -97.7431, 'AVAILABLE', false);
INSERT INTO deliveryEntitiesByStore (storeID, name, latitude, longitude, status, onDelivery) VALUES (5a2bb99f-88d2-4612-ac60-774aea9b8de4, 'de24', 30.2672, -97.7431, 'AVAILABLE', false);
INSERT INTO deliveryEntitiesByStore (storeID, name, latitude, longitude, status, onDelivery) VALUES (5a2bb99f-88d2-4612-ac60-774aea9b8de4, 'de25', 30.2672, -97.7431, 'AVAILABLE', false);

INSERT INTO deliveryEntitiesByStore (storeID, name, latitude, longitude, status, onDelivery) VALUES (b18b3932-a4ef-485c-a182-8e67b04c208c, 'de31', 29.7604, -95.3698, 'AVAILABLE', false);
INSERT INTO deliveryEntitiesByStore (storeID, name, latitude, longitude, status, onDelivery) VALUES (b18b3932-a4ef-485c-a182-8e67b04c208c, 'de32', 29.7604, -95.3698, 'AVAILABLE', false);
INSERT INTO deliveryEntitiesByStore (storeID, name, latitude, longitude, status, onDelivery) VALUES (b18b3932-a4ef-485c-a182-8e67b04c208c, 'de33', 29.7604, -95.3698, 'AVAILABLE', false);
INSERT INTO deliveryEntitiesByStore (storeID, name, latitude, longitude, status, onDelivery) VALUES (b18b3932-a4ef-485c-a182-8e67b04c208c, 'de34', 29.7604, -95.3698, 'AVAILABLE', false);
INSERT INTO deliveryEntitiesByStore (storeID, name, latitude, longitude, status, onDelivery) VALUES (b18b3932-a4ef-485c-a182-8e67b04c208c, 'de35', 29.7604, -95.3698, 'AVAILABLE', false);

CREATE TABLE payments (
    paymentToken UUID,
    method TEXT, 
    PRIMARY KEY (paymentToken)
);

CREATE TABLE orderTable (
  orderID UUID,
  orderedFrom UUID,
  orderedBy TEXT,
  delivieredBy TEXT,
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