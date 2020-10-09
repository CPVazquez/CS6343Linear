CREATE KEYSPACE IF NOT EXISTS pizza_grocery WITH REPLICATION = { 'class' : 'SimpleStrategy', 'replication_factor' : 1 };

USE pizza_grocery;

CREATE TABLE customers (
    customerName TEXT,
    latitude FLOAT,
    longitude FLOAT,
    PRIMARY KEY (customerName),
);

INSERT INTO customers (customerName, latitude, longitude) VALUES ('Anthony Miller',30.26176,-97.73457);
INSERT INTO customers (customerName, latitude, longitude) VALUES ('Morgan Thompson',30.2638,-97.72597);
INSERT INTO customers (customerName, latitude, longitude) VALUES ('Hunter Kim',29.73321,-95.40461);
INSERT INTO customers (customerName, latitude, longitude) VALUES ('David Nelson',29.75352,-95.39684);
INSERT INTO customers (customerName, latitude, longitude) VALUES ('Jennifer Wilkinson',29.79121,-95.3514);
INSERT INTO customers (customerName, latitude, longitude) VALUES ('Jesse Perry',30.26297,-97.77579);
INSERT INTO customers (customerName, latitude, longitude) VALUES ('Kurt Arnold',29.79149,-95.33107);
INSERT INTO customers (customerName, latitude, longitude) VALUES ('Nathan Reeves',30.28704,-97.72945);
INSERT INTO customers (customerName, latitude, longitude) VALUES ('Denise Nelson',29.75094,-95.41026);
INSERT INTO customers (customerName, latitude, longitude) VALUES ('Alyssa Perez',30.25427,-97.77854);
INSERT INTO customers (customerName, latitude, longitude) VALUES ('Jill Munoz',30.2779,-97.70059);
INSERT INTO customers (customerName, latitude, longitude) VALUES ('Michael Smith',30.24684,-97.70508);
INSERT INTO customers (customerName, latitude, longitude) VALUES ('Lucas Cole',29.73754,-95.39371);
INSERT INTO customers (customerName, latitude, longitude) VALUES ('Angela Green',29.72578,-95.38822 );
INSERT INTO customers (customerName, latitude, longitude) VALUES ('Amy Medina',30.23283,-97.71931 );
INSERT INTO customers (customerName, latitude, longitude) VALUES ('Scott Hogan',30.30047,-97.7571 );
INSERT INTO customers (customerName, latitude, longitude) VALUES ('Ronald Cline',30.27807,-97.71537 );
INSERT INTO customers (customerName, latitude, longitude) VALUES ('Brian Moon',30.30329,-97.73475 );
INSERT INTO customers (customerName, latitude, longitude) VALUES ('Sarah Smith',29.77481,-95.37859 );
INSERT INTO customers (customerName, latitude, longitude) VALUES ('Gwendolyn Mclaughlin',30.29523,-97.78395 );
INSERT INTO customers (customerName, latitude, longitude) VALUES ('Emily Wolfe',30.26829,-97.71228 );
INSERT INTO customers (customerName, latitude, longitude) VALUES ('Melissa Jones',29.74267,-95.36998 );
INSERT INTO customers (customerName, latitude, longitude) VALUES ('Margaret Hunter',32.83497,-96.88453 );
INSERT INTO customers (customerName, latitude, longitude) VALUES ('Joshua Stafford',29.74524,-95.34953 );
INSERT INTO customers (customerName, latitude, longitude) VALUES ('Maurice Reid',29.78186,-95.36332 );
INSERT INTO customers (customerName, latitude, longitude) VALUES ('Daniel Miller',32.81852,-96.95831 );
INSERT INTO customers (customerName, latitude, longitude) VALUES ('Brooke Bush',32.82962,-96.91604 );
INSERT INTO customers (customerName, latitude, longitude) VALUES ('Joseph Reed',32.81456,-96.94672 );
INSERT INTO customers (customerName, latitude, longitude) VALUES ('Jennifer Martin',30.29321,-97.71175 );
INSERT INTO customers (customerName, latitude, longitude) VALUES ('Emily Hudson',30.24763,-97.72199 );
INSERT INTO customers (customerName, latitude, longitude) VALUES ('Isabel Reed',29.76982,-95.35915 );
INSERT INTO customers (customerName, latitude, longitude) VALUES ('Cody Harrison',32.82426,-96.90405 );
INSERT INTO customers (customerName, latitude, longitude) VALUES ('Lisa Bolton',32.87053,-96.93417 );
INSERT INTO customers (customerName, latitude, longitude) VALUES ('Terry Barnes MD',29.79492,-95.38358 );
INSERT INTO customers (customerName, latitude, longitude) VALUES ('Jack Collins',29.73439,-95.34576 );
INSERT INTO customers (customerName, latitude, longitude) VALUES ('Benjamin Frye',29.72507,-95.38754 );
INSERT INTO customers (customerName, latitude, longitude) VALUES ('Jonathan Perry',30.29335,-97.77359 );
INSERT INTO customers (customerName, latitude, longitude) VALUES ('Chelsea Garrett',30.29776,-97.74428 );
INSERT INTO customers (customerName, latitude, longitude) VALUES ('Joseph Hawkins',29.78259,-95.36423 );
INSERT INTO customers (customerName, latitude, longitude) VALUES ('Tyler Turner',29.72351,-95.35045 );
INSERT INTO customers (customerName, latitude, longitude) VALUES ('Luke Meyer',30.27855,-97.75488 );
INSERT INTO customers (customerName, latitude, longitude) VALUES ('Joseph Johnson',29.75021,-95.3512 );
INSERT INTO customers (customerName, latitude, longitude) VALUES ('Grant Vega',29.75117,-95.37687 );
INSERT INTO customers (customerName, latitude, longitude) VALUES ('Kimberly Branch',29.76375,-95.37845 );
INSERT INTO customers (customerName, latitude, longitude) VALUES ('Daniel Moore',30.30387,-97.76083 );
INSERT INTO customers (customerName, latitude, longitude) VALUES ('Nathan Waters',32.88145,-96.88831 );
INSERT INTO customers (customerName, latitude, longitude) VALUES ('Alexandra Small',32.87744,-96.88423 );
INSERT INTO customers (customerName, latitude, longitude) VALUES ('Amanda Webb',30.29546,-97.72617 );
INSERT INTO customers (customerName, latitude, longitude) VALUES ('Mary Mullen',32.82415,-96.92969);
INSERT INTO customers (customerName, latitude, longitude) VALUES ('Eugene Barr',30.29772,-97.73853);
INSERT INTO customers (customerName, latitude, longitude) VALUES ('Jacob Garcia',29.73288,-95.39571);
INSERT INTO customers (customerName, latitude, longitude) VALUES ('Ashley Smith',32.86029,-96.9067);
INSERT INTO customers (customerName, latitude, longitude) VALUES ('Jacqueline Copeland MD',29.73975,-95.37524);
INSERT INTO customers (customerName, latitude, longitude) VALUES ('Mary Weaver',30.26309,-97.74831);
INSERT INTO customers (customerName, latitude, longitude) VALUES ('Timothy Smith',32.8637,-96.95349);
INSERT INTO customers (customerName, latitude, longitude) VALUES ('Desiree Rush',30.24092,-97.77398);
INSERT INTO customers (customerName, latitude, longitude) VALUES ('Debra Andrews',29.75389,-95.34531);
INSERT INTO customers (customerName, latitude, longitude) VALUES ('Taylor Stone',29.72498,-95.35788);
INSERT INTO customers (customerName, latitude, longitude) VALUES ('Cassidy Stewart',32.85397,-96.9465);
INSERT INTO customers (customerName, latitude, longitude) VALUES ('Amanda Allen',32.82464,-96.94884);
INSERT INTO customers (customerName, latitude, longitude) VALUES ('Jessica Thomas DVM',30.26535,-97.76009);
INSERT INTO customers (customerName, latitude, longitude) VALUES ('Sarah Henderson',30.29298,-97.7095);
INSERT INTO customers (customerName, latitude, longitude) VALUES ('Eric Douglas',30.28952,-97.77178);
INSERT INTO customers (customerName, latitude, longitude) VALUES ('Amanda Mccullough',30.27482,-97.73154);
INSERT INTO customers (customerName, latitude, longitude) VALUES ('Steven Newman',29.78586,-95.36748);
INSERT INTO customers (customerName, latitude, longitude) VALUES ('Jacqueline Todd',32.8651,-96.90797);
INSERT INTO customers (customerName, latitude, longitude) VALUES ('Tracy Smith',29.79408,-95.3362);
INSERT INTO customers (customerName, latitude, longitude) VALUES ('Scott Flores',29.73766,-95.34269);
INSERT INTO customers (customerName, latitude, longitude) VALUES ('Tracy Henderson',30.28251,-97.73309);
INSERT INTO customers (customerName, latitude, longitude) VALUES ('Joseph Nichols',32.83743,-96.92773);
INSERT INTO customers (customerName, latitude, longitude) VALUES ('Linda Jensen',29.72352,-95.35609);
INSERT INTO customers (customerName, latitude, longitude) VALUES ('Daniel Dixon',29.78858,-95.40022);
INSERT INTO customers (customerName, latitude, longitude) VALUES ('Karen Franco',30.24366,-97.70924);
INSERT INTO customers (customerName, latitude, longitude) VALUES ('Jessica Christensen',29.78495,-95.40834);
INSERT INTO customers (customerName, latitude, longitude) VALUES ('Tricia Davenport',29.77654,-95.36301);
INSERT INTO customers (customerName, latitude, longitude) VALUES ('David Lara',29.78435,-95.40971);
INSERT INTO customers (customerName, latitude, longitude) VALUES ('Jeffery Stanton',29.72536,-95.34847);
INSERT INTO customers (customerName, latitude, longitude) VALUES ('Sandra Marshall',30.27114,-97.72049);
INSERT INTO customers (customerName, latitude, longitude) VALUES ('Christopher Soto',29.79156,-95.39724);
INSERT INTO customers (customerName, latitude, longitude) VALUES ('Brittany Turner',32.87519,-96.90145);

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

INSERT INTO stock (storeID, itemName, quantity) VALUES (7098813e-4624-462a-81a1-7e0e4e67631d,'Bacon',93);
INSERT INTO stock (storeID, itemName, quantity) VALUES (7098813e-4624-462a-81a1-7e0e4e67631d,'Beef',90);
INSERT INTO stock (storeID, itemName, quantity) VALUES (7098813e-4624-462a-81a1-7e0e4e67631d,'Cheese',75);
INSERT INTO stock (storeID, itemName, quantity) VALUES (7098813e-4624-462a-81a1-7e0e4e67631d,'Chicken',91);
INSERT INTO stock (storeID, itemName, quantity) VALUES (7098813e-4624-462a-81a1-7e0e4e67631d,'Dough',74);
INSERT INTO stock (storeID, itemName, quantity) VALUES (7098813e-4624-462a-81a1-7e0e4e67631d,'Mushrooms',91);
INSERT INTO stock (storeID, itemName, quantity) VALUES (7098813e-4624-462a-81a1-7e0e4e67631d,'Olives',94);
INSERT INTO stock (storeID, itemName, quantity) VALUES (7098813e-4624-462a-81a1-7e0e4e67631d,'Onion',94);
INSERT INTO stock (storeID, itemName, quantity) VALUES (7098813e-4624-462a-81a1-7e0e4e67631d,'Pepperoni',92);
INSERT INTO stock (storeID, itemName, quantity) VALUES (7098813e-4624-462a-81a1-7e0e4e67631d,'Peppers',94);
INSERT INTO stock (storeID, itemName, quantity) VALUES (7098813e-4624-462a-81a1-7e0e4e67631d,'Pineapple',93);
INSERT INTO stock (storeID, itemName, quantity) VALUES (7098813e-4624-462a-81a1-7e0e4e67631d,'Sausage',95);
INSERT INTO stock (storeID, itemName, quantity) VALUES (7098813e-4624-462a-81a1-7e0e4e67631d,'SpicySauce',93);
INSERT INTO stock (storeID, itemName, quantity) VALUES (7098813e-4624-462a-81a1-7e0e4e67631d,'TraditionalSauce',91);
INSERT INTO stock (storeID, itemName, quantity) VALUES (b18b3932-a4ef-485c-a182-8e67b04c208c,'Bacon',88);
INSERT INTO stock (storeID, itemName, quantity) VALUES (b18b3932-a4ef-485c-a182-8e67b04c208c,'Beef',87);
INSERT INTO stock (storeID, itemName, quantity) VALUES (b18b3932-a4ef-485c-a182-8e67b04c208c,'Cheese',49);
INSERT INTO stock (storeID, itemName, quantity) VALUES (b18b3932-a4ef-485c-a182-8e67b04c208c,'Chicken',90);
INSERT INTO stock (storeID, itemName, quantity) VALUES (b18b3932-a4ef-485c-a182-8e67b04c208c,'Dough',50);
INSERT INTO stock (storeID, itemName, quantity) VALUES (b18b3932-a4ef-485c-a182-8e67b04c208c,'Mushrooms',91);
INSERT INTO stock (storeID, itemName, quantity) VALUES (b18b3932-a4ef-485c-a182-8e67b04c208c,'Olives',87);
INSERT INTO stock (storeID, itemName, quantity) VALUES (b18b3932-a4ef-485c-a182-8e67b04c208c,'Onion',90);
INSERT INTO stock (storeID, itemName, quantity) VALUES (b18b3932-a4ef-485c-a182-8e67b04c208c,'Pepperoni',88);
INSERT INTO stock (storeID, itemName, quantity) VALUES (b18b3932-a4ef-485c-a182-8e67b04c208c,'Peppers',89);
INSERT INTO stock (storeID, itemName, quantity) VALUES (b18b3932-a4ef-485c-a182-8e67b04c208c,'Pineapple',86);
INSERT INTO stock (storeID, itemName, quantity) VALUES (b18b3932-a4ef-485c-a182-8e67b04c208c,'Sausage',92);
INSERT INTO stock (storeID, itemName, quantity) VALUES (b18b3932-a4ef-485c-a182-8e67b04c208c,'SpicySauce',85);
INSERT INTO stock (storeID, itemName, quantity) VALUES (b18b3932-a4ef-485c-a182-8e67b04c208c,'TraditionalSauce',81);
INSERT INTO stock (storeID, itemName, quantity) VALUES (5a2bb99f-88d2-4612-ac60-774aea9b8de4,'Bacon',86);
INSERT INTO stock (storeID, itemName, quantity) VALUES (5a2bb99f-88d2-4612-ac60-774aea9b8de4,'Beef',84);
INSERT INTO stock (storeID, itemName, quantity) VALUES (5a2bb99f-88d2-4612-ac60-774aea9b8de4,'Cheese',58);
INSERT INTO stock (storeID, itemName, quantity) VALUES (5a2bb99f-88d2-4612-ac60-774aea9b8de4,'Chicken',84);
INSERT INTO stock (storeID, itemName, quantity) VALUES (5a2bb99f-88d2-4612-ac60-774aea9b8de4,'Dough',54);
INSERT INTO stock (storeID, itemName, quantity) VALUES (5a2bb99f-88d2-4612-ac60-774aea9b8de4,'Mushrooms',87);
INSERT INTO stock (storeID, itemName, quantity) VALUES (5a2bb99f-88d2-4612-ac60-774aea9b8de4,'Olives',86);
INSERT INTO stock (storeID, itemName, quantity) VALUES (5a2bb99f-88d2-4612-ac60-774aea9b8de4,'Onion',85);
INSERT INTO stock (storeID, itemName, quantity) VALUES (5a2bb99f-88d2-4612-ac60-774aea9b8de4,'Pepperoni',87);
INSERT INTO stock (storeID, itemName, quantity) VALUES (5a2bb99f-88d2-4612-ac60-774aea9b8de4,'Peppers',89);
INSERT INTO stock (storeID, itemName, quantity) VALUES (5a2bb99f-88d2-4612-ac60-774aea9b8de4,'Pineapple',86);
INSERT INTO stock (storeID, itemName, quantity) VALUES (5a2bb99f-88d2-4612-ac60-774aea9b8de4,'Sausage',85);
INSERT INTO stock (storeID, itemName, quantity) VALUES (5a2bb99f-88d2-4612-ac60-774aea9b8de4,'SpicySauce',81);
INSERT INTO stock (storeID, itemName, quantity) VALUES (5a2bb99f-88d2-4612-ac60-774aea9b8de4,'TraditionalSauce',89);


CREATE TABLE pizzas (
  pizzaID UUID,
  toppings SET<TUPLE<TEXT, INT>>,
  cost FLOAT,
  PRIMARY KEY (pizzaID)
);

INSERT INTO pizzas (pizzaID, toppings, cost) VALUES (2b261722-9e8b-437f-ba81-f146bafcfec7,{('Beef', 1), ('Cheese', 2), ('Chicken', 1), ('Dough', 2), ('Mushrooms', 1), ('Onion', 1), ('SpicySauce', 1)},14.9); 
INSERT INTO pizzas (pizzaID, toppings, cost) VALUES (d54488d7-b88e-416a-890e-8276f3dd5777,{('Beef', 1), ('Cheese', 2), ('Chicken', 1), ('Dough', 2), ('Mushrooms', 1), ('Olives', 1), ('Onion', 1), ('Pepperoni', 1), ('Peppers', 1), ('Pineapple', 1), ('Sausage', 1), ('TraditionalSauce', 1)},19.38);
INSERT INTO pizzas (pizzaID, toppings, cost) VALUES (597438b3-344c-4e15-b1f6-4051823e7582,{('Cheese', 2), ('Dough', 1), ('TraditionalSauce', 1)},7.2);
INSERT INTO pizzas (pizzaID, toppings, cost) VALUES (f586db3f-06b2-4772-9e44-9f78444537f9,{('Bacon', 1), ('Beef', 1), ('Cheese', 2), ('Chicken', 1), ('Dough', 1), ('Mushrooms', 1), ('Onion', 1), ('Pepperoni', 1), ('Pineapple', 1), ('Sausage', 1), ('SpicySauce', 1)},15.98);
INSERT INTO pizzas (pizzaID, toppings, cost) VALUES (56421056-f015-402c-b819-99b335c8731a,{('Beef', 1), ('Cheese', 2), ('Chicken', 1), ('Dough', 1), ('Mushrooms', 1), ('Olives', 1), ('Onion', 1), ('Pepperoni', 1), ('Peppers', 1), ('Pineapple', 1), ('Sausage', 1), ('SpicySauce', 1)},15.28);
INSERT INTO pizzas (pizzaID, toppings, cost) VALUES (fa66cb8c-07f7-4d33-ab3e-212088b94946,{('Cheese', 1), ('Dough', 2), ('Mushrooms', 1), ('SpicySauce', 1)},10.85);
INSERT INTO pizzas (pizzaID, toppings, cost) VALUES (1d440b28-5f58-460f-a9fc-c5cd9c95a696,{('Bacon', 1), ('Beef', 1), ('Cheese', 2), ('Dough', 1), ('Peppers', 1), ('Pineapple', 1), ('Sausage', 1), ('TraditionalSauce', 1)},12.73);
INSERT INTO pizzas (pizzaID, toppings, cost) VALUES (0faa103f-d7e6-44a9-bf5f-0037a79c91d4,{('Bacon', 1), ('Cheese', 2), ('Dough', 2), ('Olives', 1), ('TraditionalSauce', 1)},13.05);
INSERT INTO pizzas (pizzaID, toppings, cost) VALUES (cf555592-b47e-4940-938f-1f3e889511b9,{('Cheese', 2), ('Dough', 2), ('SpicySauce', 1)},11.1);
INSERT INTO pizzas (pizzaID, toppings, cost) VALUES (cfd2863a-0ce2-4b51-b197-9b328e45368c,{('Beef', 1), ('Cheese', 2), ('Dough', 1), ('Onion', 1), ('Pepperoni', 1), ('Sausage', 1), ('TraditionalSauce', 1)},11.95);
INSERT INTO pizzas (pizzaID, toppings, cost) VALUES (147712af-28a0-4762-aabc-86030a8e3c92,{('Beef', 1), ('Cheese', 1), ('Dough', 2), ('Pepperoni', 1), ('TraditionalSauce', 1)},13.1);
INSERT INTO pizzas (pizzaID, toppings, cost) VALUES (04814975-4ce3-4436-aca8-ca200c8f2739,{('Dough', 1), ('SpicySauce', 1)},5.1);
INSERT INTO pizzas (pizzaID, toppings, cost) VALUES (5bd37fb0-5d37-427c-a396-590cc675302c,{('Bacon', 1), ('Cheese', 2), ('Chicken', 1), ('Dough', 2), ('Mushrooms', 1), ('Onion', 1), ('Pepperoni', 1), ('Peppers', 1), ('Pineapple', 1), ('Sausage', 1), ('TraditionalSauce', 1)},19.23);
INSERT INTO pizzas (pizzaID, toppings, cost) VALUES (d07c012c-22b9-4a7d-80c5-75829fb16fa9,{('Bacon', 1), ('Beef', 1), ('Cheese', 1), ('Dough', 1), ('Olives', 1), ('Onion', 1), ('Pepperoni', 1), ('Peppers', 1), ('Sausage', 1), ('TraditionalSauce', 1)},13.35);
INSERT INTO pizzas (pizzaID, toppings, cost) VALUES (39e91684-fe19-45ac-9358-4a5cfb241054,{('Bacon', 1), ('Beef', 1), ('Cheese', 2), ('Chicken', 1), ('Dough', 2), ('Mushrooms', 1), ('Pepperoni', 1), ('Peppers', 1), ('Pineapple', 1), ('SpicySauce', 1)},18.68);
INSERT INTO pizzas (pizzaID, toppings, cost) VALUES (7fa8fe5f-84e2-41c7-8b8e-9d0ff5dba6ec,{('Cheese', 2), ('Dough', 1), ('SpicySauce', 1)},7.1);
INSERT INTO pizzas (pizzaID, toppings, cost) VALUES (09bd57d5-e399-4bbe-99bf-8d5162cc508d,{('Bacon', 1), ('Beef', 1), ('Cheese', 1), ('Chicken', 1), ('Dough', 1), ('Mushrooms', 1), ('Olives', 1), ('Onion', 1), ('Pepperoni', 1), ('Pineapple', 1), ('SpicySauce', 1)},13.73);
INSERT INTO pizzas (pizzaID, toppings, cost) VALUES (5250cb6e-1c44-4b97-88a9-e077025f965a,{('Beef', 1), ('Dough', 2), ('Mushrooms', 1), ('Onion', 1), ('SpicySauce', 1)},11.55);
INSERT INTO pizzas (pizzaID, toppings, cost) VALUES (175aea58-1eb9-42d7-afe8-6c1a54b76af9,{('Bacon', 1), ('Cheese', 1), ('Chicken', 1), ('Dough', 2), ('Sausage', 1), ('SpicySauce', 1)},14.55);
INSERT INTO pizzas (pizzaID, toppings, cost) VALUES (f6622afc-fc55-4eb5-8ae4-506f8842ac64,{('Cheese', 2), ('Dough', 1), ('Olives', 1), ('SpicySauce', 1)},7.4);
INSERT INTO pizzas (pizzaID, toppings, cost) VALUES (2ac55689-be18-4b95-a2aa-52462a36e6a2,{('Bacon', 1), ('Beef', 1), ('Chicken', 1), ('Dough', 1), ('Olives', 1), ('Onion', 1), ('Pepperoni', 1), ('Peppers', 1), ('Pineapple', 1), ('Sausage', 1), ('SpicySauce', 1)},14.08);
INSERT INTO pizzas (pizzaID, toppings, cost) VALUES (14280203-8e87-40a3-9eb0-ee0a3957f9e9,{('Bacon', 1), ('Chicken', 1), ('Dough', 2), ('Mushrooms', 1), ('Pepperoni', 1), ('Peppers', 1), ('TraditionalSauce', 1)},14.9);
INSERT INTO pizzas (pizzaID, toppings, cost) VALUES (f83537b0-25c9-4a8e-b3ba-850f5c0d8b91,{('Dough', 2), ('TraditionalSauce', 1)},9.2);
INSERT INTO pizzas (pizzaID, toppings, cost) VALUES (9a403fd5-1543-4e04-91f2-62b99e5548db,{('Beef', 1), ('Cheese', 2), ('Dough', 2), ('Pepperoni', 1), ('Pineapple', 1), ('Sausage', 1), ('TraditionalSauce', 1)},16.13);
INSERT INTO pizzas (pizzaID, toppings, cost) VALUES (65b079b2-a56f-429e-b2f1-1fa955f917e2,{('Bacon', 1), ('Beef', 1), ('Cheese', 2), ('Chicken', 1), ('Dough', 1), ('Mushrooms', 1), ('Olives', 1), ('Onion', 1), ('Sausage', 1), ('SpicySauce', 1)},14.3);
INSERT INTO pizzas (pizzaID, toppings, cost) VALUES (41c0b55b-db88-45b9-86bd-155a63eaa445,{('Dough', 2), ('Olives', 1), ('Peppers', 1), ('Pineapple', 1), ('TraditionalSauce', 1)},10.53);
INSERT INTO pizzas (pizzaID, toppings, cost) VALUES (1df25def-2b34-4186-9316-53a6a7a5ee92,{('Bacon', 1), ('Beef', 1), ('Cheese', 2), ('Chicken', 1), ('Dough', 1), ('Mushrooms', 1), ('Olives', 1), ('Onion', 1), ('Pineapple', 1), ('TraditionalSauce', 1)},13.33);
INSERT INTO pizzas (pizzaID, toppings, cost) VALUES (f09dc493-68be-4948-a23e-d6751479b2e9,{('Beef', 1), ('Dough', 1), ('Pepperoni', 1), ('Pineapple', 1), ('Sausage', 1), ('TraditionalSauce', 1)},10.13);
INSERT INTO pizzas (pizzaID, toppings, cost) VALUES (e14bc04b-0d91-4a10-9750-80c1d8bee38d,{('Cheese', 1), ('Dough', 2), ('SpicySauce', 1)},10.1);
INSERT INTO pizzas (pizzaID, toppings, cost) VALUES (2c66024e-97ab-46d3-b311-c8ab2e74a896,{('Cheese', 2), ('Dough', 1), ('TraditionalSauce', 1)},7.2);
INSERT INTO pizzas (pizzaID, toppings, cost) VALUES (4e7f1d01-d2bd-4aa4-9c9c-6b2befb4538a,{('Dough', 1), ('Pineapple', 1), ('TraditionalSauce', 1)},5.68);
INSERT INTO pizzas (pizzaID, toppings, cost) VALUES (e025a189-04b2-424c-8767-55bfa1409ad7,{('Bacon', 1), ('Chicken', 1), ('Dough', 2), ('Pepperoni', 1), ('TraditionalSauce', 1)},13.6);
INSERT INTO pizzas (pizzaID, toppings, cost) VALUES (38521e4e-5755-45af-8034-631d5b68d4f4,{('Cheese', 1), ('Chicken', 1), ('Dough', 2), ('Onion', 1), ('Pepperoni', 1), ('SpicySauce', 1)},13.25);
INSERT INTO pizzas (pizzaID, toppings, cost) VALUES (5eb93e33-ba92-4e81-9e6a-0f67fe293e33,{('Beef', 1), ('Chicken', 1), ('Dough', 1), ('Olives', 1), ('Pineapple', 1), ('TraditionalSauce', 1)},8.73);
INSERT INTO pizzas (pizzaID, toppings, cost) VALUES (f3ed9d67-c3e2-4248-8f26-0beb370d5f93,{('Cheese', 2), ('Dough', 2), ('Olives', 1), ('TraditionalSauce', 1)},11.5);
INSERT INTO pizzas (pizzaID, toppings, cost) VALUES (8dd815ec-734b-469c-9951-eb7c8500aa59,{('Beef', 1), ('Cheese', 2), ('Chicken', 1), ('Dough', 1), ('Mushrooms', 1), ('Olives', 1), ('Pepperoni', 1), ('Peppers', 1), ('Pineapple', 1), ('Sausage', 1), ('TraditionalSauce', 1)},15.08);
INSERT INTO pizzas (pizzaID, toppings, cost) VALUES (eecafeb4-b9aa-4f32-8a44-f13b0fc1fb53,{('Dough', 2), ('TraditionalSauce', 1)},9.2);
INSERT INTO pizzas (pizzaID, toppings, cost) VALUES (47ed25d4-7b32-4709-b9c8-5dd5ab44688d,{('Bacon', 1), ('Dough', 2), ('Mushrooms', 1), ('Pepperoni', 1), ('SpicySauce', 1)},12.9);
INSERT INTO pizzas (pizzaID, toppings, cost) VALUES (1a2833b8-b522-445d-ae30-74880d7a247f,{('Bacon', 1), ('Beef', 1), ('Cheese', 2), ('Chicken', 1), ('Dough', 2), ('Mushrooms', 1), ('Onion', 1), ('Sausage', 1), ('SpicySauce', 1)},18);
INSERT INTO pizzas (pizzaID, toppings, cost) VALUES (58456bfa-6953-444e-a52e-4b0927fa1904,{('Bacon', 1), ('Beef', 1), ('Cheese', 2), ('Chicken', 1), ('Dough', 2), ('Mushrooms', 1), ('Olives', 1), ('Onion', 1), ('Pepperoni', 1), ('Pineapple', 1), ('SpicySauce', 1)},18.73);
INSERT INTO pizzas (pizzaID, toppings, cost) VALUES (72b170a0-ec72-4855-9f12-7ab15148ef57,{('Bacon', 1), ('Cheese', 2), ('Dough', 1), ('Olives', 1), ('SpicySauce', 1)},8.95);
INSERT INTO pizzas (pizzaID, toppings, cost) VALUES (17f86318-c900-4ed2-947b-90a2a3b86e1b,{('Bacon', 1), ('Beef', 1), ('Cheese', 2), ('Chicken', 1), ('Dough', 2), ('Mushrooms', 1), ('Olives', 1), ('Onion', 1), ('Pepperoni', 1), ('Peppers', 1), ('Sausage', 1), ('TraditionalSauce', 1)},20.45);
INSERT INTO pizzas (pizzaID, toppings, cost) VALUES (91add4b4-372a-4f2e-8783-0abb8837a24b,{('Beef', 1), ('Cheese', 2), ('Chicken', 1), ('Dough', 1), ('Mushrooms', 1), ('Olives', 1), ('Onion', 1), ('Pepperoni', 1), ('Pineapple', 1), ('TraditionalSauce', 1)},13.28);
INSERT INTO pizzas (pizzaID, toppings, cost) VALUES (03054769-21bf-4337-baf1-4927b3fb2e45,{('Cheese', 1), ('Dough', 2), ('Pineapple', 1), ('TraditionalSauce', 1)},10.68);
INSERT INTO pizzas (pizzaID, toppings, cost) VALUES (e7d7acb9-86df-431c-871a-71e31fb66343,{('Bacon', 1), ('Beef', 1), ('Cheese', 1), ('Chicken', 1), ('Dough', 1), ('Mushrooms', 1), ('Olives', 1), ('Onion', 1), ('Pepperoni', 1), ('Peppers', 1), ('Sausage', 1), ('TraditionalSauce', 1)},15.45);
INSERT INTO pizzas (pizzaID, toppings, cost) VALUES (83dd415d-5210-441d-ad00-57d0eb0f740b,{('Cheese', 2), ('Dough', 1), ('Mushrooms', 1), ('Pineapple', 1), ('TraditionalSauce', 1)},8.43);
INSERT INTO pizzas (pizzaID, toppings, cost) VALUES (105cc909-2ea6-4707-84e7-1a6e8bf0ea63,{('Cheese', 1), ('Chicken', 1), ('Dough', 1), ('Onion', 1), ('Peppers', 1), ('Pineapple', 1), ('Sausage', 1), ('TraditionalSauce', 1)},10.43);
INSERT INTO pizzas (pizzaID, toppings, cost) VALUES (3332bbcf-4ce3-40fd-aa42-c15a219c479d,{('Bacon', 1), ('Beef', 1), ('Cheese', 2), ('Chicken', 1), ('Dough', 2), ('Mushrooms', 1), ('Olives', 1), ('Onion', 1), ('Pepperoni', 1), ('Pineapple', 1), ('Sausage', 1), ('SpicySauce', 1)},20.28);
INSERT INTO pizzas (pizzaID, toppings, cost) VALUES (4549d2fc-3235-47dc-b14e-222599afc454,{('Bacon', 1), ('Beef', 1), ('Cheese', 1), ('Chicken', 1), ('Dough', 1), ('Olives', 1), ('Onion', 1), ('Pepperoni', 1), ('Peppers', 1), ('SpicySauce', 1)},13.05);
INSERT INTO pizzas (pizzaID, toppings, cost) VALUES (6c897063-1f53-495a-b283-cc6da68db89a,{('Bacon', 1), ('Cheese', 1), ('Chicken', 1), ('Dough', 2), ('Olives', 1), ('Peppers', 1), ('Pineapple', 1), ('TraditionalSauce', 1)},14.43);
INSERT INTO pizzas (pizzaID, toppings, cost) VALUES (569928fe-e937-42d4-8225-a38d22e42606,{('Beef', 1), ('Chicken', 1), ('Dough', 1), ('Olives', 1), ('Pineapple', 1), ('Sausage', 1), ('SpicySauce', 1)},10.18);
INSERT INTO pizzas (pizzaID, toppings, cost) VALUES (203e75f7-6153-4a84-b774-de1ab1f22a05,{('Bacon', 1), ('Cheese', 1), ('Dough', 1), ('Olives', 1), ('Onion', 1), ('Peppers', 1), ('Pineapple', 1), ('Sausage', 1), ('TraditionalSauce', 1)},10.93);
INSERT INTO pizzas (pizzaID, toppings, cost) VALUES (9fbf6d5e-083e-43ab-b94f-4752456525a0,{('Bacon', 1), ('Beef', 1), ('Cheese', 1), ('Chicken', 1), ('Dough', 1), ('Olives', 1), ('Pepperoni', 1), ('Peppers', 1), ('Pineapple', 1), ('Sausage', 1), ('TraditionalSauce', 1)},14.88);
INSERT INTO pizzas (pizzaID, toppings, cost) VALUES (dfde8495-e4f5-4c74-b8fa-6f73748f548a,{('Bacon', 1), ('Beef', 1), ('Cheese', 2), ('Chicken', 1), ('Dough', 1), ('Mushrooms', 1), ('Olives', 1), ('Onion', 1), ('Peppers', 1), ('TraditionalSauce', 1)},13.4);
INSERT INTO pizzas (pizzaID, toppings, cost) VALUES (fe980885-adae-4399-abf0-eeedaeffe4ef,{('Dough', 1), ('Mushrooms', 1), ('Onion', 1), ('Pepperoni', 1), ('Peppers', 1), ('Pineapple', 1), ('Sausage', 1), ('SpicySauce', 1)},10.23);
INSERT INTO pizzas (pizzaID, toppings, cost) VALUES (9bb0f02d-ee75-4db3-97c2-dd6b6a3f301b,{('Beef', 1), ('Cheese', 1), ('Dough', 2), ('Olives', 1), ('Onion', 1), ('Pepperoni', 1), ('Pineapple', 1), ('SpicySauce', 1)},14.08);
INSERT INTO pizzas (pizzaID, toppings, cost) VALUES (2541dffc-00bf-4f6f-b579-e9c5f797a984,{('Beef', 1), ('Cheese', 2), ('Dough', 2), ('TraditionalSauce', 1)},12.6);
INSERT INTO pizzas (pizzaID, toppings, cost) VALUES (98674f4c-2737-4802-a5d5-396a59825b2c,{('Cheese', 1), ('Dough', 1), ('SpicySauce', 1)},6.1);
INSERT INTO pizzas (pizzaID, toppings, cost) VALUES (f0e0c16a-0650-4fc5-a2cb-dc4f1e1a5a02,{('Bacon', 1), ('Beef', 1), ('Cheese', 2), ('Dough', 2), ('Mushrooms', 1), ('Olives', 1), ('Pepperoni', 1), ('Pineapple', 1), ('Sausage', 1), ('SpicySauce', 1)},18.63);
INSERT INTO pizzas (pizzaID, toppings, cost) VALUES (ef634e30-5aee-42f6-a747-5046d3111388,{('Beef', 1), ('Cheese', 2), ('Chicken', 1), ('Dough', 2), ('Mushrooms', 1), ('Olives', 1), ('Onion', 1), ('Peppers', 1), ('Pineapple', 1), ('SpicySauce', 1)},16.23);
INSERT INTO pizzas (pizzaID, toppings, cost) VALUES (378fe289-f002-490d-835a-96d69a100abf,{('Beef', 1), ('Cheese', 1), ('Dough', 2), ('Olives', 1), ('Sausage', 1), ('TraditionalSauce', 1)},13.45);
INSERT INTO pizzas (pizzaID, toppings, cost) VALUES (de4504b5-fdec-4255-b002-6e785966cb72,{('Beef', 1), ('Cheese', 1), ('Dough', 2), ('Olives', 1), ('Onion', 1), ('Peppers', 1), ('Pineapple', 1), ('SpicySauce', 1)},13.13);
INSERT INTO pizzas (pizzaID, toppings, cost) VALUES (69422396-1058-440b-b810-92905d31923e,{('Cheese', 1), ('Dough', 2), ('SpicySauce', 1)},10.1);
INSERT INTO pizzas (pizzaID, toppings, cost) VALUES (7482a291-f8d6-460b-a84d-93f0e373b1b4,{('Bacon', 1), ('Beef', 1), ('Cheese', 1), ('Chicken', 1), ('Dough', 1), ('Mushrooms', 1), ('Olives', 1), ('Pepperoni', 1), ('Peppers', 1), ('Pineapple', 1), ('TraditionalSauce', 1)},14.08);
INSERT INTO pizzas (pizzaID, toppings, cost) VALUES (0d1184ef-a354-4491-8ca9-0ee0350adbe9,{('Cheese', 2), ('Dough', 2), ('TraditionalSauce', 1)},11.2);
INSERT INTO pizzas (pizzaID, toppings, cost) VALUES (e19f18ef-7254-4dbe-91be-1cf4ccab644f,{('Cheese', 1), ('Dough', 1), ('SpicySauce', 1)},6.1);
INSERT INTO pizzas (pizzaID, toppings, cost) VALUES (0bd5ca22-7192-4c3f-a87a-79146152a238,{('Bacon', 1), ('Cheese', 2), ('Chicken', 1), ('Dough', 2), ('Mushrooms', 1), ('Onion', 1), ('Pepperoni', 1), ('Peppers', 1), ('Sausage', 1), ('TraditionalSauce', 1)},18.75);
INSERT INTO pizzas (pizzaID, toppings, cost) VALUES (838648de-57cb-4472-a8b1-c6711ac934e0,{('Bacon', 1), ('Cheese', 2), ('Dough', 2), ('Mushrooms', 1), ('SpicySauce', 1)},13.4);
INSERT INTO pizzas (pizzaID, toppings, cost) VALUES (f0a76e0b-bfd2-4574-8d3f-61651332aa67,{('Chicken', 1), ('Dough', 1), ('Pineapple', 1), ('TraditionalSauce', 1)},7.03);
INSERT INTO pizzas (pizzaID, toppings, cost) VALUES (1f3cea3f-6e28-4714-afc4-8335a5bee1b5,{('Bacon', 1), ('Beef', 1), ('Dough', 2), ('TraditionalSauce', 1)},12.15);
INSERT INTO pizzas (pizzaID, toppings, cost) VALUES (79407346-85ab-4980-a7b7-77e421677ed6,{('Chicken', 1), ('Dough', 1), ('Mushrooms', 1), ('Olives', 1), ('Onion', 1), ('Pepperoni', 1), ('Peppers', 1), ('Pineapple', 1), ('Sausage', 1), ('SpicySauce', 1)},11.88);
INSERT INTO pizzas (pizzaID, toppings, cost) VALUES (f277d488-8508-4e46-8f83-84a5cf2eeea5,{('Beef', 1), ('Cheese', 2), ('Dough', 2), ('Mushrooms', 1), ('Olives', 1), ('Onion', 1), ('Peppers', 1), ('Pineapple', 1), ('Sausage', 1), ('TraditionalSauce', 1)},16.53);
INSERT INTO pizzas (pizzaID, toppings, cost) VALUES (2db9f011-4d96-40f4-ae4d-a49aacfb4b2b,{('Bacon', 1), ('Cheese', 2), ('Dough', 1), ('Peppers', 1), ('SpicySauce', 1)},9.2);
INSERT INTO pizzas (pizzaID, toppings, cost) VALUES (05724f7e-bf92-479f-8069-2ce827b11b19,{('Bacon', 1), ('Cheese', 2), ('Dough', 1), ('Pepperoni', 1), ('SpicySauce', 1)},10.15);
INSERT INTO pizzas (pizzaID, toppings, cost) VALUES (486f776d-e836-4dc7-8513-fd5e8adde482,{('Cheese', 1), ('Dough', 1), ('SpicySauce', 1)},6.1);
INSERT INTO pizzas (pizzaID, toppings, cost) VALUES (5fb56da6-3428-4bb2-a133-d278913569af,{('Cheese', 1), ('Dough', 2), ('Peppers', 1), ('SpicySauce', 1)},10.65);
INSERT INTO pizzas (pizzaID, toppings, cost) VALUES (9c486eab-eb00-468d-87ca-85d9b19b91bd,{('Bacon', 1), ('Beef', 1), ('Cheese', 2), ('Chicken', 1), ('Dough', 2), ('Mushrooms', 1), ('Onion', 1), ('Pepperoni', 1), ('Peppers', 1), ('Pineapple', 1), ('Sausage', 1), ('SpicySauce', 1)},20.53);
INSERT INTO pizzas (pizzaID, toppings, cost) VALUES (64784cad-41c0-476e-99fe-3f035465da4a,{('Cheese', 1), ('Dough', 2), ('Pepperoni', 1), ('SpicySauce', 1)},11.6);
INSERT INTO pizzas (pizzaID, toppings, cost) VALUES (30749baf-c9b1-4623-b44e-ebab0d9cb9c3,{('Cheese', 2), ('Dough', 2), ('SpicySauce', 1)},11.1);
INSERT INTO pizzas (pizzaID, toppings, cost) VALUES (7fb1e7fb-c042-4b6b-bb91-e0b5c07184e8,{('Beef', 1), ('Cheese', 1), ('Chicken', 1), ('Dough', 1), ('SpicySauce', 1)},8.85);

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

INSERT INTO payments (paymentToken, method) VALUES (895d9f25-a013-4320-8c44-6a536283f883,'Visa');
INSERT INTO payments (paymentToken, method) VALUES (8693234d-07e7-4985-aaa7-fcf7e6d80639,'Discover');
INSERT INTO payments (paymentToken, method) VALUES (8495948c-f95a-4571-a61f-9ee725ce4a4e,'Visa');
INSERT INTO payments (paymentToken, method) VALUES (663f24b7-7803-41c0-9d4a-45d452a57c55,'Apple Pay');
INSERT INTO payments (paymentToken, method) VALUES (05fd4e59-9933-40bd-83f8-599f557bc9f6,'Discover');
INSERT INTO payments (paymentToken, method) VALUES (58a1c776-6ed2-4193-9979-2dcc49a04b24,'Discover');
INSERT INTO payments (paymentToken, method) VALUES (c2788f1a-8bf2-4d22-841b-bfd935f5557c,'AMEX');
INSERT INTO payments (paymentToken, method) VALUES (2298f1aa-d3e3-42a2-8ac1-7152ad28592c,'Discover');
INSERT INTO payments (paymentToken, method) VALUES (3a5fde6c-9d5c-4965-84f6-7e5a0cda01b0,'PayPal');
INSERT INTO payments (paymentToken, method) VALUES (ef0aea75-2a68-464b-950e-88a888884fa9,'Discover');
INSERT INTO payments (paymentToken, method) VALUES (bc37d930-199b-4a3e-92cd-8df514a32532,'AMEX');
INSERT INTO payments (paymentToken, method) VALUES (c649f1e4-8f61-4807-aef3-49eeb8468670,'Visa');
INSERT INTO payments (paymentToken, method) VALUES (f8185f2d-d574-41a8-840b-7a4204eb848e,'AMEX');
INSERT INTO payments (paymentToken, method) VALUES (2961cc7f-056f-4205-8d4f-82d00a81966a,'Apple Pay');
INSERT INTO payments (paymentToken, method) VALUES (6974b6d0-709b-471a-8681-b604e6a99f91,'Google Pay');
INSERT INTO payments (paymentToken, method) VALUES (fb13d054-6836-4ab3-95ad-7ab9a5c20ec0,'Apple Pay');
INSERT INTO payments (paymentToken, method) VALUES (3ae06404-35ad-40f1-b601-a4b7758441b6,'Google Pay');
INSERT INTO payments (paymentToken, method) VALUES (0f13da6b-8632-41d3-acea-f4b1bdfc34bf,'Apple Pay');
INSERT INTO payments (paymentToken, method) VALUES (4641ffee-afe8-4ebf-ab2b-69845d2bf3f9,'Visa');
INSERT INTO payments (paymentToken, method) VALUES (abccaba5-399c-40e6-9ceb-0c75dd960f62,'Visa');
INSERT INTO payments (paymentToken, method) VALUES (bf79288e-441e-4d85-9e67-fafcefb45eec,'Gift Card');
INSERT INTO payments (paymentToken, method) VALUES (30759031-4911-43f9-8761-9057622ce567,'Mastercard');
INSERT INTO payments (paymentToken, method) VALUES (21fb43a7-b0a8-4e18-b13e-b16b655eeb22,'Gift Card');
INSERT INTO payments (paymentToken, method) VALUES (2ffce2c4-d40d-41fd-ab81-3573a3d482af,'Gift Card');
INSERT INTO payments (paymentToken, method) VALUES (364e534d-1c5f-4216-a0de-b3d1ddd94f0a,'AMEX');
INSERT INTO payments (paymentToken, method) VALUES (bdf88da3-77e8-40bf-b9dd-bd5ee7c311a1,'Google Pay');
INSERT INTO payments (paymentToken, method) VALUES (531382a3-824e-483d-b2b9-831007ed32e7,'Google Pay');
INSERT INTO payments (paymentToken, method) VALUES (6f8c32c6-21ad-468e-935c-bba31eb83ee9,'AMEX');
INSERT INTO payments (paymentToken, method) VALUES (31d925d5-7843-4301-981f-2dbfb906ca88,'Apple Pay');
INSERT INTO payments (paymentToken, method) VALUES (011c5485-bbc4-4922-9fc8-f558852076da,'Google Pay');
INSERT INTO payments (paymentToken, method) VALUES (15f7190a-bd15-4158-b778-32eae5edc576,'Google Pay');
INSERT INTO payments (paymentToken, method) VALUES (e6dfcbcf-bcb9-45aa-9447-8b1968957b83,'PayPal');
INSERT INTO payments (paymentToken, method) VALUES (bad25e7a-1e47-4f98-92a5-a85e2e2d8a03,'Apple Pay');
INSERT INTO payments (paymentToken, method) VALUES (e8c0c0fd-4e7f-4384-8718-9d4ba13f94cd,'Apple Pay');
INSERT INTO payments (paymentToken, method) VALUES (7128ca2f-ab1d-48f6-9970-e08c9a05d4f3,'AMEX');
INSERT INTO payments (paymentToken, method) VALUES (b4475392-ca66-4af4-bfe4-9fa6fb9702f2,'Apple Pay');
INSERT INTO payments (paymentToken, method) VALUES (aeb0f74f-8b2b-4104-904c-3891adf50b62,'Gift Card');
INSERT INTO payments (paymentToken, method) VALUES (15a6c870-b55e-4613-888b-bc24290b32dd,'Mastercard');
INSERT INTO payments (paymentToken, method) VALUES (bfca7d32-8470-4fdb-873b-46a81e911207,'Google Pay');
INSERT INTO payments (paymentToken, method) VALUES (4079f913-503f-4ebb-ac98-4aa4d1d03f5e,'Visa');
INSERT INTO payments (paymentToken, method) VALUES (58114734-2380-455c-8ab1-2d0f478c133d,'Apple Pay');
INSERT INTO payments (paymentToken, method) VALUES (348a8d18-eb33-407d-a7d0-15e0d6ae915a,'Google Pay');
INSERT INTO payments (paymentToken, method) VALUES (448eb340-970d-48b8-8a98-3851a1fca020,'Apple Pay');
INSERT INTO payments (paymentToken, method) VALUES (83749beb-80f3-4330-ac14-a66e64968938,'Gift Card');
INSERT INTO payments (paymentToken, method) VALUES (f8bf5d8c-a797-49f4-b8ea-75001ec012cd,'Discover');
INSERT INTO payments (paymentToken, method) VALUES (398608f2-24da-4129-a5c1-dd35aa3cfed8,'AMEX');
INSERT INTO payments (paymentToken, method) VALUES (f61c0a05-d6ef-4748-9460-9caa9bee9d7d,'Gift Card');
INSERT INTO payments (paymentToken, method) VALUES (7e6c0f35-5fff-4a7d-95de-7e8c5eb4f756,'Google Pay');
INSERT INTO payments (paymentToken, method) VALUES (2faf12ae-e554-42d0-8a35-4851b9b1def2,'Discover');
INSERT INTO payments (paymentToken, method) VALUES (2524b719-66bd-4041-82a3-724ed59c5ac9,'Apple Pay');
INSERT INTO payments (paymentToken, method) VALUES (7fd777e8-eb04-4a78-b3ef-205337085658,'AMEX');
INSERT INTO payments (paymentToken, method) VALUES (4387e62a-461c-4a00-9d64-3dd58ca4844c,'Gift Card');
INSERT INTO payments (paymentToken, method) VALUES (a00d9fcb-ea90-414e-8a2d-a468d43463af,'Gift Card');
INSERT INTO payments (paymentToken, method) VALUES (20057d2f-b636-4c7a-b2c9-87018bbe1f9d,'Gift Card');
INSERT INTO payments (paymentToken, method) VALUES (a71fe3f0-3f55-487f-9b64-17587f40694e,'Google Pay');
INSERT INTO payments (paymentToken, method) VALUES (6601d2c5-30e5-4cec-aa56-bc48102575a0,'Mastercard');
INSERT INTO payments (paymentToken, method) VALUES (e5d2e6be-028f-44fe-862f-f8897b775e59,'Discover');
INSERT INTO payments (paymentToken, method) VALUES (94930699-93ce-4fc7-b451-469eee26b0a8,'Mastercard');
INSERT INTO payments (paymentToken, method) VALUES (52efdec8-713f-4f1c-91fa-f1ea1c6eb9d0,'Mastercard');
INSERT INTO payments (paymentToken, method) VALUES (35422016-6ce8-4a2c-9022-6b3b3914726c,'PayPal');
INSERT INTO payments (paymentToken, method) VALUES (a380d0f8-b476-4fdd-9cd5-86bdba850e2d,'Google Pay');
INSERT INTO payments (paymentToken, method) VALUES (7ffe8fde-dbe5-4d09-ae15-2bbb8fc9043c,'Apple Pay');
INSERT INTO payments (paymentToken, method) VALUES (dbe342b9-ba5f-40ad-a5a8-c2b783287200,'Discover');
INSERT INTO payments (paymentToken, method) VALUES (54dbe01d-55de-4b42-9bcf-2d553fc34411,'PayPal');
INSERT INTO payments (paymentToken, method) VALUES (c3bdb71d-ff83-46cf-9196-179b9d0186bc,'Apple Pay');
INSERT INTO payments (paymentToken, method) VALUES (8f834ccd-2c2a-4f66-95f9-6fcd2cc1a408,'AMEX');
INSERT INTO payments (paymentToken, method) VALUES (f513a61b-4f1a-4043-ab57-12dc2a7e5197,'Apple Pay');
INSERT INTO payments (paymentToken, method) VALUES (6cd04850-d7ff-4de1-af4d-282f38ffbfa7,'Gift Card');
INSERT INTO payments (paymentToken, method) VALUES (d859a0f3-d53e-4240-a547-312da0b8f2e1,'AMEX');
INSERT INTO payments (paymentToken, method) VALUES (3c398f62-c238-4696-9f03-6e4573b65a64,'Visa');
INSERT INTO payments (paymentToken, method) VALUES (7d3605f8-c91b-48ec-98fc-c98832feb0bc,'Visa');
INSERT INTO payments (paymentToken, method) VALUES (7d153683-fc39-41a7-9faa-4a5489ab1ffb,'Gift Card');
INSERT INTO payments (paymentToken, method) VALUES (5ad40947-d338-4cbf-9e7e-929d63d2eada,'Apple Pay');
INSERT INTO payments (paymentToken, method) VALUES (cdcecc01-7838-472c-86bf-a7c057d0d811,'Google Pay');
INSERT INTO payments (paymentToken, method) VALUES (10043981-8ecb-4a07-8e9f-235e9779712c,'AMEX');
INSERT INTO payments (paymentToken, method) VALUES (5bdf8378-843d-4bca-8b0c-da49c79dccd2,'Discover');
INSERT INTO payments (paymentToken, method) VALUES (0379bb17-7b46-4140-be8b-548554d1a022,'Gift Card');
INSERT INTO payments (paymentToken, method) VALUES (b55aeb0a-4900-48ee-8816-f40f68f6d9d7,'Apple Pay');
INSERT INTO payments (paymentToken, method) VALUES (25102af0-c11e-41d3-a691-7204b30aeb36,'Gift Card');
INSERT INTO payments (paymentToken, method) VALUES (e494b7dc-596a-4d15-a6b5-0542fc0f1c37,'Visa');

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

INSERT INTO orderTable (orderId, orderedFrom, orderedBy, containsPizzas, paymentID, placedAT, active, estimatedDeliveryTime ) VALUES (24408218-0e26-4089-8ef6-a39ec804e2e5,7098813e-4624-462a-81a1-7e0e4e67631d,'Margaret Hunter',{58456bfa-6953-444e-a52e-4b0927fa1904},dbe342b9-ba5f-40ad-a5a8-c2b783287200,'2020-10-09 16:11:04.898+0000',True,-1);
INSERT INTO orderTable (orderId, orderedFrom, orderedBy, containsPizzas, paymentID, placedAT, active, estimatedDeliveryTime ) VALUES (fe741c7e-963c-47cd-85fc-3436bd02da82,7098813e-4624-462a-81a1-7e0e4e67631d,'Daniel Miller',{838648de-57cb-4472-a8b1-c6711ac934e0},15f7190a-bd15-4158-b778-32eae5edc576,'2020-10-09 16:09:04.684+0000',True,-1);
INSERT INTO orderTable (orderId, orderedFrom, orderedBy, containsPizzas, paymentID, placedAT, active, estimatedDeliveryTime ) VALUES (f46c3113-8afe-42f9-bbce-c86566b4bcef,5a2bb99f-88d2-4612-ac60-774aea9b8de4,'Daniel Moore',{e19f18ef-7254-4dbe-91be-1cf4ccab644f},b55aeb0a-4900-48ee-8816-f40f68f6d9d7,'2020-10-09 16:12:04.710+0000',True,-1);
INSERT INTO orderTable (orderId, orderedFrom, orderedBy, containsPizzas, paymentID, placedAT, active, estimatedDeliveryTime ) VALUES (7e723ea6-cbba-4b3d-91b1-6729a18e8ac0,b18b3932-a4ef-485c-a182-8e67b04c208c,'Kurt Arnold',{30749baf-c9b1-4623-b44e-ebab0d9cb9c3},e8c0c0fd-4e7f-4384-8718-9d4ba13f94cd,'2020-10-09 16:11:04.984+0000',True,-1);
INSERT INTO orderTable (orderId, orderedFrom, orderedBy, containsPizzas, paymentID, placedAT, active, estimatedDeliveryTime ) VALUES (9e3c3466-e9d3-49bd-81ba-d9edde2f162d,7098813e-4624-462a-81a1-7e0e4e67631d,'Cassidy Stewart',{0faa103f-d7e6-44a9-bf5f-0037a79c91d4},7d153683-fc39-41a7-9faa-4a5489ab1ffb,'2020-10-09 16:08:04.681+0000',True,-1);
INSERT INTO orderTable (orderId, orderedFrom, orderedBy, containsPizzas, paymentID, placedAT, active, estimatedDeliveryTime ) VALUES (6e330978-3bc9-4793-a179-ed47a5f55f55,b18b3932-a4ef-485c-a182-8e67b04c208c,'Jacob Garcia',{e025a189-04b2-424c-8767-55bfa1409ad7},4387e62a-461c-4a00-9d64-3dd58ca4844c,'2020-10-09 16:11:04.855+0000',True,-1);
INSERT INTO orderTable (orderId, orderedFrom, orderedBy, containsPizzas, paymentID, placedAT, active, estimatedDeliveryTime ) VALUES (4fcfa2de-ba46-4d2f-a2f4-13a721722573,b18b3932-a4ef-485c-a182-8e67b04c208c,'Melissa Jones',{1d440b28-5f58-460f-a9fc-c5cd9c95a696},663f24b7-7803-41c0-9d4a-45d452a57c55,'2020-10-09 16:06:57.075+0000',True,-1);
INSERT INTO orderTable (orderId, orderedFrom, orderedBy, containsPizzas, paymentID, placedAT, active, estimatedDeliveryTime ) VALUES (9e27952a-cee7-449a-b8e1-26ae2728b1d0,5a2bb99f-88d2-4612-ac60-774aea9b8de4,'Jennifer Martin',{79407346-85ab-4980-a7b7-77e421677ed6},f513a61b-4f1a-4043-ab57-12dc2a7e5197,'2020-10-09 16:11:05.030+0000',True,-1);
INSERT INTO orderTable (orderId, orderedFrom, orderedBy, containsPizzas, paymentID, placedAT, active, estimatedDeliveryTime ) VALUES (ff01189b-3ae9-4ff2-a2bc-4cdff699454f,5a2bb99f-88d2-4612-ac60-774aea9b8de4,'Tracy Henderson',{0d1184ef-a354-4491-8ca9-0ee0350adbe9},fb13d054-6836-4ab3-95ad-7ab9a5c20ec0,'2020-10-09 16:08:04.787+0000',True,-1);
INSERT INTO orderTable (orderId, orderedFrom, orderedBy, containsPizzas, paymentID, placedAT, active, estimatedDeliveryTime ) VALUES (e8debfe5-9f74-4d26-88f4-e06473f857cf,b18b3932-a4ef-485c-a182-8e67b04c208c,'Christopher Soto',{47ed25d4-7b32-4709-b9c8-5dd5ab44688d},011c5485-bbc4-4922-9fc8-f558852076da,'2020-10-09 16:08:04.876+0000',True,-1);
INSERT INTO orderTable (orderId, orderedFrom, orderedBy, containsPizzas, paymentID, placedAT, active, estimatedDeliveryTime ) VALUES (f611d989-f120-4010-b92c-df393b13a5a0,b18b3932-a4ef-485c-a182-8e67b04c208c,'Jack Collins',{2541dffc-00bf-4f6f-b579-e9c5f797a984},8693234d-07e7-4985-aaa7-fcf7e6d80639,'2020-10-09 16:12:04.532+0000',True,-1);
INSERT INTO orderTable (orderId, orderedFrom, orderedBy, containsPizzas, paymentID, placedAT, active, estimatedDeliveryTime ) VALUES (f59ecde2-0208-40fc-a48f-c1181bb1c7fb,b18b3932-a4ef-485c-a182-8e67b04c208c,'Steven Newman',{fe980885-adae-4399-abf0-eeedaeffe4ef},aeb0f74f-8b2b-4104-904c-3891adf50b62,'2020-10-09 16:12:04.798+0000',True,-1);
INSERT INTO orderTable (orderId, orderedFrom, orderedBy, containsPizzas, paymentID, placedAT, active, estimatedDeliveryTime ) VALUES (966d2851-ec6b-4709-90fd-1cb51e6e99f3,b18b3932-a4ef-485c-a182-8e67b04c208c,'Tracy Smith',{1df25def-2b34-4186-9316-53a6a7a5ee92},f8185f2d-d574-41a8-840b-7a4204eb848e,'2020-10-09 16:08:04.738+0000',True,-1);
INSERT INTO orderTable (orderId, orderedFrom, orderedBy, containsPizzas, paymentID, placedAT, active, estimatedDeliveryTime ) VALUES (2e1c6b7a-7757-4ede-8b0e-a3f5a07a263a,5a2bb99f-88d2-4612-ac60-774aea9b8de4,'Eric Douglas',{f277d488-8508-4e46-8f83-84a5cf2eeea5},5bdf8378-843d-4bca-8b0c-da49c79dccd2,'2020-10-09 16:06:57.132+0000',True,-1);
INSERT INTO orderTable (orderId, orderedFrom, orderedBy, containsPizzas, paymentID, placedAT, active, estimatedDeliveryTime ) VALUES (2a4541e9-c33f-4605-a736-19cec3c07011,7098813e-4624-462a-81a1-7e0e4e67631d,'Nathan Waters',{5250cb6e-1c44-4b97-88a9-e077025f965a},21fb43a7-b0a8-4e18-b13e-b16b655eeb22,'2020-10-09 16:13:04.823+0000',True,-1);
INSERT INTO orderTable (orderId, orderedFrom, orderedBy, containsPizzas, paymentID, placedAT, active, estimatedDeliveryTime ) VALUES (366f46bc-5ffe-4e3e-960b-e8bd2557a26c,b18b3932-a4ef-485c-a182-8e67b04c208c,'Maurice Reid',{105cc909-2ea6-4707-84e7-1a6e8bf0ea63},8495948c-f95a-4571-a61f-9ee725ce4a4e,'2020-10-09 16:11:05.117+0000',True,-1);
INSERT INTO orderTable (orderId, orderedFrom, orderedBy, containsPizzas, paymentID, placedAT, active, estimatedDeliveryTime ) VALUES (7a8c0c2b-f337-4ba7-9f6c-9fb7e63fa259,5a2bb99f-88d2-4612-ac60-774aea9b8de4,'Amy Medina',{9bb0f02d-ee75-4db3-97c2-dd6b6a3f301b},f8bf5d8c-a797-49f4-b8ea-75001ec012cd,'2020-10-09 16:09:05.020+0000',True,-1);
INSERT INTO orderTable (orderId, orderedFrom, orderedBy, containsPizzas, paymentID, placedAT, active, estimatedDeliveryTime ) VALUES (12f63894-844b-4372-8857-32c1c416de77,b18b3932-a4ef-485c-a182-8e67b04c208c,'Linda Jensen',{597438b3-344c-4e15-b1f6-4051823e7582},58114734-2380-455c-8ab1-2d0f478c133d,'2020-10-09 16:11:05.077+0000',True,-1);
INSERT INTO orderTable (orderId, orderedFrom, orderedBy, containsPizzas, paymentID, placedAT, active, estimatedDeliveryTime ) VALUES (b6b52ffd-c527-420f-b87e-01d1d10e211e,b18b3932-a4ef-485c-a182-8e67b04c208c,'Denise Nelson',{e7d7acb9-86df-431c-871a-71e31fb66343},7128ca2f-ab1d-48f6-9970-e08c9a05d4f3,'2020-10-09 16:12:04.750+0000',True,-1);
INSERT INTO orderTable (orderId, orderedFrom, orderedBy, containsPizzas, paymentID, placedAT, active, estimatedDeliveryTime ) VALUES (84994022-041d-4d95-a752-79c2f09d651a,5a2bb99f-88d2-4612-ac60-774aea9b8de4,'Jill Munoz',{f586db3f-06b2-4772-9e44-9f78444537f9},6f8c32c6-21ad-468e-935c-bba31eb83ee9,'2020-10-09 16:06:57.294+0000',True,-1);
INSERT INTO orderTable (orderId, orderedFrom, orderedBy, containsPizzas, paymentID, placedAT, active, estimatedDeliveryTime ) VALUES (44f789d6-4ebb-421b-9c54-ed4bc363d360,5a2bb99f-88d2-4612-ac60-774aea9b8de4,'Michael Smith',{98674f4c-2737-4802-a5d5-396a59825b2c},7ffe8fde-dbe5-4d09-ae15-2bbb8fc9043c,'2020-10-09 16:09:04.778+0000',True,-1);
INSERT INTO orderTable (orderId, orderedFrom, orderedBy, containsPizzas, paymentID, placedAT, active, estimatedDeliveryTime ) VALUES (471767a2-f07b-4f1e-8c35-752f3564670d,b18b3932-a4ef-485c-a182-8e67b04c208c,'Terry Barnes MD',{83dd415d-5210-441d-ad00-57d0eb0f740b},3a5fde6c-9d5c-4965-84f6-7e5a0cda01b0,'2020-10-09 16:06:57.398+0000',True,-1);
INSERT INTO orderTable (orderId, orderedFrom, orderedBy, containsPizzas, paymentID, placedAT, active, estimatedDeliveryTime ) VALUES (3c4622eb-d936-454d-8f97-2211ce03ba3a,7098813e-4624-462a-81a1-7e0e4e67631d,'Ashley Smith',{8dd815ec-734b-469c-9951-eb7c8500aa59},4641ffee-afe8-4ebf-ab2b-69845d2bf3f9,'2020-10-09 16:12:04.842+0000',True,-1);
INSERT INTO orderTable (orderId, orderedFrom, orderedBy, containsPizzas, paymentID, placedAT, active, estimatedDeliveryTime ) VALUES (b93e8a4a-a9c7-4553-a7b2-f05475569d36,b18b3932-a4ef-485c-a182-8e67b04c208c,'Joshua Stafford',{de4504b5-fdec-4255-b002-6e785966cb72},f61c0a05-d6ef-4748-9460-9caa9bee9d7d,'2020-10-09 16:06:56.896+0000',True,-1);
INSERT INTO orderTable (orderId, orderedFrom, orderedBy, containsPizzas, paymentID, placedAT, active, estimatedDeliveryTime ) VALUES (f7eb68a7-3a3f-44b7-9653-7b46922bd7a0,7098813e-4624-462a-81a1-7e0e4e67631d,'Mary Mullen',{9c486eab-eb00-468d-87ca-85d9b19b91bd},2524b719-66bd-4041-82a3-724ed59c5ac9,'2020-10-09 16:11:05.161+0000',True,-1);
INSERT INTO orderTable (orderId, orderedFrom, orderedBy, containsPizzas, paymentID, placedAT, active, estimatedDeliveryTime ) VALUES (ec85a551-f506-4957-bb00-dac1a954a01e,7098813e-4624-462a-81a1-7e0e4e67631d,'Lisa Bolton',{cfd2863a-0ce2-4b51-b197-9b328e45368c},bdf88da3-77e8-40bf-b9dd-bd5ee7c311a1,'2020-10-09 16:10:04.498+0000',True,-1);
INSERT INTO orderTable (orderId, orderedFrom, orderedBy, containsPizzas, paymentID, placedAT, active, estimatedDeliveryTime ) VALUES (c79fac0e-a231-48f0-92b8-7bdd65c6f752,b18b3932-a4ef-485c-a182-8e67b04c208c,'Tyler Turner',{72b170a0-ec72-4855-9f12-7ab15148ef57},448eb340-970d-48b8-8a98-3851a1fca020,'2020-10-09 16:12:04.574+0000',True,-1);
INSERT INTO orderTable (orderId, orderedFrom, orderedBy, containsPizzas, paymentID, placedAT, active, estimatedDeliveryTime ) VALUES (ad75ba81-4a5c-44a7-a0f3-2d6f4b4b4958,b18b3932-a4ef-485c-a182-8e67b04c208c,'Jacqueline Copeland MD',{91add4b4-372a-4f2e-8783-0abb8837a24b},3ae06404-35ad-40f1-b601-a4b7758441b6,'2020-10-09 16:06:57.347+0000',True,-1);
INSERT INTO orderTable (orderId, orderedFrom, orderedBy, containsPizzas, paymentID, placedAT, active, estimatedDeliveryTime ) VALUES (373da967-c790-454e-a978-b5a46ec344e9,5a2bb99f-88d2-4612-ac60-774aea9b8de4,'Sandra Marshall',{6c897063-1f53-495a-b283-cc6da68db89a},364e534d-1c5f-4216-a0de-b3d1ddd94f0a,'2020-10-09 16:06:56.956+0000',True,-1);
INSERT INTO orderTable (orderId, orderedFrom, orderedBy, containsPizzas, paymentID, placedAT, active, estimatedDeliveryTime ) VALUES (543623f9-49cb-444e-b9d2-1604a4ee0cd5,7098813e-4624-462a-81a1-7e0e4e67631d,'Joseph Nichols',{7482a291-f8d6-460b-a84d-93f0e373b1b4},83749beb-80f3-4330-ac14-a66e64968938,'2020-10-09 16:09:04.592+0000',True,-1);
INSERT INTO orderTable (orderId, orderedFrom, orderedBy, containsPizzas, paymentID, placedAT, active, estimatedDeliveryTime ) VALUES (432da2bb-6486-4749-987c-70c2b5ba7f1a,5a2bb99f-88d2-4612-ac60-774aea9b8de4,'Emily Hudson',{f09dc493-68be-4948-a23e-d6751479b2e9},10043981-8ecb-4a07-8e9f-235e9779712c,'2020-10-09 16:10:04.555+0000',True,-1);
INSERT INTO orderTable (orderId, orderedFrom, orderedBy, containsPizzas, paymentID, placedAT, active, estimatedDeliveryTime ) VALUES (1e8b03b3-0514-4e3c-bb19-b4701582b252,7098813e-4624-462a-81a1-7e0e4e67631d,'Amanda Allen',{cf555592-b47e-4940-938f-1f3e889511b9},7d3605f8-c91b-48ec-98fc-c98832feb0bc,'2020-10-09 16:13:04.945+0000',True,-1);
INSERT INTO orderTable (orderId, orderedFrom, orderedBy, containsPizzas, paymentID, placedAT, active, estimatedDeliveryTime ) VALUES (2e48854a-c59d-4171-8a25-563c01efb7d4,5a2bb99f-88d2-4612-ac60-774aea9b8de4,'Jesse Perry',{5bd37fb0-5d37-427c-a396-590cc675302c},15a6c870-b55e-4613-888b-bc24290b32dd,'2020-10-09 16:10:04.684+0000',True,-1);
INSERT INTO orderTable (orderId, orderedFrom, orderedBy, containsPizzas, paymentID, placedAT, active, estimatedDeliveryTime ) VALUES (6f461e2a-c67d-4c74-b786-76cc642e2aad,5a2bb99f-88d2-4612-ac60-774aea9b8de4,'Brian Moon',{2b261722-9e8b-437f-ba81-f146bafcfec7},5ad40947-d338-4cbf-9e7e-929d63d2eada,'2020-10-09 16:14:04.532+0000',True,-1);
INSERT INTO orderTable (orderId, orderedFrom, orderedBy, containsPizzas, paymentID, placedAT, active, estimatedDeliveryTime ) VALUES (b07fc505-3569-4d51-a3b5-59bd2f29c340,5a2bb99f-88d2-4612-ac60-774aea9b8de4,'Morgan Thompson',{f0e0c16a-0650-4fc5-a2cb-dc4f1e1a5a02},7e6c0f35-5fff-4a7d-95de-7e8c5eb4f756,'2020-10-09 16:14:04.738+0000',True,-1);
INSERT INTO orderTable (orderId, orderedFrom, orderedBy, containsPizzas, paymentID, placedAT, active, estimatedDeliveryTime ) VALUES (dceaebcf-d084-4489-a9d4-a32868a07dc8,5a2bb99f-88d2-4612-ac60-774aea9b8de4,'Alyssa Perez',{7fa8fe5f-84e2-41c7-8b8e-9d0ff5dba6ec},a380d0f8-b476-4fdd-9cd5-86bdba850e2d,'2020-10-09 16:11:04.943+0000',True,-1);
INSERT INTO orderTable (orderId, orderedFrom, orderedBy, containsPizzas, paymentID, placedAT, active, estimatedDeliveryTime ) VALUES (4e3a990d-e67d-4ecc-9f12-6e8c01e0af87,b18b3932-a4ef-485c-a182-8e67b04c208c,'Tricia Davenport',{486f776d-e836-4dc7-8513-fd5e8adde482},c2788f1a-8bf2-4d22-841b-bfd935f5557c,'2020-10-09 16:13:05.072+0000',True,-1);
INSERT INTO orderTable (orderId, orderedFrom, orderedBy, containsPizzas, paymentID, placedAT, active, estimatedDeliveryTime ) VALUES (2dbab543-bb2d-4766-8c91-439f5688b2f1,5a2bb99f-88d2-4612-ac60-774aea9b8de4,'Amanda Mccullough',{09bd57d5-e399-4bbe-99bf-8d5162cc508d},94930699-93ce-4fc7-b451-469eee26b0a8,'2020-10-09 16:06:57.012+0000',True,-1);
INSERT INTO orderTable (orderId, orderedFrom, orderedBy, containsPizzas, paymentID, placedAT, active, estimatedDeliveryTime ) VALUES (bd592e06-a030-4dc5-948a-4b6cdd8a653c,5a2bb99f-88d2-4612-ac60-774aea9b8de4,'Scott Hogan',{d07c012c-22b9-4a7d-80c5-75829fb16fa9},b4475392-ca66-4af4-bfe4-9fa6fb9702f2,'2020-10-09 16:06:57.241+0000',True,-1);
INSERT INTO orderTable (orderId, orderedFrom, orderedBy, containsPizzas, paymentID, placedAT, active, estimatedDeliveryTime ) VALUES (1436c6a7-b4c6-420a-8edf-38bc08db3739,5a2bb99f-88d2-4612-ac60-774aea9b8de4,'Mary Weaver',{9fbf6d5e-083e-43ab-b94f-4752456525a0},6601d2c5-30e5-4cec-aa56-bc48102575a0,'2020-10-09 16:14:04.782+0000',True,-1);
INSERT INTO orderTable (orderId, orderedFrom, orderedBy, containsPizzas, paymentID, placedAT, active, estimatedDeliveryTime ) VALUES (d78c51ed-41ab-4716-afb2-fdb9673851d8,b18b3932-a4ef-485c-a182-8e67b04c208c,'Jessica Christensen',{5fb56da6-3428-4bb2-a133-d278913569af},25102af0-c11e-41d3-a691-7204b30aeb36,'2020-10-09 16:08:04.923+0000',True,-1);
INSERT INTO orderTable (orderId, orderedFrom, orderedBy, containsPizzas, paymentID, placedAT, active, estimatedDeliveryTime ) VALUES (27aa345c-dc96-4099-9599-93824940d1e9,7098813e-4624-462a-81a1-7e0e4e67631d,'Jacqueline Todd',{d54488d7-b88e-416a-890e-8276f3dd5777},6cd04850-d7ff-4de1-af4d-282f38ffbfa7,'2020-10-09 16:06:57.188+0000',True,-1);
INSERT INTO orderTable (orderId, orderedFrom, orderedBy, containsPizzas, paymentID, placedAT, active, estimatedDeliveryTime ) VALUES (6d8c1311-55fd-4c2c-b84b-7265c5fbc8b6,b18b3932-a4ef-485c-a182-8e67b04c208c,'Grant Vega',{5eb93e33-ba92-4e81-9e6a-0f67fe293e33},d859a0f3-d53e-4240-a547-312da0b8f2e1,'2020-10-09 16:13:04.781+0000',True,-1);
INSERT INTO orderTable (orderId, orderedFrom, orderedBy, containsPizzas, paymentID, placedAT, active, estimatedDeliveryTime ) VALUES (d2bbdb30-3e2f-4f42-992c-fd38d872acc1,b18b3932-a4ef-485c-a182-8e67b04c208c,'Sarah Smith',{05724f7e-bf92-479f-8069-2ce827b11b19},52efdec8-713f-4f1c-91fa-f1ea1c6eb9d0,'2020-10-09 16:14:04.619+0000',True,-1);
INSERT INTO orderTable (orderId, orderedFrom, orderedBy, containsPizzas, paymentID, placedAT, active, estimatedDeliveryTime ) VALUES (19c9de5c-4293-4e2f-9280-a58ca7ec80ce,5a2bb99f-88d2-4612-ac60-774aea9b8de4,'Jonathan Perry',{65b079b2-a56f-429e-b2f1-1fa955f917e2},348a8d18-eb33-407d-a7d0-15e0d6ae915a,'2020-10-09 16:12:04.663+0000',True,-1);
INSERT INTO orderTable (orderId, orderedFrom, orderedBy, containsPizzas, paymentID, placedAT, active, estimatedDeliveryTime ) VALUES (4792ffeb-2259-44a2-b35d-31bf2df38b95,5a2bb99f-88d2-4612-ac60-774aea9b8de4,'Jessica Thomas DVM',{4549d2fc-3235-47dc-b14e-222599afc454},c3bdb71d-ff83-46cf-9196-179b9d0186bc,'2020-10-09 16:13:04.733+0000',True,-1);
INSERT INTO orderTable (orderId, orderedFrom, orderedBy, containsPizzas, paymentID, placedAT, active, estimatedDeliveryTime ) VALUES (2067a957-6cb3-4e31-b571-5a3b77045efe,5a2bb99f-88d2-4612-ac60-774aea9b8de4,'Ronald Cline',{0bd5ca22-7192-4c3f-a87a-79146152a238},e494b7dc-596a-4d15-a6b5-0542fc0f1c37,'2020-10-09 16:10:04.858+0000',True,-1);
INSERT INTO orderTable (orderId, orderedFrom, orderedBy, containsPizzas, paymentID, placedAT, active, estimatedDeliveryTime ) VALUES (c345f4fa-5ab3-4314-96cb-a5b08153e7ea,5a2bb99f-88d2-4612-ac60-774aea9b8de4,'Karen Franco',{ef634e30-5aee-42f6-a747-5046d3111388},398608f2-24da-4129-a5c1-dd35aa3cfed8,'2020-10-09 16:14:04.574+0000',True,-1);
INSERT INTO orderTable (orderId, orderedFrom, orderedBy, containsPizzas, paymentID, placedAT, active, estimatedDeliveryTime ) VALUES (385364d4-add9-4ac8-8ca6-0a8d78d5040f,5a2bb99f-88d2-4612-ac60-774aea9b8de4,'Emily Wolfe',{203e75f7-6153-4a84-b774-de1ab1f22a05},8f834ccd-2c2a-4f66-95f9-6fcd2cc1a408,'2020-10-09 16:10:04.813+0000',True,-1);
INSERT INTO orderTable (orderId, orderedFrom, orderedBy, containsPizzas, paymentID, placedAT, active, estimatedDeliveryTime ) VALUES (ada9cbf0-8d1f-4925-b015-9fa2d1a42bed,b18b3932-a4ef-485c-a182-8e67b04c208c,'Jeffery Stanton',{2ac55689-be18-4b95-a2aa-52462a36e6a2},0f13da6b-8632-41d3-acea-f4b1bdfc34bf,'2020-10-09 16:10:04.904+0000',True,-1);
INSERT INTO orderTable (orderId, orderedFrom, orderedBy, containsPizzas, paymentID, placedAT, active, estimatedDeliveryTime ) VALUES (8f373e5e-4cad-4f5c-90f7-273f7ff8da4b,b18b3932-a4ef-485c-a182-8e67b04c208c,'Kimberly Branch',{9a403fd5-1543-4e04-91f2-62b99e5548db},54dbe01d-55de-4b42-9bcf-2d553fc34411,'2020-10-09 16:13:04.986+0000',True,-1);
INSERT INTO orderTable (orderId, orderedFrom, orderedBy, containsPizzas, paymentID, placedAT, active, estimatedDeliveryTime ) VALUES (ffbe3fe5-3987-4225-a2c6-471423adfef5,b18b3932-a4ef-485c-a182-8e67b04c208c,'Hunter Kim',{f3ed9d67-c3e2-4248-8f26-0beb370d5f93},bad25e7a-1e47-4f98-92a5-a85e2e2d8a03,'2020-10-09 16:13:04.864+0000',True,-1);
INSERT INTO orderTable (orderId, orderedFrom, orderedBy, containsPizzas, paymentID, placedAT, active, estimatedDeliveryTime ) VALUES (d75616c9-2a4b-4a31-a0fe-5b08855ecb70,5a2bb99f-88d2-4612-ac60-774aea9b8de4,'Gwendolyn Mclaughlin',{1a2833b8-b522-445d-ae30-74880d7a247f},2ffce2c4-d40d-41fd-ab81-3573a3d482af,'2020-10-09 16:14:04.826+0000',True,-1);
INSERT INTO orderTable (orderId, orderedFrom, orderedBy, containsPizzas, paymentID, placedAT, active, estimatedDeliveryTime ) VALUES (8434d2be-49d5-4c72-af24-981f04e3c196,5a2bb99f-88d2-4612-ac60-774aea9b8de4,'Nathan Reeves',{378fe289-f002-490d-835a-96d69a100abf},6974b6d0-709b-471a-8681-b604e6a99f91,'2020-10-09 16:14:04.911+0000',True,-1);
INSERT INTO orderTable (orderId, orderedFrom, orderedBy, containsPizzas, paymentID, placedAT, active, estimatedDeliveryTime ) VALUES (601ca3ab-c72f-452d-901f-112d75a6d8b9,7098813e-4624-462a-81a1-7e0e4e67631d,'Alexandra Small',{56421056-f015-402c-b819-99b335c8731a},2961cc7f-056f-4205-8d4f-82d00a81966a,'2020-10-09 16:12:04.616+0000',True,-1);
INSERT INTO orderTable (orderId, orderedFrom, orderedBy, containsPizzas, paymentID, placedAT, active, estimatedDeliveryTime ) VALUES (f02752a4-398d-4914-918f-88a35e23513a,7098813e-4624-462a-81a1-7e0e4e67631d,'Timothy Smith',{f0a76e0b-bfd2-4574-8d3f-61651332aa67},05fd4e59-9933-40bd-83f8-599f557bc9f6,'2020-10-09 16:14:04.658+0000',True,-1);
INSERT INTO orderTable (orderId, orderedFrom, orderedBy, containsPizzas, paymentID, placedAT, active, estimatedDeliveryTime ) VALUES (806677d4-34f8-45d8-96b1-4b52b01eb714,7098813e-4624-462a-81a1-7e0e4e67631d,'Joseph Reed',{14280203-8e87-40a3-9eb0-ee0a3957f9e9},a71fe3f0-3f55-487f-9b64-17587f40694e,'2020-10-09 16:08:04.577+0000',True,-1);
INSERT INTO orderTable (orderId, orderedFrom, orderedBy, containsPizzas, paymentID, placedAT, active, estimatedDeliveryTime ) VALUES (ce6e1eec-e949-40d6-95a2-72b197b50a35,b18b3932-a4ef-485c-a182-8e67b04c208c,'Joseph Hawkins',{17f86318-c900-4ed2-947b-90a2a3b86e1b},4079f913-503f-4ebb-ac98-4aa4d1d03f5e,'2020-10-09 16:09:04.727+0000',True,-1);
INSERT INTO orderTable (orderId, orderedFrom, orderedBy, containsPizzas, paymentID, placedAT, active, estimatedDeliveryTime ) VALUES (a14787b7-2fd0-46eb-b670-aa92f6a96ead,b18b3932-a4ef-485c-a182-8e67b04c208c,'Debra Andrews',{03054769-21bf-4337-baf1-4927b3fb2e45},bf79288e-441e-4d85-9e67-fafcefb45eec,'2020-10-09 16:09:04.821+0000',True,-1);
INSERT INTO orderTable (orderId, orderedFrom, orderedBy, containsPizzas, paymentID, placedAT, active, estimatedDeliveryTime ) VALUES (f682d32f-4e11-4394-a4a3-c0eb0880a14b,b18b3932-a4ef-485c-a182-8e67b04c208c,'Benjamin Frye',{f6622afc-fc55-4eb5-8ae4-506f8842ac64},58a1c776-6ed2-4193-9979-2dcc49a04b24,'2020-10-09 16:11:04.770+0000',True,-1);
INSERT INTO orderTable (orderId, orderedFrom, orderedBy, containsPizzas, paymentID, placedAT, active, estimatedDeliveryTime ) VALUES (3023d9d3-e0e5-4692-8570-40432c4a6005,b18b3932-a4ef-485c-a182-8e67b04c208c,'Joseph Johnson',{dfde8495-e4f5-4c74-b8fa-6f73748f548a},7fd777e8-eb04-4a78-b3ef-205337085658,'2020-10-09 16:10:04.640+0000',True,-1);
INSERT INTO orderTable (orderId, orderedFrom, orderedBy, containsPizzas, paymentID, placedAT, active, estimatedDeliveryTime ) VALUES (1774e9ac-885f-4154-a4c0-f181765f490d,5a2bb99f-88d2-4612-ac60-774aea9b8de4,'Eugene Barr',{f83537b0-25c9-4a8e-b3ba-850f5c0d8b91},30759031-4911-43f9-8761-9057622ce567,'2020-10-09 16:13:04.906+0000',True,-1);
INSERT INTO orderTable (orderId, orderedFrom, orderedBy, containsPizzas, paymentID, placedAT, active, estimatedDeliveryTime ) VALUES (c6a0e33e-c55a-413d-bfb9-83cfc1aa5c83,b18b3932-a4ef-485c-a182-8e67b04c208c,'Jennifer Wilkinson',{e14bc04b-0d91-4a10-9750-80c1d8bee38d},2298f1aa-d3e3-42a2-8ac1-7152ad28592c,'2020-10-09 16:08:04.532+0000',True,-1);
INSERT INTO orderTable (orderId, orderedFrom, orderedBy, containsPizzas, paymentID, placedAT, active, estimatedDeliveryTime ) VALUES (21dec7fa-c2c7-4c55-abd9-570f7dcd6c0c,b18b3932-a4ef-485c-a182-8e67b04c208c,'Daniel Dixon',{147712af-28a0-4762-aabc-86030a8e3c92},c649f1e4-8f61-4807-aef3-49eeb8468670,'2020-10-09 16:14:04.698+0000',True,-1);
INSERT INTO orderTable (orderId, orderedFrom, orderedBy, containsPizzas, paymentID, placedAT, active, estimatedDeliveryTime ) VALUES (f0a203d4-e324-405b-aff0-d05478add4bd,b18b3932-a4ef-485c-a182-8e67b04c208c,'Scott Flores',{3332bbcf-4ce3-40fd-aa42-c15a219c479d},ef0aea75-2a68-464b-950e-88a888884fa9,'2020-10-09 16:09:04.958+0000',True,-1);
INSERT INTO orderTable (orderId, orderedFrom, orderedBy, containsPizzas, paymentID, placedAT, active, estimatedDeliveryTime ) VALUES (9d677262-9759-46a0-9be2-4d2e6fcfe173,b18b3932-a4ef-485c-a182-8e67b04c208c,'Lucas Cole',{2c66024e-97ab-46d3-b311-c8ab2e74a896},895d9f25-a013-4320-8c44-6a536283f883,'2020-10-09 16:08:04.832+0000',True,-1);
INSERT INTO orderTable (orderId, orderedFrom, orderedBy, containsPizzas, paymentID, placedAT, active, estimatedDeliveryTime ) VALUES (e7c3873a-4828-4c82-b8b6-803dda9567fe,5a2bb99f-88d2-4612-ac60-774aea9b8de4,'Luke Meyer',{175aea58-1eb9-42d7-afe8-6c1a54b76af9},2faf12ae-e554-42d0-8a35-4851b9b1def2,'2020-10-09 16:09:04.641+0000',True,-1);
INSERT INTO orderTable (orderId, orderedFrom, orderedBy, containsPizzas, paymentID, placedAT, active, estimatedDeliveryTime ) VALUES (ca45ff1f-5633-4ab6-a1bb-76dfe53c65c5,5a2bb99f-88d2-4612-ac60-774aea9b8de4,'Sarah Henderson',{04814975-4ce3-4436-aca8-ca200c8f2739},20057d2f-b636-4c7a-b2c9-87018bbe1f9d,'2020-10-09 16:09:04.863+0000',True,-1);
INSERT INTO orderTable (orderId, orderedFrom, orderedBy, containsPizzas, paymentID, placedAT, active, estimatedDeliveryTime ) VALUES (8e5e5918-ef09-4616-b72f-1546ade4f94b,5a2bb99f-88d2-4612-ac60-774aea9b8de4,'Anthony Miller',{569928fe-e937-42d4-8225-a38d22e42606},e5d2e6be-028f-44fe-862f-f8897b775e59,'2020-10-09 16:14:04.869+0000',True,-1);
INSERT INTO orderTable (orderId, orderedFrom, orderedBy, containsPizzas, paymentID, placedAT, active, estimatedDeliveryTime ) VALUES (5ee27389-403f-42a3-af18-4d32c04b3b3a,7098813e-4624-462a-81a1-7e0e4e67631d,'Brittany Turner',{7fb1e7fb-c042-4b6b-bb91-e0b5c07184e8},abccaba5-399c-40e6-9ceb-0c75dd960f62,'2020-10-09 16:10:04.771+0000',True,-1);
INSERT INTO orderTable (orderId, orderedFrom, orderedBy, containsPizzas, paymentID, placedAT, active, estimatedDeliveryTime ) VALUES (cf64acf4-a663-4926-9a05-74c60daf7768,b18b3932-a4ef-485c-a182-8e67b04c208c,'Taylor Stone',{69422396-1058-440b-b810-92905d31923e},e6dfcbcf-bcb9-45aa-9447-8b1968957b83,'2020-10-09 16:10:04.731+0000',True,-1);
INSERT INTO orderTable (orderId, orderedFrom, orderedBy, containsPizzas, paymentID, placedAT, active, estimatedDeliveryTime ) VALUES (738cbccb-084f-46f1-9bee-b44add451fe2,5a2bb99f-88d2-4612-ac60-774aea9b8de4,'Amanda Webb',{39e91684-fe19-45ac-9358-4a5cfb241054},531382a3-824e-483d-b2b9-831007ed32e7,'2020-10-09 16:08:04.480+0000',True,-1);
INSERT INTO orderTable (orderId, orderedFrom, orderedBy, containsPizzas, paymentID, placedAT, active, estimatedDeliveryTime ) VALUES (b7372bf2-572c-491e-9014-7c04b14e6714,b18b3932-a4ef-485c-a182-8e67b04c208c,'Isabel Reed',{41c0b55b-db88-45b9-86bd-155a63eaa445},31d925d5-7843-4301-981f-2dbfb906ca88,'2020-10-09 16:09:04.904+0000',True,-1);
INSERT INTO orderTable (orderId, orderedFrom, orderedBy, containsPizzas, paymentID, placedAT, active, estimatedDeliveryTime ) VALUES (568258b2-3510-474d-ac5b-6180340bd4dc,5a2bb99f-88d2-4612-ac60-774aea9b8de4,'Desiree Rush',{38521e4e-5755-45af-8034-631d5b68d4f4},35422016-6ce8-4a2c-9022-6b3b3914726c,'2020-10-09 16:12:04.490+0000',True,-1);
INSERT INTO orderTable (orderId, orderedFrom, orderedBy, containsPizzas, paymentID, placedAT, active, estimatedDeliveryTime ) VALUES (0a6dfe17-3ef7-4922-86d6-7771cd852834,5a2bb99f-88d2-4612-ac60-774aea9b8de4,'Chelsea Garrett',{fa66cb8c-07f7-4d33-ab3e-212088b94946},cdcecc01-7838-472c-86bf-a7c057d0d811,'2020-10-09 16:13:05.030+0000',True,-1);
INSERT INTO orderTable (orderId, orderedFrom, orderedBy, containsPizzas, paymentID, placedAT, active, estimatedDeliveryTime ) VALUES (34a795fe-ca6d-4758-b21f-9e64fdd56e60,b18b3932-a4ef-485c-a182-8e67b04c208c,'David Nelson',{4e7f1d01-d2bd-4aa4-9c9c-6b2befb4538a},3c398f62-c238-4696-9f03-6e4573b65a64,'2020-10-09 16:12:04.449+0000',True,-1);
INSERT INTO orderTable (orderId, orderedFrom, orderedBy, containsPizzas, paymentID, placedAT, active, estimatedDeliveryTime ) VALUES (416f06dc-cf3e-4258-9e3d-cd456c655bb6,7098813e-4624-462a-81a1-7e0e4e67631d,'Cody Harrison',{eecafeb4-b9aa-4f32-8a44-f13b0fc1fb53},bfca7d32-8470-4fdb-873b-46a81e911207,'2020-10-09 16:08:04.632+0000',True,-1);
INSERT INTO orderTable (orderId, orderedFrom, orderedBy, containsPizzas, paymentID, placedAT, active, estimatedDeliveryTime ) VALUES (1d78ec54-5137-4373-b96f-0fbc54eb4b12,7098813e-4624-462a-81a1-7e0e4e67631d,'Brooke Bush',{1f3cea3f-6e28-4714-afc4-8335a5bee1b5},a00d9fcb-ea90-414e-8a2d-a468d43463af,'2020-10-09 16:13:04.690+0000',True,-1);
INSERT INTO orderTable (orderId, orderedFrom, orderedBy, containsPizzas, paymentID, placedAT, active, estimatedDeliveryTime ) VALUES (d3e3b1cb-6edb-410d-bd37-42ec214d1358,b18b3932-a4ef-485c-a182-8e67b04c208c,'Angela Green',{64784cad-41c0-476e-99fe-3f035465da4a},bc37d930-199b-4a3e-92cd-8df514a32532,'2020-10-09 16:11:04.812+0000',True,-1);
INSERT INTO orderTable (orderId, orderedFrom, orderedBy, containsPizzas, paymentID, placedAT, active, estimatedDeliveryTime ) VALUES (0abbc8d6-23f0-4696-930f-30b6e5d09857,b18b3932-a4ef-485c-a182-8e67b04c208c,'David Lara',{2db9f011-4d96-40f4-ae4d-a49aacfb4b2b},0379bb17-7b46-4140-be8b-548554d1a022,'2020-10-09 16:10:04.598+0000',True,-1);


CREATE TABLE orderByStore (
  orderedFrom UUID,
  placedAT TIMESTAMP,
  orderID UUID,
  PRIMARY KEY (orderedFrom, placedAt)
);

INSERT INTO orderByStore (orderedFrom, placedAT, orderID) VALUES (5a2bb99f-88d2-4612-ac60-774aea9b8de4,'2020-10-09 16:06:56.956+0000',373da967-c790-454e-a978-b5a46ec344e9);
INSERT INTO orderByStore (orderedFrom, placedAT, orderID) VALUES (5a2bb99f-88d2-4612-ac60-774aea9b8de4,'2020-10-09 16:06:57.012+0000',2dbab543-bb2d-4766-8c91-439f5688b2f1);
INSERT INTO orderByStore (orderedFrom, placedAT, orderID) VALUES (5a2bb99f-88d2-4612-ac60-774aea9b8de4,'2020-10-09 16:06:57.132+0000',2e1c6b7a-7757-4ede-8b0e-a3f5a07a263a);
INSERT INTO orderByStore (orderedFrom, placedAT, orderID) VALUES (5a2bb99f-88d2-4612-ac60-774aea9b8de4,'2020-10-09 16:06:57.241+0000',bd592e06-a030-4dc5-948a-4b6cdd8a653c);
INSERT INTO orderByStore (orderedFrom, placedAT, orderID) VALUES (5a2bb99f-88d2-4612-ac60-774aea9b8de4,'2020-10-09 16:06:57.294+0000',84994022-041d-4d95-a752-79c2f09d651a);
INSERT INTO orderByStore (orderedFrom, placedAT, orderID) VALUES (5a2bb99f-88d2-4612-ac60-774aea9b8de4,'2020-10-09 16:08:04.480+0000',738cbccb-084f-46f1-9bee-b44add451fe2);
INSERT INTO orderByStore (orderedFrom, placedAT, orderID) VALUES (5a2bb99f-88d2-4612-ac60-774aea9b8de4,'2020-10-09 16:08:04.787+0000',ff01189b-3ae9-4ff2-a2bc-4cdff699454f);
INSERT INTO orderByStore (orderedFrom, placedAT, orderID) VALUES (5a2bb99f-88d2-4612-ac60-774aea9b8de4,'2020-10-09 16:09:04.641+0000',e7c3873a-4828-4c82-b8b6-803dda9567fe);
INSERT INTO orderByStore (orderedFrom, placedAT, orderID) VALUES (5a2bb99f-88d2-4612-ac60-774aea9b8de4,'2020-10-09 16:09:04.778+0000',44f789d6-4ebb-421b-9c54-ed4bc363d360);
INSERT INTO orderByStore (orderedFrom, placedAT, orderID) VALUES (5a2bb99f-88d2-4612-ac60-774aea9b8de4,'2020-10-09 16:09:04.863+0000',ca45ff1f-5633-4ab6-a1bb-76dfe53c65c5);
INSERT INTO orderByStore (orderedFrom, placedAT, orderID) VALUES (5a2bb99f-88d2-4612-ac60-774aea9b8de4,'2020-10-09 16:09:05.020+0000',7a8c0c2b-f337-4ba7-9f6c-9fb7e63fa259);
INSERT INTO orderByStore (orderedFrom, placedAT, orderID) VALUES (5a2bb99f-88d2-4612-ac60-774aea9b8de4,'2020-10-09 16:10:04.555+0000',432da2bb-6486-4749-987c-70c2b5ba7f1a);
INSERT INTO orderByStore (orderedFrom, placedAT, orderID) VALUES (5a2bb99f-88d2-4612-ac60-774aea9b8de4,'2020-10-09 16:10:04.684+0000',2e48854a-c59d-4171-8a25-563c01efb7d4);
INSERT INTO orderByStore (orderedFrom, placedAT, orderID) VALUES (5a2bb99f-88d2-4612-ac60-774aea9b8de4,'2020-10-09 16:10:04.813+0000',385364d4-add9-4ac8-8ca6-0a8d78d5040f);
INSERT INTO orderByStore (orderedFrom, placedAT, orderID) VALUES (5a2bb99f-88d2-4612-ac60-774aea9b8de4,'2020-10-09 16:10:04.858+0000',2067a957-6cb3-4e31-b571-5a3b77045efe);
INSERT INTO orderByStore (orderedFrom, placedAT, orderID) VALUES (5a2bb99f-88d2-4612-ac60-774aea9b8de4,'2020-10-09 16:11:04.943+0000',dceaebcf-d084-4489-a9d4-a32868a07dc8);
INSERT INTO orderByStore (orderedFrom, placedAT, orderID) VALUES (5a2bb99f-88d2-4612-ac60-774aea9b8de4,'2020-10-09 16:11:05.030+0000',9e27952a-cee7-449a-b8e1-26ae2728b1d0);
INSERT INTO orderByStore (orderedFrom, placedAT, orderID) VALUES (5a2bb99f-88d2-4612-ac60-774aea9b8de4,'2020-10-09 16:12:04.490+0000',568258b2-3510-474d-ac5b-6180340bd4dc);
INSERT INTO orderByStore (orderedFrom, placedAT, orderID) VALUES (5a2bb99f-88d2-4612-ac60-774aea9b8de4,'2020-10-09 16:12:04.663+0000',19c9de5c-4293-4e2f-9280-a58ca7ec80ce);
INSERT INTO orderByStore (orderedFrom, placedAT, orderID) VALUES (5a2bb99f-88d2-4612-ac60-774aea9b8de4,'2020-10-09 16:12:04.710+0000',f46c3113-8afe-42f9-bbce-c86566b4bcef);
INSERT INTO orderByStore (orderedFrom, placedAT, orderID) VALUES (5a2bb99f-88d2-4612-ac60-774aea9b8de4,'2020-10-09 16:13:04.733+0000',4792ffeb-2259-44a2-b35d-31bf2df38b95);
INSERT INTO orderByStore (orderedFrom, placedAT, orderID) VALUES (5a2bb99f-88d2-4612-ac60-774aea9b8de4,'2020-10-09 16:13:04.906+0000',1774e9ac-885f-4154-a4c0-f181765f490d);
INSERT INTO orderByStore (orderedFrom, placedAT, orderID) VALUES (5a2bb99f-88d2-4612-ac60-774aea9b8de4,'2020-10-09 16:13:05.030+0000',0a6dfe17-3ef7-4922-86d6-7771cd852834);
INSERT INTO orderByStore (orderedFrom, placedAT, orderID) VALUES (5a2bb99f-88d2-4612-ac60-774aea9b8de4,'2020-10-09 16:14:04.532+0000',6f461e2a-c67d-4c74-b786-76cc642e2aad);
INSERT INTO orderByStore (orderedFrom, placedAT, orderID) VALUES (5a2bb99f-88d2-4612-ac60-774aea9b8de4,'2020-10-09 16:14:04.574+0000',c345f4fa-5ab3-4314-96cb-a5b08153e7ea);
INSERT INTO orderByStore (orderedFrom, placedAT, orderID) VALUES (5a2bb99f-88d2-4612-ac60-774aea9b8de4,'2020-10-09 16:14:04.738+0000',b07fc505-3569-4d51-a3b5-59bd2f29c340);
INSERT INTO orderByStore (orderedFrom, placedAT, orderID) VALUES (5a2bb99f-88d2-4612-ac60-774aea9b8de4,'2020-10-09 16:14:04.782+0000',1436c6a7-b4c6-420a-8edf-38bc08db3739);
INSERT INTO orderByStore (orderedFrom, placedAT, orderID) VALUES (5a2bb99f-88d2-4612-ac60-774aea9b8de4,'2020-10-09 16:14:04.826+0000',d75616c9-2a4b-4a31-a0fe-5b08855ecb70);
INSERT INTO orderByStore (orderedFrom, placedAT, orderID) VALUES (5a2bb99f-88d2-4612-ac60-774aea9b8de4,'2020-10-09 16:14:04.869+0000',8e5e5918-ef09-4616-b72f-1546ade4f94b);
INSERT INTO orderByStore (orderedFrom, placedAT, orderID) VALUES (5a2bb99f-88d2-4612-ac60-774aea9b8de4,'2020-10-09 16:14:04.911+0000',8434d2be-49d5-4c72-af24-981f04e3c196);
INSERT INTO orderByStore (orderedFrom, placedAT, orderID) VALUES (7098813e-4624-462a-81a1-7e0e4e67631d,'2020-10-09 16:06:57.188+0000',27aa345c-dc96-4099-9599-93824940d1e9);
INSERT INTO orderByStore (orderedFrom, placedAT, orderID) VALUES (7098813e-4624-462a-81a1-7e0e4e67631d,'2020-10-09 16:08:04.577+0000',806677d4-34f8-45d8-96b1-4b52b01eb714);
INSERT INTO orderByStore (orderedFrom, placedAT, orderID) VALUES (7098813e-4624-462a-81a1-7e0e4e67631d,'2020-10-09 16:08:04.632+0000',416f06dc-cf3e-4258-9e3d-cd456c655bb6);
INSERT INTO orderByStore (orderedFrom, placedAT, orderID) VALUES (7098813e-4624-462a-81a1-7e0e4e67631d,'2020-10-09 16:08:04.681+0000',9e3c3466-e9d3-49bd-81ba-d9edde2f162d);
INSERT INTO orderByStore (orderedFrom, placedAT, orderID) VALUES (7098813e-4624-462a-81a1-7e0e4e67631d,'2020-10-09 16:09:04.592+0000',543623f9-49cb-444e-b9d2-1604a4ee0cd5);
INSERT INTO orderByStore (orderedFrom, placedAT, orderID) VALUES (7098813e-4624-462a-81a1-7e0e4e67631d,'2020-10-09 16:09:04.684+0000',fe741c7e-963c-47cd-85fc-3436bd02da82);
INSERT INTO orderByStore (orderedFrom, placedAT, orderID) VALUES (7098813e-4624-462a-81a1-7e0e4e67631d,'2020-10-09 16:10:04.498+0000',ec85a551-f506-4957-bb00-dac1a954a01e);
INSERT INTO orderByStore (orderedFrom, placedAT, orderID) VALUES (7098813e-4624-462a-81a1-7e0e4e67631d,'2020-10-09 16:10:04.771+0000',5ee27389-403f-42a3-af18-4d32c04b3b3a);
INSERT INTO orderByStore (orderedFrom, placedAT, orderID) VALUES (7098813e-4624-462a-81a1-7e0e4e67631d,'2020-10-09 16:11:04.898+0000',24408218-0e26-4089-8ef6-a39ec804e2e5);
INSERT INTO orderByStore (orderedFrom, placedAT, orderID) VALUES (7098813e-4624-462a-81a1-7e0e4e67631d,'2020-10-09 16:11:05.161+0000',f7eb68a7-3a3f-44b7-9653-7b46922bd7a0);
INSERT INTO orderByStore (orderedFrom, placedAT, orderID) VALUES (7098813e-4624-462a-81a1-7e0e4e67631d,'2020-10-09 16:12:04.616+0000',601ca3ab-c72f-452d-901f-112d75a6d8b9);
INSERT INTO orderByStore (orderedFrom, placedAT, orderID) VALUES (7098813e-4624-462a-81a1-7e0e4e67631d,'2020-10-09 16:12:04.842+0000',3c4622eb-d936-454d-8f97-2211ce03ba3a);
INSERT INTO orderByStore (orderedFrom, placedAT, orderID) VALUES (7098813e-4624-462a-81a1-7e0e4e67631d,'2020-10-09 16:13:04.690+0000',1d78ec54-5137-4373-b96f-0fbc54eb4b12);
INSERT INTO orderByStore (orderedFrom, placedAT, orderID) VALUES (7098813e-4624-462a-81a1-7e0e4e67631d,'2020-10-09 16:13:04.823+0000',2a4541e9-c33f-4605-a736-19cec3c07011);
INSERT INTO orderByStore (orderedFrom, placedAT, orderID) VALUES (7098813e-4624-462a-81a1-7e0e4e67631d,'2020-10-09 16:13:04.945+0000',1e8b03b3-0514-4e3c-bb19-b4701582b252);
INSERT INTO orderByStore (orderedFrom, placedAT, orderID) VALUES (7098813e-4624-462a-81a1-7e0e4e67631d,'2020-10-09 16:14:04.658+0000',f02752a4-398d-4914-918f-88a35e23513a);
INSERT INTO orderByStore (orderedFrom, placedAT, orderID) VALUES (b18b3932-a4ef-485c-a182-8e67b04c208c,'2020-10-09 16:06:56.896+0000',b93e8a4a-a9c7-4553-a7b2-f05475569d36);
INSERT INTO orderByStore (orderedFrom, placedAT, orderID) VALUES (b18b3932-a4ef-485c-a182-8e67b04c208c,'2020-10-09 16:06:57.075+0000',4fcfa2de-ba46-4d2f-a2f4-13a721722573);
INSERT INTO orderByStore (orderedFrom, placedAT, orderID) VALUES (b18b3932-a4ef-485c-a182-8e67b04c208c,'2020-10-09 16:06:57.347+0000',ad75ba81-4a5c-44a7-a0f3-2d6f4b4b4958);
INSERT INTO orderByStore (orderedFrom, placedAT, orderID) VALUES (b18b3932-a4ef-485c-a182-8e67b04c208c,'2020-10-09 16:06:57.398+0000',471767a2-f07b-4f1e-8c35-752f3564670d);
INSERT INTO orderByStore (orderedFrom, placedAT, orderID) VALUES (b18b3932-a4ef-485c-a182-8e67b04c208c,'2020-10-09 16:08:04.532+0000',c6a0e33e-c55a-413d-bfb9-83cfc1aa5c83);
INSERT INTO orderByStore (orderedFrom, placedAT, orderID) VALUES (b18b3932-a4ef-485c-a182-8e67b04c208c,'2020-10-09 16:08:04.738+0000',966d2851-ec6b-4709-90fd-1cb51e6e99f3);
INSERT INTO orderByStore (orderedFrom, placedAT, orderID) VALUES (b18b3932-a4ef-485c-a182-8e67b04c208c,'2020-10-09 16:08:04.832+0000',9d677262-9759-46a0-9be2-4d2e6fcfe173);
INSERT INTO orderByStore (orderedFrom, placedAT, orderID) VALUES (b18b3932-a4ef-485c-a182-8e67b04c208c,'2020-10-09 16:08:04.876+0000',e8debfe5-9f74-4d26-88f4-e06473f857cf);
INSERT INTO orderByStore (orderedFrom, placedAT, orderID) VALUES (b18b3932-a4ef-485c-a182-8e67b04c208c,'2020-10-09 16:08:04.923+0000',d78c51ed-41ab-4716-afb2-fdb9673851d8);
INSERT INTO orderByStore (orderedFrom, placedAT, orderID) VALUES (b18b3932-a4ef-485c-a182-8e67b04c208c,'2020-10-09 16:09:04.727+0000',ce6e1eec-e949-40d6-95a2-72b197b50a35);
INSERT INTO orderByStore (orderedFrom, placedAT, orderID) VALUES (b18b3932-a4ef-485c-a182-8e67b04c208c,'2020-10-09 16:09:04.821+0000',a14787b7-2fd0-46eb-b670-aa92f6a96ead);
INSERT INTO orderByStore (orderedFrom, placedAT, orderID) VALUES (b18b3932-a4ef-485c-a182-8e67b04c208c,'2020-10-09 16:09:04.904+0000',b7372bf2-572c-491e-9014-7c04b14e6714);
INSERT INTO orderByStore (orderedFrom, placedAT, orderID) VALUES (b18b3932-a4ef-485c-a182-8e67b04c208c,'2020-10-09 16:09:04.958+0000',f0a203d4-e324-405b-aff0-d05478add4bd);
INSERT INTO orderByStore (orderedFrom, placedAT, orderID) VALUES (b18b3932-a4ef-485c-a182-8e67b04c208c,'2020-10-09 16:10:04.598+0000',0abbc8d6-23f0-4696-930f-30b6e5d09857);
INSERT INTO orderByStore (orderedFrom, placedAT, orderID) VALUES (b18b3932-a4ef-485c-a182-8e67b04c208c,'2020-10-09 16:10:04.640+0000',3023d9d3-e0e5-4692-8570-40432c4a6005);
INSERT INTO orderByStore (orderedFrom, placedAT, orderID) VALUES (b18b3932-a4ef-485c-a182-8e67b04c208c,'2020-10-09 16:10:04.731+0000',cf64acf4-a663-4926-9a05-74c60daf7768);
INSERT INTO orderByStore (orderedFrom, placedAT, orderID) VALUES (b18b3932-a4ef-485c-a182-8e67b04c208c,'2020-10-09 16:10:04.904+0000',ada9cbf0-8d1f-4925-b015-9fa2d1a42bed);
INSERT INTO orderByStore (orderedFrom, placedAT, orderID) VALUES (b18b3932-a4ef-485c-a182-8e67b04c208c,'2020-10-09 16:11:04.770+0000',f682d32f-4e11-4394-a4a3-c0eb0880a14b);
INSERT INTO orderByStore (orderedFrom, placedAT, orderID) VALUES (b18b3932-a4ef-485c-a182-8e67b04c208c,'2020-10-09 16:11:04.812+0000',d3e3b1cb-6edb-410d-bd37-42ec214d1358);
INSERT INTO orderByStore (orderedFrom, placedAT, orderID) VALUES (b18b3932-a4ef-485c-a182-8e67b04c208c,'2020-10-09 16:11:04.855+0000',6e330978-3bc9-4793-a179-ed47a5f55f55);
INSERT INTO orderByStore (orderedFrom, placedAT, orderID) VALUES (b18b3932-a4ef-485c-a182-8e67b04c208c,'2020-10-09 16:11:04.984+0000',7e723ea6-cbba-4b3d-91b1-6729a18e8ac0);
INSERT INTO orderByStore (orderedFrom, placedAT, orderID) VALUES (b18b3932-a4ef-485c-a182-8e67b04c208c,'2020-10-09 16:11:05.077+0000',12f63894-844b-4372-8857-32c1c416de77);
INSERT INTO orderByStore (orderedFrom, placedAT, orderID) VALUES (b18b3932-a4ef-485c-a182-8e67b04c208c,'2020-10-09 16:11:05.117+0000',366f46bc-5ffe-4e3e-960b-e8bd2557a26c);
INSERT INTO orderByStore (orderedFrom, placedAT, orderID) VALUES (b18b3932-a4ef-485c-a182-8e67b04c208c,'2020-10-09 16:12:04.449+0000',34a795fe-ca6d-4758-b21f-9e64fdd56e60);
INSERT INTO orderByStore (orderedFrom, placedAT, orderID) VALUES (b18b3932-a4ef-485c-a182-8e67b04c208c,'2020-10-09 16:12:04.532+0000',f611d989-f120-4010-b92c-df393b13a5a0);
INSERT INTO orderByStore (orderedFrom, placedAT, orderID) VALUES (b18b3932-a4ef-485c-a182-8e67b04c208c,'2020-10-09 16:12:04.574+0000',c79fac0e-a231-48f0-92b8-7bdd65c6f752);
INSERT INTO orderByStore (orderedFrom, placedAT, orderID) VALUES (b18b3932-a4ef-485c-a182-8e67b04c208c,'2020-10-09 16:12:04.750+0000',b6b52ffd-c527-420f-b87e-01d1d10e211e);
INSERT INTO orderByStore (orderedFrom, placedAT, orderID) VALUES (b18b3932-a4ef-485c-a182-8e67b04c208c,'2020-10-09 16:12:04.798+0000',f59ecde2-0208-40fc-a48f-c1181bb1c7fb);
INSERT INTO orderByStore (orderedFrom, placedAT, orderID) VALUES (b18b3932-a4ef-485c-a182-8e67b04c208c,'2020-10-09 16:13:04.781+0000',6d8c1311-55fd-4c2c-b84b-7265c5fbc8b6);
INSERT INTO orderByStore (orderedFrom, placedAT, orderID) VALUES (b18b3932-a4ef-485c-a182-8e67b04c208c,'2020-10-09 16:13:04.864+0000',ffbe3fe5-3987-4225-a2c6-471423adfef5);
INSERT INTO orderByStore (orderedFrom, placedAT, orderID) VALUES (b18b3932-a4ef-485c-a182-8e67b04c208c,'2020-10-09 16:13:04.986+0000',8f373e5e-4cad-4f5c-90f7-273f7ff8da4b);
INSERT INTO orderByStore (orderedFrom, placedAT, orderID) VALUES (b18b3932-a4ef-485c-a182-8e67b04c208c,'2020-10-09 16:13:05.072+0000',4e3a990d-e67d-4ecc-9f12-6e8c01e0af87);
INSERT INTO orderByStore (orderedFrom, placedAT, orderID) VALUES (b18b3932-a4ef-485c-a182-8e67b04c208c,'2020-10-09 16:14:04.619+0000',d2bbdb30-3e2f-4f42-992c-fd38d872acc1);
INSERT INTO orderByStore (orderedFrom, placedAT, orderID) VALUES (b18b3932-a4ef-485c-a182-8e67b04c208c,'2020-10-09 16:14:04.698+0000',21dec7fa-c2c7-4c55-abd9-570f7dcd6c0c);


CREATE TABLE orderByDeliveryEntity (
  deliveredBy TEXT,
  placedAT TIMESTAMP,
  orderID UUID,
  PRIMARY KEY (deliveredBy, placedAt)
);

CREATE TABLE stockTracker (
  storeID UUID,
  itemName TEXT,
  quantitySold FLOAT,
  dateSold TIMESTAMP,
  PRIMARY KEY (storeID, itemName, dateSold)
);

INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (7098813e-4624-462a-81a1-7e0e4e67631d,'Bacon',0,'2020-10-01 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (7098813e-4624-462a-81a1-7e0e4e67631d,'Bacon',2,'2020-10-02 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (7098813e-4624-462a-81a1-7e0e4e67631d,'Bacon',2,'2020-10-03 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (7098813e-4624-462a-81a1-7e0e4e67631d,'Bacon',0,'2020-10-04 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (7098813e-4624-462a-81a1-7e0e4e67631d,'Bacon',2,'2020-10-05 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (7098813e-4624-462a-81a1-7e0e4e67631d,'Bacon',0,'2020-10-06 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (7098813e-4624-462a-81a1-7e0e4e67631d,'Bacon',1,'2020-10-07 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (7098813e-4624-462a-81a1-7e0e4e67631d,'Bacon',0,'2020-10-08 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (7098813e-4624-462a-81a1-7e0e4e67631d,'Beef',1,'2020-10-01 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (7098813e-4624-462a-81a1-7e0e4e67631d,'Beef',0,'2020-10-02 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (7098813e-4624-462a-81a1-7e0e4e67631d,'Beef',1,'2020-10-03 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (7098813e-4624-462a-81a1-7e0e4e67631d,'Beef',2,'2020-10-04 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (7098813e-4624-462a-81a1-7e0e4e67631d,'Beef',2,'2020-10-05 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (7098813e-4624-462a-81a1-7e0e4e67631d,'Beef',2,'2020-10-06 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (7098813e-4624-462a-81a1-7e0e4e67631d,'Beef',2,'2020-10-07 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (7098813e-4624-462a-81a1-7e0e4e67631d,'Beef',0,'2020-10-08 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (7098813e-4624-462a-81a1-7e0e4e67631d,'Cheese',3,'2020-10-01 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (7098813e-4624-462a-81a1-7e0e4e67631d,'Cheese',2,'2020-10-02 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (7098813e-4624-462a-81a1-7e0e4e67631d,'Cheese',4,'2020-10-03 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (7098813e-4624-462a-81a1-7e0e4e67631d,'Cheese',4,'2020-10-04 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (7098813e-4624-462a-81a1-7e0e4e67631d,'Cheese',5,'2020-10-05 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (7098813e-4624-462a-81a1-7e0e4e67631d,'Cheese',4,'2020-10-06 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (7098813e-4624-462a-81a1-7e0e4e67631d,'Cheese',3,'2020-10-07 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (7098813e-4624-462a-81a1-7e0e4e67631d,'Cheese',0,'2020-10-08 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (7098813e-4624-462a-81a1-7e0e4e67631d,'Chicken',1,'2020-10-01 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (7098813e-4624-462a-81a1-7e0e4e67631d,'Chicken',1,'2020-10-02 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (7098813e-4624-462a-81a1-7e0e4e67631d,'Chicken',1,'2020-10-03 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (7098813e-4624-462a-81a1-7e0e4e67631d,'Chicken',1,'2020-10-04 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (7098813e-4624-462a-81a1-7e0e4e67631d,'Chicken',2,'2020-10-05 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (7098813e-4624-462a-81a1-7e0e4e67631d,'Chicken',2,'2020-10-06 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (7098813e-4624-462a-81a1-7e0e4e67631d,'Chicken',0,'2020-10-07 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (7098813e-4624-462a-81a1-7e0e4e67631d,'Chicken',1,'2020-10-08 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (7098813e-4624-462a-81a1-7e0e4e67631d,'Dough',2,'2020-10-01 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (7098813e-4624-462a-81a1-7e0e4e67631d,'Dough',6,'2020-10-02 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (7098813e-4624-462a-81a1-7e0e4e67631d,'Dough',3,'2020-10-03 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (7098813e-4624-462a-81a1-7e0e4e67631d,'Dough',2,'2020-10-04 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (7098813e-4624-462a-81a1-7e0e4e67631d,'Dough',4,'2020-10-05 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (7098813e-4624-462a-81a1-7e0e4e67631d,'Dough',2,'2020-10-06 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (7098813e-4624-462a-81a1-7e0e4e67631d,'Dough',6,'2020-10-07 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (7098813e-4624-462a-81a1-7e0e4e67631d,'Dough',1,'2020-10-08 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (7098813e-4624-462a-81a1-7e0e4e67631d,'Mushrooms',1,'2020-10-01 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (7098813e-4624-462a-81a1-7e0e4e67631d,'Mushrooms',1,'2020-10-02 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (7098813e-4624-462a-81a1-7e0e4e67631d,'Mushrooms',2,'2020-10-03 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (7098813e-4624-462a-81a1-7e0e4e67631d,'Mushrooms',0,'2020-10-04 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (7098813e-4624-462a-81a1-7e0e4e67631d,'Mushrooms',2,'2020-10-05 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (7098813e-4624-462a-81a1-7e0e4e67631d,'Mushrooms',2,'2020-10-06 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (7098813e-4624-462a-81a1-7e0e4e67631d,'Mushrooms',1,'2020-10-07 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (7098813e-4624-462a-81a1-7e0e4e67631d,'Mushrooms',0,'2020-10-08 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (7098813e-4624-462a-81a1-7e0e4e67631d,'Olives',1,'2020-10-01 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (7098813e-4624-462a-81a1-7e0e4e67631d,'Olives',1,'2020-10-02 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (7098813e-4624-462a-81a1-7e0e4e67631d,'Olives',1,'2020-10-03 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (7098813e-4624-462a-81a1-7e0e4e67631d,'Olives',0,'2020-10-04 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (7098813e-4624-462a-81a1-7e0e4e67631d,'Olives',1,'2020-10-05 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (7098813e-4624-462a-81a1-7e0e4e67631d,'Olives',2,'2020-10-06 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (7098813e-4624-462a-81a1-7e0e4e67631d,'Olives',0,'2020-10-07 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (7098813e-4624-462a-81a1-7e0e4e67631d,'Olives',0,'2020-10-08 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (7098813e-4624-462a-81a1-7e0e4e67631d,'Onion',1,'2020-10-01 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (7098813e-4624-462a-81a1-7e0e4e67631d,'Onion',0,'2020-10-02 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (7098813e-4624-462a-81a1-7e0e4e67631d,'Onion',0,'2020-10-03 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (7098813e-4624-462a-81a1-7e0e4e67631d,'Onion',1,'2020-10-04 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (7098813e-4624-462a-81a1-7e0e4e67631d,'Onion',2,'2020-10-05 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (7098813e-4624-462a-81a1-7e0e4e67631d,'Onion',1,'2020-10-06 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (7098813e-4624-462a-81a1-7e0e4e67631d,'Onion',1,'2020-10-07 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (7098813e-4624-462a-81a1-7e0e4e67631d,'Onion',0,'2020-10-08 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (7098813e-4624-462a-81a1-7e0e4e67631d,'Pepperoni',1,'2020-10-01 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (7098813e-4624-462a-81a1-7e0e4e67631d,'Pepperoni',1,'2020-10-02 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (7098813e-4624-462a-81a1-7e0e4e67631d,'Pepperoni',1,'2020-10-03 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (7098813e-4624-462a-81a1-7e0e4e67631d,'Pepperoni',1,'2020-10-04 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (7098813e-4624-462a-81a1-7e0e4e67631d,'Pepperoni',2,'2020-10-05 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (7098813e-4624-462a-81a1-7e0e4e67631d,'Pepperoni',2,'2020-10-06 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (7098813e-4624-462a-81a1-7e0e4e67631d,'Pepperoni',0,'2020-10-07 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (7098813e-4624-462a-81a1-7e0e4e67631d,'Pepperoni',0,'2020-10-08 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (7098813e-4624-462a-81a1-7e0e4e67631d,'Peppers',1,'2020-10-01 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (7098813e-4624-462a-81a1-7e0e4e67631d,'Peppers',1,'2020-10-02 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (7098813e-4624-462a-81a1-7e0e4e67631d,'Peppers',1,'2020-10-03 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (7098813e-4624-462a-81a1-7e0e4e67631d,'Peppers',0,'2020-10-04 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (7098813e-4624-462a-81a1-7e0e4e67631d,'Peppers',1,'2020-10-05 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (7098813e-4624-462a-81a1-7e0e4e67631d,'Peppers',2,'2020-10-06 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (7098813e-4624-462a-81a1-7e0e4e67631d,'Peppers',0,'2020-10-07 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (7098813e-4624-462a-81a1-7e0e4e67631d,'Peppers',0,'2020-10-08 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (7098813e-4624-462a-81a1-7e0e4e67631d,'Pineapple',1,'2020-10-01 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (7098813e-4624-462a-81a1-7e0e4e67631d,'Pineapple',0,'2020-10-02 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (7098813e-4624-462a-81a1-7e0e4e67631d,'Pineapple',1,'2020-10-03 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (7098813e-4624-462a-81a1-7e0e4e67631d,'Pineapple',0,'2020-10-04 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (7098813e-4624-462a-81a1-7e0e4e67631d,'Pineapple',2,'2020-10-05 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (7098813e-4624-462a-81a1-7e0e4e67631d,'Pineapple',2,'2020-10-06 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (7098813e-4624-462a-81a1-7e0e4e67631d,'Pineapple',0,'2020-10-07 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (7098813e-4624-462a-81a1-7e0e4e67631d,'Pineapple',1,'2020-10-08 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (7098813e-4624-462a-81a1-7e0e4e67631d,'Sausage',1,'2020-10-01 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (7098813e-4624-462a-81a1-7e0e4e67631d,'Sausage',0,'2020-10-02 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (7098813e-4624-462a-81a1-7e0e4e67631d,'Sausage',0,'2020-10-03 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (7098813e-4624-462a-81a1-7e0e4e67631d,'Sausage',1,'2020-10-04 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (7098813e-4624-462a-81a1-7e0e4e67631d,'Sausage',1,'2020-10-05 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (7098813e-4624-462a-81a1-7e0e4e67631d,'Sausage',2,'2020-10-06 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (7098813e-4624-462a-81a1-7e0e4e67631d,'Sausage',0,'2020-10-07 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (7098813e-4624-462a-81a1-7e0e4e67631d,'Sausage',0,'2020-10-08 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (7098813e-4624-462a-81a1-7e0e4e67631d,'SpicySauce',0,'2020-10-01 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (7098813e-4624-462a-81a1-7e0e4e67631d,'SpicySauce',0,'2020-10-02 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (7098813e-4624-462a-81a1-7e0e4e67631d,'SpicySauce',1,'2020-10-03 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (7098813e-4624-462a-81a1-7e0e4e67631d,'SpicySauce',1,'2020-10-04 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (7098813e-4624-462a-81a1-7e0e4e67631d,'SpicySauce',2,'2020-10-05 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (7098813e-4624-462a-81a1-7e0e4e67631d,'SpicySauce',1,'2020-10-06 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (7098813e-4624-462a-81a1-7e0e4e67631d,'SpicySauce',2,'2020-10-07 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (7098813e-4624-462a-81a1-7e0e4e67631d,'SpicySauce',0,'2020-10-08 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (7098813e-4624-462a-81a1-7e0e4e67631d,'TraditionalSauce',1,'2020-10-01 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (7098813e-4624-462a-81a1-7e0e4e67631d,'TraditionalSauce',3,'2020-10-02 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (7098813e-4624-462a-81a1-7e0e4e67631d,'TraditionalSauce',1,'2020-10-03 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (7098813e-4624-462a-81a1-7e0e4e67631d,'TraditionalSauce',1,'2020-10-04 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (7098813e-4624-462a-81a1-7e0e4e67631d,'TraditionalSauce',0,'2020-10-05 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (7098813e-4624-462a-81a1-7e0e4e67631d,'TraditionalSauce',1,'2020-10-06 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (7098813e-4624-462a-81a1-7e0e4e67631d,'TraditionalSauce',1,'2020-10-07 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (7098813e-4624-462a-81a1-7e0e4e67631d,'TraditionalSauce',1,'2020-10-08 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (b18b3932-a4ef-485c-a182-8e67b04c208c,'Bacon',1,'2020-10-01 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (b18b3932-a4ef-485c-a182-8e67b04c208c,'Bacon',2,'2020-10-02 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (b18b3932-a4ef-485c-a182-8e67b04c208c,'Bacon',2,'2020-10-03 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (b18b3932-a4ef-485c-a182-8e67b04c208c,'Bacon',3,'2020-10-04 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (b18b3932-a4ef-485c-a182-8e67b04c208c,'Bacon',1,'2020-10-05 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (b18b3932-a4ef-485c-a182-8e67b04c208c,'Bacon',2,'2020-10-06 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (b18b3932-a4ef-485c-a182-8e67b04c208c,'Bacon',0,'2020-10-07 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (b18b3932-a4ef-485c-a182-8e67b04c208c,'Bacon',1,'2020-10-08 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (b18b3932-a4ef-485c-a182-8e67b04c208c,'Beef',3,'2020-10-01 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (b18b3932-a4ef-485c-a182-8e67b04c208c,'Beef',1,'2020-10-02 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (b18b3932-a4ef-485c-a182-8e67b04c208c,'Beef',2,'2020-10-03 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (b18b3932-a4ef-485c-a182-8e67b04c208c,'Beef',2,'2020-10-04 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (b18b3932-a4ef-485c-a182-8e67b04c208c,'Beef',0,'2020-10-05 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (b18b3932-a4ef-485c-a182-8e67b04c208c,'Beef',2,'2020-10-06 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (b18b3932-a4ef-485c-a182-8e67b04c208c,'Beef',2,'2020-10-07 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (b18b3932-a4ef-485c-a182-8e67b04c208c,'Beef',1,'2020-10-08 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (b18b3932-a4ef-485c-a182-8e67b04c208c,'Cheese',10,'2020-10-01 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (b18b3932-a4ef-485c-a182-8e67b04c208c,'Cheese',6,'2020-10-02 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (b18b3932-a4ef-485c-a182-8e67b04c208c,'Cheese',5,'2020-10-03 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (b18b3932-a4ef-485c-a182-8e67b04c208c,'Cheese',5,'2020-10-04 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (b18b3932-a4ef-485c-a182-8e67b04c208c,'Cheese',10,'2020-10-05 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (b18b3932-a4ef-485c-a182-8e67b04c208c,'Cheese',6,'2020-10-06 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (b18b3932-a4ef-485c-a182-8e67b04c208c,'Cheese',5,'2020-10-07 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (b18b3932-a4ef-485c-a182-8e67b04c208c,'Cheese',4,'2020-10-08 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (b18b3932-a4ef-485c-a182-8e67b04c208c,'Chicken',1,'2020-10-01 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (b18b3932-a4ef-485c-a182-8e67b04c208c,'Chicken',1,'2020-10-02 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (b18b3932-a4ef-485c-a182-8e67b04c208c,'Chicken',2,'2020-10-03 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (b18b3932-a4ef-485c-a182-8e67b04c208c,'Chicken',2,'2020-10-04 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (b18b3932-a4ef-485c-a182-8e67b04c208c,'Chicken',2,'2020-10-05 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (b18b3932-a4ef-485c-a182-8e67b04c208c,'Chicken',1,'2020-10-06 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (b18b3932-a4ef-485c-a182-8e67b04c208c,'Chicken',1,'2020-10-07 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (b18b3932-a4ef-485c-a182-8e67b04c208c,'Chicken',0,'2020-10-08 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (b18b3932-a4ef-485c-a182-8e67b04c208c,'Dough',5,'2020-10-01 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (b18b3932-a4ef-485c-a182-8e67b04c208c,'Dough',8,'2020-10-02 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (b18b3932-a4ef-485c-a182-8e67b04c208c,'Dough',8,'2020-10-03 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (b18b3932-a4ef-485c-a182-8e67b04c208c,'Dough',5,'2020-10-04 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (b18b3932-a4ef-485c-a182-8e67b04c208c,'Dough',9,'2020-10-05 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (b18b3932-a4ef-485c-a182-8e67b04c208c,'Dough',6,'2020-10-06 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (b18b3932-a4ef-485c-a182-8e67b04c208c,'Dough',6,'2020-10-07 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (b18b3932-a4ef-485c-a182-8e67b04c208c,'Dough',3,'2020-10-08 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (b18b3932-a4ef-485c-a182-8e67b04c208c,'Mushrooms',2,'2020-10-01 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (b18b3932-a4ef-485c-a182-8e67b04c208c,'Mushrooms',2,'2020-10-02 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (b18b3932-a4ef-485c-a182-8e67b04c208c,'Mushrooms',2,'2020-10-03 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (b18b3932-a4ef-485c-a182-8e67b04c208c,'Mushrooms',1,'2020-10-04 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (b18b3932-a4ef-485c-a182-8e67b04c208c,'Mushrooms',0,'2020-10-05 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (b18b3932-a4ef-485c-a182-8e67b04c208c,'Mushrooms',2,'2020-10-06 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (b18b3932-a4ef-485c-a182-8e67b04c208c,'Mushrooms',0,'2020-10-07 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (b18b3932-a4ef-485c-a182-8e67b04c208c,'Mushrooms',0,'2020-10-08 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (b18b3932-a4ef-485c-a182-8e67b04c208c,'Olives',2,'2020-10-01 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (b18b3932-a4ef-485c-a182-8e67b04c208c,'Olives',1,'2020-10-02 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (b18b3932-a4ef-485c-a182-8e67b04c208c,'Olives',3,'2020-10-03 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (b18b3932-a4ef-485c-a182-8e67b04c208c,'Olives',2,'2020-10-04 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (b18b3932-a4ef-485c-a182-8e67b04c208c,'Olives',1,'2020-10-05 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (b18b3932-a4ef-485c-a182-8e67b04c208c,'Olives',2,'2020-10-06 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (b18b3932-a4ef-485c-a182-8e67b04c208c,'Olives',2,'2020-10-07 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (b18b3932-a4ef-485c-a182-8e67b04c208c,'Olives',0,'2020-10-08 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (b18b3932-a4ef-485c-a182-8e67b04c208c,'Onion',2,'2020-10-01 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (b18b3932-a4ef-485c-a182-8e67b04c208c,'Onion',1,'2020-10-02 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (b18b3932-a4ef-485c-a182-8e67b04c208c,'Onion',2,'2020-10-03 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (b18b3932-a4ef-485c-a182-8e67b04c208c,'Onion',2,'2020-10-04 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (b18b3932-a4ef-485c-a182-8e67b04c208c,'Onion',1,'2020-10-05 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (b18b3932-a4ef-485c-a182-8e67b04c208c,'Onion',2,'2020-10-06 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (b18b3932-a4ef-485c-a182-8e67b04c208c,'Onion',0,'2020-10-07 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (b18b3932-a4ef-485c-a182-8e67b04c208c,'Onion',0,'2020-10-08 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (b18b3932-a4ef-485c-a182-8e67b04c208c,'Pepperoni',1,'2020-10-01 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (b18b3932-a4ef-485c-a182-8e67b04c208c,'Pepperoni',1,'2020-10-02 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (b18b3932-a4ef-485c-a182-8e67b04c208c,'Pepperoni',2,'2020-10-03 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (b18b3932-a4ef-485c-a182-8e67b04c208c,'Pepperoni',1,'2020-10-04 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (b18b3932-a4ef-485c-a182-8e67b04c208c,'Pepperoni',2,'2020-10-05 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (b18b3932-a4ef-485c-a182-8e67b04c208c,'Pepperoni',2,'2020-10-06 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (b18b3932-a4ef-485c-a182-8e67b04c208c,'Pepperoni',1,'2020-10-07 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (b18b3932-a4ef-485c-a182-8e67b04c208c,'Pepperoni',2,'2020-10-08 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (b18b3932-a4ef-485c-a182-8e67b04c208c,'Peppers',2,'2020-10-01 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (b18b3932-a4ef-485c-a182-8e67b04c208c,'Peppers',1,'2020-10-02 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (b18b3932-a4ef-485c-a182-8e67b04c208c,'Peppers',2,'2020-10-03 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (b18b3932-a4ef-485c-a182-8e67b04c208c,'Peppers',3,'2020-10-04 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (b18b3932-a4ef-485c-a182-8e67b04c208c,'Peppers',1,'2020-10-05 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (b18b3932-a4ef-485c-a182-8e67b04c208c,'Peppers',2,'2020-10-06 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (b18b3932-a4ef-485c-a182-8e67b04c208c,'Peppers',0,'2020-10-07 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (b18b3932-a4ef-485c-a182-8e67b04c208c,'Peppers',0,'2020-10-08 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (b18b3932-a4ef-485c-a182-8e67b04c208c,'Pineapple',4,'2020-10-01 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (b18b3932-a4ef-485c-a182-8e67b04c208c,'Pineapple',1,'2020-10-02 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (b18b3932-a4ef-485c-a182-8e67b04c208c,'Pineapple',3,'2020-10-03 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (b18b3932-a4ef-485c-a182-8e67b04c208c,'Pineapple',1,'2020-10-04 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (b18b3932-a4ef-485c-a182-8e67b04c208c,'Pineapple',1,'2020-10-05 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (b18b3932-a4ef-485c-a182-8e67b04c208c,'Pineapple',2,'2020-10-06 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (b18b3932-a4ef-485c-a182-8e67b04c208c,'Pineapple',2,'2020-10-07 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (b18b3932-a4ef-485c-a182-8e67b04c208c,'Pineapple',0,'2020-10-08 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (b18b3932-a4ef-485c-a182-8e67b04c208c,'Sausage',1,'2020-10-01 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (b18b3932-a4ef-485c-a182-8e67b04c208c,'Sausage',0,'2020-10-02 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (b18b3932-a4ef-485c-a182-8e67b04c208c,'Sausage',2,'2020-10-03 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (b18b3932-a4ef-485c-a182-8e67b04c208c,'Sausage',1,'2020-10-04 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (b18b3932-a4ef-485c-a182-8e67b04c208c,'Sausage',1,'2020-10-05 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (b18b3932-a4ef-485c-a182-8e67b04c208c,'Sausage',2,'2020-10-06 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (b18b3932-a4ef-485c-a182-8e67b04c208c,'Sausage',1,'2020-10-07 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (b18b3932-a4ef-485c-a182-8e67b04c208c,'Sausage',0,'2020-10-08 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (b18b3932-a4ef-485c-a182-8e67b04c208c,'SpicySauce',1,'2020-10-01 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (b18b3932-a4ef-485c-a182-8e67b04c208c,'SpicySauce',3,'2020-10-02 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (b18b3932-a4ef-485c-a182-8e67b04c208c,'SpicySauce',1,'2020-10-03 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (b18b3932-a4ef-485c-a182-8e67b04c208c,'SpicySauce',3,'2020-10-04 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (b18b3932-a4ef-485c-a182-8e67b04c208c,'SpicySauce',3,'2020-10-05 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (b18b3932-a4ef-485c-a182-8e67b04c208c,'SpicySauce',2,'2020-10-06 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (b18b3932-a4ef-485c-a182-8e67b04c208c,'SpicySauce',1,'2020-10-07 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (b18b3932-a4ef-485c-a182-8e67b04c208c,'SpicySauce',1,'2020-10-08 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (b18b3932-a4ef-485c-a182-8e67b04c208c,'TraditionalSauce',3,'2020-10-01 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (b18b3932-a4ef-485c-a182-8e67b04c208c,'TraditionalSauce',2,'2020-10-02 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (b18b3932-a4ef-485c-a182-8e67b04c208c,'TraditionalSauce',3,'2020-10-03 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (b18b3932-a4ef-485c-a182-8e67b04c208c,'TraditionalSauce',1,'2020-10-04 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (b18b3932-a4ef-485c-a182-8e67b04c208c,'TraditionalSauce',3,'2020-10-05 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (b18b3932-a4ef-485c-a182-8e67b04c208c,'TraditionalSauce',3,'2020-10-06 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (b18b3932-a4ef-485c-a182-8e67b04c208c,'TraditionalSauce',3,'2020-10-07 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (b18b3932-a4ef-485c-a182-8e67b04c208c,'TraditionalSauce',1,'2020-10-08 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (5a2bb99f-88d2-4612-ac60-774aea9b8de4,'Bacon',4,'2020-10-01 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (5a2bb99f-88d2-4612-ac60-774aea9b8de4,'Bacon',1,'2020-10-02 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (5a2bb99f-88d2-4612-ac60-774aea9b8de4,'Bacon',1,'2020-10-03 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (5a2bb99f-88d2-4612-ac60-774aea9b8de4,'Bacon',3,'2020-10-04 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (5a2bb99f-88d2-4612-ac60-774aea9b8de4,'Bacon',0,'2020-10-05 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (5a2bb99f-88d2-4612-ac60-774aea9b8de4,'Bacon',1,'2020-10-06 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (5a2bb99f-88d2-4612-ac60-774aea9b8de4,'Bacon',1,'2020-10-07 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (5a2bb99f-88d2-4612-ac60-774aea9b8de4,'Bacon',3,'2020-10-08 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (5a2bb99f-88d2-4612-ac60-774aea9b8de4,'Beef',4,'2020-10-01 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (5a2bb99f-88d2-4612-ac60-774aea9b8de4,'Beef',1,'2020-10-02 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (5a2bb99f-88d2-4612-ac60-774aea9b8de4,'Beef',1,'2020-10-03 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (5a2bb99f-88d2-4612-ac60-774aea9b8de4,'Beef',1,'2020-10-04 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (5a2bb99f-88d2-4612-ac60-774aea9b8de4,'Beef',0,'2020-10-05 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (5a2bb99f-88d2-4612-ac60-774aea9b8de4,'Beef',1,'2020-10-06 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (5a2bb99f-88d2-4612-ac60-774aea9b8de4,'Beef',1,'2020-10-07 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (5a2bb99f-88d2-4612-ac60-774aea9b8de4,'Beef',7,'2020-10-08 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (5a2bb99f-88d2-4612-ac60-774aea9b8de4,'Cheese',8,'2020-10-01 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (5a2bb99f-88d2-4612-ac60-774aea9b8de4,'Cheese',4,'2020-10-02 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (5a2bb99f-88d2-4612-ac60-774aea9b8de4,'Cheese',3,'2020-10-03 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (5a2bb99f-88d2-4612-ac60-774aea9b8de4,'Cheese',6,'2020-10-04 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (5a2bb99f-88d2-4612-ac60-774aea9b8de4,'Cheese',3,'2020-10-05 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (5a2bb99f-88d2-4612-ac60-774aea9b8de4,'Cheese',4,'2020-10-06 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (5a2bb99f-88d2-4612-ac60-774aea9b8de4,'Cheese',2,'2020-10-07 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (5a2bb99f-88d2-4612-ac60-774aea9b8de4,'Cheese',12,'2020-10-08 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (5a2bb99f-88d2-4612-ac60-774aea9b8de4,'Chicken',3,'2020-10-01 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (5a2bb99f-88d2-4612-ac60-774aea9b8de4,'Chicken',1,'2020-10-02 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (5a2bb99f-88d2-4612-ac60-774aea9b8de4,'Chicken',1,'2020-10-03 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (5a2bb99f-88d2-4612-ac60-774aea9b8de4,'Chicken',2,'2020-10-04 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (5a2bb99f-88d2-4612-ac60-774aea9b8de4,'Chicken',1,'2020-10-05 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (5a2bb99f-88d2-4612-ac60-774aea9b8de4,'Chicken',2,'2020-10-06 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (5a2bb99f-88d2-4612-ac60-774aea9b8de4,'Chicken',1,'2020-10-07 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (5a2bb99f-88d2-4612-ac60-774aea9b8de4,'Chicken',5,'2020-10-08 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (5a2bb99f-88d2-4612-ac60-774aea9b8de4,'Dough',7,'2020-10-01 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (5a2bb99f-88d2-4612-ac60-774aea9b8de4,'Dough',4,'2020-10-02 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (5a2bb99f-88d2-4612-ac60-774aea9b8de4,'Dough',6,'2020-10-03 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (5a2bb99f-88d2-4612-ac60-774aea9b8de4,'Dough',6,'2020-10-04 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (5a2bb99f-88d2-4612-ac60-774aea9b8de4,'Dough',2,'2020-10-05 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (5a2bb99f-88d2-4612-ac60-774aea9b8de4,'Dough',4,'2020-10-06 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (5a2bb99f-88d2-4612-ac60-774aea9b8de4,'Dough',5,'2020-10-07 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (5a2bb99f-88d2-4612-ac60-774aea9b8de4,'Dough',12,'2020-10-08 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (5a2bb99f-88d2-4612-ac60-774aea9b8de4,'Mushrooms',3,'2020-10-01 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (5a2bb99f-88d2-4612-ac60-774aea9b8de4,'Mushrooms',1,'2020-10-02 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (5a2bb99f-88d2-4612-ac60-774aea9b8de4,'Mushrooms',0,'2020-10-03 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (5a2bb99f-88d2-4612-ac60-774aea9b8de4,'Mushrooms',2,'2020-10-04 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (5a2bb99f-88d2-4612-ac60-774aea9b8de4,'Mushrooms',1,'2020-10-05 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (5a2bb99f-88d2-4612-ac60-774aea9b8de4,'Mushrooms',1,'2020-10-06 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (5a2bb99f-88d2-4612-ac60-774aea9b8de4,'Mushrooms',1,'2020-10-07 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (5a2bb99f-88d2-4612-ac60-774aea9b8de4,'Mushrooms',4,'2020-10-08 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (5a2bb99f-88d2-4612-ac60-774aea9b8de4,'Olives',4,'2020-10-01 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (5a2bb99f-88d2-4612-ac60-774aea9b8de4,'Olives',0,'2020-10-02 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (5a2bb99f-88d2-4612-ac60-774aea9b8de4,'Olives',1,'2020-10-03 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (5a2bb99f-88d2-4612-ac60-774aea9b8de4,'Olives',1,'2020-10-04 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (5a2bb99f-88d2-4612-ac60-774aea9b8de4,'Olives',1,'2020-10-05 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (5a2bb99f-88d2-4612-ac60-774aea9b8de4,'Olives',1,'2020-10-06 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (5a2bb99f-88d2-4612-ac60-774aea9b8de4,'Olives',1,'2020-10-07 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (5a2bb99f-88d2-4612-ac60-774aea9b8de4,'Olives',5,'2020-10-08 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (5a2bb99f-88d2-4612-ac60-774aea9b8de4,'Onion',4,'2020-10-01 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (5a2bb99f-88d2-4612-ac60-774aea9b8de4,'Onion',0,'2020-10-02 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (5a2bb99f-88d2-4612-ac60-774aea9b8de4,'Onion',1,'2020-10-03 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (5a2bb99f-88d2-4612-ac60-774aea9b8de4,'Onion',3,'2020-10-04 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (5a2bb99f-88d2-4612-ac60-774aea9b8de4,'Onion',1,'2020-10-05 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (5a2bb99f-88d2-4612-ac60-774aea9b8de4,'Onion',2,'2020-10-06 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (5a2bb99f-88d2-4612-ac60-774aea9b8de4,'Onion',1,'2020-10-07 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (5a2bb99f-88d2-4612-ac60-774aea9b8de4,'Onion',3,'2020-10-08 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (5a2bb99f-88d2-4612-ac60-774aea9b8de4,'Pepperoni',3,'2020-10-01 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (5a2bb99f-88d2-4612-ac60-774aea9b8de4,'Pepperoni',1,'2020-10-02 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (5a2bb99f-88d2-4612-ac60-774aea9b8de4,'Pepperoni',1,'2020-10-03 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (5a2bb99f-88d2-4612-ac60-774aea9b8de4,'Pepperoni',3,'2020-10-04 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (5a2bb99f-88d2-4612-ac60-774aea9b8de4,'Pepperoni',1,'2020-10-05 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (5a2bb99f-88d2-4612-ac60-774aea9b8de4,'Pepperoni',1,'2020-10-06 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (5a2bb99f-88d2-4612-ac60-774aea9b8de4,'Pepperoni',1,'2020-10-07 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (5a2bb99f-88d2-4612-ac60-774aea9b8de4,'Pepperoni',2,'2020-10-08 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (5a2bb99f-88d2-4612-ac60-774aea9b8de4,'Peppers',3,'2020-10-01 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (5a2bb99f-88d2-4612-ac60-774aea9b8de4,'Peppers',1,'2020-10-02 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (5a2bb99f-88d2-4612-ac60-774aea9b8de4,'Peppers',0,'2020-10-03 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (5a2bb99f-88d2-4612-ac60-774aea9b8de4,'Peppers',3,'2020-10-04 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (5a2bb99f-88d2-4612-ac60-774aea9b8de4,'Peppers',1,'2020-10-05 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (5a2bb99f-88d2-4612-ac60-774aea9b8de4,'Peppers',0,'2020-10-06 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (5a2bb99f-88d2-4612-ac60-774aea9b8de4,'Peppers',1,'2020-10-07 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (5a2bb99f-88d2-4612-ac60-774aea9b8de4,'Peppers',2,'2020-10-08 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (5a2bb99f-88d2-4612-ac60-774aea9b8de4,'Pineapple',4,'2020-10-01 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (5a2bb99f-88d2-4612-ac60-774aea9b8de4,'Pineapple',1,'2020-10-02 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (5a2bb99f-88d2-4612-ac60-774aea9b8de4,'Pineapple',1,'2020-10-03 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (5a2bb99f-88d2-4612-ac60-774aea9b8de4,'Pineapple',3,'2020-10-04 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (5a2bb99f-88d2-4612-ac60-774aea9b8de4,'Pineapple',1,'2020-10-05 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (5a2bb99f-88d2-4612-ac60-774aea9b8de4,'Pineapple',0,'2020-10-06 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (5a2bb99f-88d2-4612-ac60-774aea9b8de4,'Pineapple',0,'2020-10-07 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (5a2bb99f-88d2-4612-ac60-774aea9b8de4,'Pineapple',4,'2020-10-08 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (5a2bb99f-88d2-4612-ac60-774aea9b8de4,'Sausage',3,'2020-10-01 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (5a2bb99f-88d2-4612-ac60-774aea9b8de4,'Sausage',0,'2020-10-02 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (5a2bb99f-88d2-4612-ac60-774aea9b8de4,'Sausage',1,'2020-10-03 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (5a2bb99f-88d2-4612-ac60-774aea9b8de4,'Sausage',4,'2020-10-04 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (5a2bb99f-88d2-4612-ac60-774aea9b8de4,'Sausage',1,'2020-10-05 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (5a2bb99f-88d2-4612-ac60-774aea9b8de4,'Sausage',1,'2020-10-06 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (5a2bb99f-88d2-4612-ac60-774aea9b8de4,'Sausage',0,'2020-10-07 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (5a2bb99f-88d2-4612-ac60-774aea9b8de4,'Sausage',5,'2020-10-08 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (5a2bb99f-88d2-4612-ac60-774aea9b8de4,'SpicySauce',2,'2020-10-01 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (5a2bb99f-88d2-4612-ac60-774aea9b8de4,'SpicySauce',1,'2020-10-02 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (5a2bb99f-88d2-4612-ac60-774aea9b8de4,'SpicySauce',4,'2020-10-03 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (5a2bb99f-88d2-4612-ac60-774aea9b8de4,'SpicySauce',0,'2020-10-04 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (5a2bb99f-88d2-4612-ac60-774aea9b8de4,'SpicySauce',2,'2020-10-05 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (5a2bb99f-88d2-4612-ac60-774aea9b8de4,'SpicySauce',3,'2020-10-06 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (5a2bb99f-88d2-4612-ac60-774aea9b8de4,'SpicySauce',2,'2020-10-07 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (5a2bb99f-88d2-4612-ac60-774aea9b8de4,'SpicySauce',5,'2020-10-08 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (5a2bb99f-88d2-4612-ac60-774aea9b8de4,'TraditionalSauce',3,'2020-10-01 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (5a2bb99f-88d2-4612-ac60-774aea9b8de4,'TraditionalSauce',1,'2020-10-02 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (5a2bb99f-88d2-4612-ac60-774aea9b8de4,'TraditionalSauce',0,'2020-10-03 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (5a2bb99f-88d2-4612-ac60-774aea9b8de4,'TraditionalSauce',4,'2020-10-04 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (5a2bb99f-88d2-4612-ac60-774aea9b8de4,'TraditionalSauce',0,'2020-10-05 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (5a2bb99f-88d2-4612-ac60-774aea9b8de4,'TraditionalSauce',0,'2020-10-06 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (5a2bb99f-88d2-4612-ac60-774aea9b8de4,'TraditionalSauce',1,'2020-10-07 00:00:00.000+0000');
INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (5a2bb99f-88d2-4612-ac60-774aea9b8de4,'TraditionalSauce',2,'2020-10-08 00:00:00.000+0000');


CREATE TABLE orderByCustomer (
  orderedBy TEXT,
  placedAT TIMESTAMP,
  orderID UUID,
  PRIMARY KEY (orderedBy, placedAt)
);

INSERT INTO orderByCustomer (orderedBy, placedAT, orderID) VALUES ('Daniel Miller','2020-10-09 16:09:04.684+0000',fe741c7e-963c-47cd-85fc-3436bd02da82);
INSERT INTO orderByCustomer (orderedBy, placedAT, orderID) VALUES ('Brooke Bush','2020-10-09 16:13:04.690+0000',1d78ec54-5137-4373-b96f-0fbc54eb4b12);
INSERT INTO orderByCustomer (orderedBy, placedAT, orderID) VALUES ('Joseph Reed','2020-10-09 16:08:04.577+0000',806677d4-34f8-45d8-96b1-4b52b01eb714);
INSERT INTO orderByCustomer (orderedBy, placedAT, orderID) VALUES ('Jennifer Martin','2020-10-09 16:11:05.030+0000',9e27952a-cee7-449a-b8e1-26ae2728b1d0);
INSERT INTO orderByCustomer (orderedBy, placedAT, orderID) VALUES ('Emily Hudson','2020-10-09 16:10:04.555+0000',432da2bb-6486-4749-987c-70c2b5ba7f1a);
INSERT INTO orderByCustomer (orderedBy, placedAT, orderID) VALUES ('Terry Barnes MD','2020-10-09 16:06:57.398+0000',471767a2-f07b-4f1e-8c35-752f3564670d);
INSERT INTO orderByCustomer (orderedBy, placedAT, orderID) VALUES ('Amanda Webb','2020-10-09 16:08:04.480+0000',738cbccb-084f-46f1-9bee-b44add451fe2);
INSERT INTO orderByCustomer (orderedBy, placedAT, orderID) VALUES ('Mary Mullen','2020-10-09 16:11:05.161+0000',f7eb68a7-3a3f-44b7-9653-7b46922bd7a0);
INSERT INTO orderByCustomer (orderedBy, placedAT, orderID) VALUES ('Jack Collins','2020-10-09 16:12:04.532+0000',f611d989-f120-4010-b92c-df393b13a5a0);
INSERT INTO orderByCustomer (orderedBy, placedAT, orderID) VALUES ('Benjamin Frye','2020-10-09 16:11:04.770+0000',f682d32f-4e11-4394-a4a3-c0eb0880a14b);
INSERT INTO orderByCustomer (orderedBy, placedAT, orderID) VALUES ('Jonathan Perry','2020-10-09 16:12:04.663+0000',19c9de5c-4293-4e2f-9280-a58ca7ec80ce);
INSERT INTO orderByCustomer (orderedBy, placedAT, orderID) VALUES ('Luke Meyer','2020-10-09 16:09:04.641+0000',e7c3873a-4828-4c82-b8b6-803dda9567fe);
INSERT INTO orderByCustomer (orderedBy, placedAT, orderID) VALUES ('Joseph Johnson','2020-10-09 16:10:04.640+0000',3023d9d3-e0e5-4692-8570-40432c4a6005);
INSERT INTO orderByCustomer (orderedBy, placedAT, orderID) VALUES ('Grant Vega','2020-10-09 16:13:04.781+0000',6d8c1311-55fd-4c2c-b84b-7265c5fbc8b6);
INSERT INTO orderByCustomer (orderedBy, placedAT, orderID) VALUES ('Nathan Waters','2020-10-09 16:13:04.823+0000',2a4541e9-c33f-4605-a736-19cec3c07011);
INSERT INTO orderByCustomer (orderedBy, placedAT, orderID) VALUES ('Alexandra Small','2020-10-09 16:12:04.616+0000',601ca3ab-c72f-452d-901f-112d75a6d8b9);
INSERT INTO orderByCustomer (orderedBy, placedAT, orderID) VALUES ('Anthony Miller','2020-10-09 16:14:04.869+0000',8e5e5918-ef09-4616-b72f-1546ade4f94b);
INSERT INTO orderByCustomer (orderedBy, placedAT, orderID) VALUES ('Morgan Thompson','2020-10-09 16:14:04.738+0000',b07fc505-3569-4d51-a3b5-59bd2f29c340);
INSERT INTO orderByCustomer (orderedBy, placedAT, orderID) VALUES ('Scott Flores','2020-10-09 16:09:04.958+0000',f0a203d4-e324-405b-aff0-d05478add4bd);
INSERT INTO orderByCustomer (orderedBy, placedAT, orderID) VALUES ('Eugene Barr','2020-10-09 16:13:04.906+0000',1774e9ac-885f-4154-a4c0-f181765f490d);
INSERT INTO orderByCustomer (orderedBy, placedAT, orderID) VALUES ('Amanda Allen','2020-10-09 16:13:04.945+0000',1e8b03b3-0514-4e3c-bb19-b4701582b252);
INSERT INTO orderByCustomer (orderedBy, placedAT, orderID) VALUES ('Hunter Kim','2020-10-09 16:13:04.864+0000',ffbe3fe5-3987-4225-a2c6-471423adfef5);
INSERT INTO orderByCustomer (orderedBy, placedAT, orderID) VALUES ('Ashley Smith','2020-10-09 16:12:04.842+0000',3c4622eb-d936-454d-8f97-2211ce03ba3a);
INSERT INTO orderByCustomer (orderedBy, placedAT, orderID) VALUES ('Mary Weaver','2020-10-09 16:14:04.782+0000',1436c6a7-b4c6-420a-8edf-38bc08db3739);
INSERT INTO orderByCustomer (orderedBy, placedAT, orderID) VALUES ('Michael Smith','2020-10-09 16:09:04.778+0000',44f789d6-4ebb-421b-9c54-ed4bc363d360);
INSERT INTO orderByCustomer (orderedBy, placedAT, orderID) VALUES ('Lucas Cole','2020-10-09 16:08:04.832+0000',9d677262-9759-46a0-9be2-4d2e6fcfe173);
INSERT INTO orderByCustomer (orderedBy, placedAT, orderID) VALUES ('Angela Green','2020-10-09 16:11:04.812+0000',d3e3b1cb-6edb-410d-bd37-42ec214d1358);
INSERT INTO orderByCustomer (orderedBy, placedAT, orderID) VALUES ('Jessica Thomas DVM','2020-10-09 16:13:04.733+0000',4792ffeb-2259-44a2-b35d-31bf2df38b95);
INSERT INTO orderByCustomer (orderedBy, placedAT, orderID) VALUES ('Sarah Henderson','2020-10-09 16:09:04.863+0000',ca45ff1f-5633-4ab6-a1bb-76dfe53c65c5);
INSERT INTO orderByCustomer (orderedBy, placedAT, orderID) VALUES ('Jeffery Stanton','2020-10-09 16:10:04.904+0000',ada9cbf0-8d1f-4925-b015-9fa2d1a42bed);
INSERT INTO orderByCustomer (orderedBy, placedAT, orderID) VALUES ('Maurice Reid','2020-10-09 16:11:05.117+0000',366f46bc-5ffe-4e3e-960b-e8bd2557a26c);
INSERT INTO orderByCustomer (orderedBy, placedAT, orderID) VALUES ('Eric Douglas','2020-10-09 16:06:57.132+0000',2e1c6b7a-7757-4ede-8b0e-a3f5a07a263a);
INSERT INTO orderByCustomer (orderedBy, placedAT, orderID) VALUES ('Amanda Mccullough','2020-10-09 16:06:57.012+0000',2dbab543-bb2d-4766-8c91-439f5688b2f1);
INSERT INTO orderByCustomer (orderedBy, placedAT, orderID) VALUES ('Amy Medina','2020-10-09 16:09:05.020+0000',7a8c0c2b-f337-4ba7-9f6c-9fb7e63fa259);
INSERT INTO orderByCustomer (orderedBy, placedAT, orderID) VALUES ('Chelsea Garrett','2020-10-09 16:13:05.030+0000',0a6dfe17-3ef7-4922-86d6-7771cd852834);
INSERT INTO orderByCustomer (orderedBy, placedAT, orderID) VALUES ('Joseph Hawkins','2020-10-09 16:09:04.727+0000',ce6e1eec-e949-40d6-95a2-72b197b50a35);
INSERT INTO orderByCustomer (orderedBy, placedAT, orderID) VALUES ('Tyler Turner','2020-10-09 16:12:04.574+0000',c79fac0e-a231-48f0-92b8-7bdd65c6f752);
INSERT INTO orderByCustomer (orderedBy, placedAT, orderID) VALUES ('Scott Hogan','2020-10-09 16:06:57.241+0000',bd592e06-a030-4dc5-948a-4b6cdd8a653c);
INSERT INTO orderByCustomer (orderedBy, placedAT, orderID) VALUES ('Ronald Cline','2020-10-09 16:10:04.858+0000',2067a957-6cb3-4e31-b571-5a3b77045efe);
INSERT INTO orderByCustomer (orderedBy, placedAT, orderID) VALUES ('Brian Moon','2020-10-09 16:14:04.532+0000',6f461e2a-c67d-4c74-b786-76cc642e2aad);
INSERT INTO orderByCustomer (orderedBy, placedAT, orderID) VALUES ('Sandra Marshall','2020-10-09 16:06:56.956+0000',373da967-c790-454e-a978-b5a46ec344e9);
INSERT INTO orderByCustomer (orderedBy, placedAT, orderID) VALUES ('Christopher Soto','2020-10-09 16:08:04.876+0000',e8debfe5-9f74-4d26-88f4-e06473f857cf);
INSERT INTO orderByCustomer (orderedBy, placedAT, orderID) VALUES ('Gwendolyn Mclaughlin','2020-10-09 16:14:04.826+0000',d75616c9-2a4b-4a31-a0fe-5b08855ecb70);
INSERT INTO orderByCustomer (orderedBy, placedAT, orderID) VALUES ('Emily Wolfe','2020-10-09 16:10:04.813+0000',385364d4-add9-4ac8-8ca6-0a8d78d5040f);
INSERT INTO orderByCustomer (orderedBy, placedAT, orderID) VALUES ('Debra Andrews','2020-10-09 16:09:04.821+0000',a14787b7-2fd0-46eb-b670-aa92f6a96ead);
INSERT INTO orderByCustomer (orderedBy, placedAT, orderID) VALUES ('Taylor Stone','2020-10-09 16:10:04.731+0000',cf64acf4-a663-4926-9a05-74c60daf7768);
INSERT INTO orderByCustomer (orderedBy, placedAT, orderID) VALUES ('Joshua Stafford','2020-10-09 16:06:56.896+0000',b93e8a4a-a9c7-4553-a7b2-f05475569d36);
INSERT INTO orderByCustomer (orderedBy, placedAT, orderID) VALUES ('Tracy Henderson','2020-10-09 16:08:04.787+0000',ff01189b-3ae9-4ff2-a2bc-4cdff699454f);
INSERT INTO orderByCustomer (orderedBy, placedAT, orderID) VALUES ('Linda Jensen','2020-10-09 16:11:05.077+0000',12f63894-844b-4372-8857-32c1c416de77);
INSERT INTO orderByCustomer (orderedBy, placedAT, orderID) VALUES ('Karen Franco','2020-10-09 16:14:04.574+0000',c345f4fa-5ab3-4314-96cb-a5b08153e7ea);
INSERT INTO orderByCustomer (orderedBy, placedAT, orderID) VALUES ('Jennifer Wilkinson','2020-10-09 16:08:04.532+0000',c6a0e33e-c55a-413d-bfb9-83cfc1aa5c83);
INSERT INTO orderByCustomer (orderedBy, placedAT, orderID) VALUES ('Kurt Arnold','2020-10-09 16:11:04.984+0000',7e723ea6-cbba-4b3d-91b1-6729a18e8ac0);
INSERT INTO orderByCustomer (orderedBy, placedAT, orderID) VALUES ('Brittany Turner','2020-10-09 16:10:04.771+0000',5ee27389-403f-42a3-af18-4d32c04b3b3a);
INSERT INTO orderByCustomer (orderedBy, placedAT, orderID) VALUES ('Denise Nelson','2020-10-09 16:12:04.750+0000',b6b52ffd-c527-420f-b87e-01d1d10e211e);
INSERT INTO orderByCustomer (orderedBy, placedAT, orderID) VALUES ('Alyssa Perez','2020-10-09 16:11:04.943+0000',dceaebcf-d084-4489-a9d4-a32868a07dc8);
INSERT INTO orderByCustomer (orderedBy, placedAT, orderID) VALUES ('Jill Munoz','2020-10-09 16:06:57.294+0000',84994022-041d-4d95-a752-79c2f09d651a);
INSERT INTO orderByCustomer (orderedBy, placedAT, orderID) VALUES ('Isabel Reed','2020-10-09 16:09:04.904+0000',b7372bf2-572c-491e-9014-7c04b14e6714);
INSERT INTO orderByCustomer (orderedBy, placedAT, orderID) VALUES ('Cody Harrison','2020-10-09 16:08:04.632+0000',416f06dc-cf3e-4258-9e3d-cd456c655bb6);
INSERT INTO orderByCustomer (orderedBy, placedAT, orderID) VALUES ('Kimberly Branch','2020-10-09 16:13:04.986+0000',8f373e5e-4cad-4f5c-90f7-273f7ff8da4b);
INSERT INTO orderByCustomer (orderedBy, placedAT, orderID) VALUES ('Daniel Moore','2020-10-09 16:12:04.710+0000',f46c3113-8afe-42f9-bbce-c86566b4bcef);
INSERT INTO orderByCustomer (orderedBy, placedAT, orderID) VALUES ('Jacob Garcia','2020-10-09 16:11:04.855+0000',6e330978-3bc9-4793-a179-ed47a5f55f55);
INSERT INTO orderByCustomer (orderedBy, placedAT, orderID) VALUES ('Timothy Smith','2020-10-09 16:14:04.658+0000',f02752a4-398d-4914-918f-88a35e23513a);
INSERT INTO orderByCustomer (orderedBy, placedAT, orderID) VALUES ('Jacqueline Copeland MD','2020-10-09 16:06:57.347+0000',ad75ba81-4a5c-44a7-a0f3-2d6f4b4b4958);
INSERT INTO orderByCustomer (orderedBy, placedAT, orderID) VALUES ('Lisa Bolton','2020-10-09 16:10:04.498+0000',ec85a551-f506-4957-bb00-dac1a954a01e);
INSERT INTO orderByCustomer (orderedBy, placedAT, orderID) VALUES ('Cassidy Stewart','2020-10-09 16:08:04.681+0000',9e3c3466-e9d3-49bd-81ba-d9edde2f162d);
INSERT INTO orderByCustomer (orderedBy, placedAT, orderID) VALUES ('Joseph Nichols','2020-10-09 16:09:04.592+0000',543623f9-49cb-444e-b9d2-1604a4ee0cd5);
INSERT INTO orderByCustomer (orderedBy, placedAT, orderID) VALUES ('Daniel Dixon','2020-10-09 16:14:04.698+0000',21dec7fa-c2c7-4c55-abd9-570f7dcd6c0c);
INSERT INTO orderByCustomer (orderedBy, placedAT, orderID) VALUES ('David Nelson','2020-10-09 16:12:04.449+0000',34a795fe-ca6d-4758-b21f-9e64fdd56e60);
INSERT INTO orderByCustomer (orderedBy, placedAT, orderID) VALUES ('Jesse Perry','2020-10-09 16:10:04.684+0000',2e48854a-c59d-4171-8a25-563c01efb7d4);
INSERT INTO orderByCustomer (orderedBy, placedAT, orderID) VALUES ('Tricia Davenport','2020-10-09 16:13:05.072+0000',4e3a990d-e67d-4ecc-9f12-6e8c01e0af87);
INSERT INTO orderByCustomer (orderedBy, placedAT, orderID) VALUES ('Sarah Smith','2020-10-09 16:14:04.619+0000',d2bbdb30-3e2f-4f42-992c-fd38d872acc1);
INSERT INTO orderByCustomer (orderedBy, placedAT, orderID) VALUES ('Jessica Christensen','2020-10-09 16:08:04.923+0000',d78c51ed-41ab-4716-afb2-fdb9673851d8);
INSERT INTO orderByCustomer (orderedBy, placedAT, orderID) VALUES ('Nathan Reeves','2020-10-09 16:14:04.911+0000',8434d2be-49d5-4c72-af24-981f04e3c196);
INSERT INTO orderByCustomer (orderedBy, placedAT, orderID) VALUES ('David Lara','2020-10-09 16:10:04.598+0000',0abbc8d6-23f0-4696-930f-30b6e5d09857);
INSERT INTO orderByCustomer (orderedBy, placedAT, orderID) VALUES ('Melissa Jones','2020-10-09 16:06:57.075+0000',4fcfa2de-ba46-4d2f-a2f4-13a721722573);
INSERT INTO orderByCustomer (orderedBy, placedAT, orderID) VALUES ('Margaret Hunter','2020-10-09 16:11:04.898+0000',24408218-0e26-4089-8ef6-a39ec804e2e5);
INSERT INTO orderByCustomer (orderedBy, placedAT, orderID) VALUES ('Desiree Rush','2020-10-09 16:12:04.490+0000',568258b2-3510-474d-ac5b-6180340bd4dc);
INSERT INTO orderByCustomer (orderedBy, placedAT, orderID) VALUES ('Steven Newman','2020-10-09 16:12:04.798+0000',f59ecde2-0208-40fc-a48f-c1181bb1c7fb);
INSERT INTO orderByCustomer (orderedBy, placedAT, orderID) VALUES ('Jacqueline Todd','2020-10-09 16:06:57.188+0000',27aa345c-dc96-4099-9599-93824940d1e9);
INSERT INTO orderByCustomer (orderedBy, placedAT, orderID) VALUES ('Tracy Smith','2020-10-09 16:08:04.738+0000',966d2851-ec6b-4709-90fd-1cb51e6e99f3);