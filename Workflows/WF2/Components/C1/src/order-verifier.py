from flask import Flask, request, Response
from cassandra.cluster import Cluster
from datetime import date
from datetime import datetime
import jsonschema
import json
import logging
import time
import uuid
import os

# Connect to Cassandra service
cass_IP = os.environ["CASS_DB"]
cluster = Cluster([cass_IP])  #[cass_IP]
session = cluster.connect('pizza_grocery')

# Cassandra prepared statements
check_stock_prepared = session.prepare('SELECT * FROM stock WHERE storeID=?')
dec_stock_prepared = session.prepare('UPDATE stock SET quantity=? WHERE storeID=? AND itemName=?')
item_price_prepared = session.prepare('SELECT * FROM items WHERE name=?')
insert_cust_prepared = session.prepare('INSERT INTO customers (customerName, latitude, longitude) VALUES (?, ?, ?)')
insert_pay_prepared = session.prepare('INSERT INTO payments (paymentToken, method) VALUES (?, ?)')
insert_pizzas_prepared = session.prepare('INSERT INTO pizzas (pizzaID, toppings, cost) VALUES (?, ?, ?)')
insert_order_prepared = session.prepare('\
    INSERT INTO orderTable \
        (orderID, orderedFrom, orderedBy, deliveredBy, containsPizzas, containsItems, paymentID, placedAt, active, estimatedDeliveryTime) \
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)\
')
insert_order_by_store_prepared = session.prepare('INSERT INTO orderByStore (orderedFrom, placedAt, orderID) VALUES (?, ?, ?)')
insert_order_by_cust_prepared = session.prepare('INSERT INTO orderByCustomer (orderedBy, placedAt, orderID) VALUES (?, ?, ?)')
select_tracker_prepared = session.prepare('SELECT * FROM stockTracker WHERE storeID=? AND itemName=? AND dateSold=?')
insert_tracker_prepared = session.prepare('INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) VALUES (?, ?, ?, ?)')
update_tracker_prepared = session.prepare('UPDATE stockTracker SET quantitySold=? WHERE storeID=? AND itemName=? AND dateSold=?')

# Create Flask app
app = Flask(__name__)

# Open jsonschema for pizza orders
with open("src/pizza-order.schema.json", "r") as schema:
    schema = json.loads(schema.read())

# Logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Flag for stock_tracker_test() - dumby inserts for Randeep C4 testing
stock_tracker_test_flag = True


# Aggregate all ingredients for a given order
def aggregate_ingredients(pizza_list):
    ingredients = {
        'Dough': 0,         'SpicySauce': 0,        'TraditionalSauce': 0,  'Cheese': 0,
        'Pepperoni': 0,     'Sausage': 0,           'Beef': 0,              'Onion': 0,
        'Chicken': 0,       'Peppers': 0,           'Olives': 0,            'Bacon': 0,
        'Pineapple': 0,     'Mushrooms': 0
    }

    # Loop through each pizza in pizza_list and aggregate the required ingredients
    for pizza in pizza_list:
        if pizza['crustType'] == 'Thin':
            ingredients['Dough'] += 1
        elif pizza['crustType'] == 'Traditional':
            ingredients['Dough'] += 2

        if pizza['sauceType'] == 'Spicy':
            ingredients['SpicySauce'] += 1
        elif pizza['sauceType'] == 'Traditional':
            ingredients['TraditionalSauce'] += 1

        if pizza['cheeseAmt'] == 'Light':
            ingredients['Cheese'] += 1
        elif pizza['cheeseAmt'] == 'Normal':
            ingredients['Cheese'] += 2
        elif pizza['cheeseAmt'] == 'Extra':
            ingredients['Cheese'] += 3

        for topping in pizza["toppingList"]:
            ingredients[topping] += 1

    return ingredients


# Decrement a store's stock for the order about to be placed
def decrement_stock(store_id, in_stock_dict, req_item_dict):
    for item_name in req_item_dict:
        new_quantity = in_stock_dict[item_name] - req_item_dict[item_name]
        session.execute(dec_stock_prepared, (new_quantity, store_id, item_name))


# Calculate pizza price
def calc_pizza_cost(topping_set):
    # Note: topping_set also contains dough amount, sauce type, and cheese amount,
    # in addition to the toppings. Name was selected to be consistent with DB naming
    cost = 0.0
    for topping in topping_set:
        result = session.execute(item_price_prepared, (topping[0],))
        for (name, price) in result:
            cost += price * topping[1] 
    return cost


# Insert an order's pizza(s) into 'pizzas' table
def insert_pizzas(pizza_list):
    uuid_set = set()
    
    for pizza in pizza_list:
        pizza_uuid = uuid.uuid4()
        uuid_set.add(pizza_uuid)
        topping_set = set()

        if pizza["crustType"] == "Thin":
            topping_set.add(("Dough", 1))
        elif pizza["crustType"] == "Traditional":
            topping_set.add(("Dough", 2))

        if pizza["sauceType"] == "Spicy":
            topping_set.add(("SpicySauce", 1))
        elif pizza["sauceType"] == "Traditional":
            topping_set.add(("TraditionalSauce", 1))

        if pizza["cheeseAmt"] == "Light":
            topping_set.add(("Cheese", 1))
        elif pizza["cheeseAmt"] == "Normal":
            topping_set.add(("Cheese", 2))
        elif pizza["cheeseAmt"] == "Extra":
            topping_set.add(("Cheese", 2))

        for topping in pizza["toppingList"]:
            topping_set.add((topping, 1))
        
        cost = calc_pizza_cost(topping_set)
        session.execute(insert_pizzas_prepared, (pizza_uuid, topping_set, cost))
    
    return uuid_set


# TODO: Remove after Randeep's C4 testing
def stock_tracker_test():
    global stock_tracker_test_flag
    store_uuid = uuid.UUID("7098813e-4624-462a-81a1-7e0e4e67631d")
    for offset in range(5):
        date_sold = datetime.combine(datetime(2020, 10, (1 + offset)), datetime.min.time())
        quantity = 5 * offset + 10
        session.execute(insert_tracker_prepared, (store_uuid, "Dough", quantity, date_sold))
        logging.debug("C4 TESTING - StoreID 7098813e-4624-462a-81a1-7e0e4e67631d: itemName = Dough, Quantity = " + str(quantity))
    stock_tracker_test_flag = False


# Insert or update stockTracker table for items sold per day
def stock_tracker_mgr(store_uuid, req_item_dict):
    date_sold = datetime.combine(date.today(), datetime.min.time())
    for item_name in req_item_dict:
        rows = session.execute(select_tracker_prepared, (store_uuid, item_name, date_sold))
        if not rows:
            session.execute(insert_tracker_prepared, (store_uuid, item_name, req_item_dict[item_name], date_sold))
        else:
            for row in rows:
                quantity = row.quantitysold + req_item_dict[item_name]
                session.execute(update_tracker_prepared, (quantity, store_uuid, item_name, date_sold))


# Insert order info into DB
def insert_order(order_id, order_dict, req_item_dict):
    order_uuid = uuid.UUID(order_id)
    store_uuid = uuid.UUID(order_dict[order_id]["storeId"])
    pay_uuid = uuid.UUID(order_dict[order_id]["paymentToken"])
    cust_name = order_dict[order_id]["custName"]
    cust_lat = order_dict[order_id]["custLocation"]["lat"]
    cust_lon = order_dict[order_id]["custLocation"]["lon"]
    placed_at = datetime.now()

    # Insert customer information into 'customers' table
    session.execute(insert_cust_prepared, (cust_name, cust_lat, cust_lon))
    # Insert order payment information into 'payments' table
    session.execute(insert_pay_prepared, (pay_uuid, order_dict[order_id]["paymentTokenType"]))  
    # Insert the ordered pizzas into 'pizzas' table
    pizza_uuid_set = insert_pizzas(order_dict[order_id]["pizzaList"])
    # Insert order into 'orderTable' table
    session.execute(insert_order_prepared, 
        (order_uuid, store_uuid, cust_name, "", pizza_uuid_set, None, pay_uuid, placed_at, True, -1)
    )
    # Insert order into 'orderByStore' table
    session.execute(insert_order_by_store_prepared, (store_uuid, placed_at, order_uuid))
    # Insert order into 'orderByCustomer' table
    session.execute(insert_order_by_cust_prepared, (cust_name, placed_at, order_uuid))
    # Insert or update 'stockTracker' table
    stock_tracker_mgr(store_uuid, req_item_dict)
    # Only used for Randeep's C4 testing
    # TODO: Remove after Randeep has completed C4 testing
    if stock_tracker_test_flag:
        stock_tracker_test()


# Check stock at a given store to determine if order can be filled
def check_stock_then_insert(order_dict):
    in_stock = True
    in_stock_dict = {
        'Dough': 0,         'SpicySauce': 0,        'TraditionalSauce': 0,      'Cheese': 0,
        'Pepperoni': 0,     'Sausage': 0,           'Beef': 0,                  'Onion': 0,
        'Chicken': 0,       'Peppers': 0,           'Olives': 0,                'Bacon': 0,
        'Pineapple': 0,     'Mushrooms': 0
    }
    for order_id in order_dict:
        store_id = uuid.UUID(order_dict[order_id]["storeId"])
    req_item_dict = aggregate_ingredients(order_dict[order_id]["pizzaList"])
    restock_list = []

    # If the order cannot be filled, restock_list contains items for restock
    # Otherwise, restock_list is an empty list
    rows = session.execute(check_stock_prepared, (store_id,))
    for row in rows:
        if row.quantity < req_item_dict[row.itemname]:
            in_stock = False
            restock_list.append({"item-name": row.itemname, "quantity": req_item_dict[row.itemname]})
        else:
            in_stock_dict[row.itemname] = row.quantity

    # If no restock required, decrement stock and insert order into DB
    if in_stock:
        decrement_stock(store_id, in_stock_dict, req_item_dict)
        insert_order(order_id, order_dict, req_item_dict)

    return restock_list


# Manages order placement or restock, if needed
def order_manager(order_dict):
    # Validate order json against jsonschema
    global schema
    try:
        for order_id in order_dict:
            jsonschema.validate(instance=order_dict[order_id], schema=schema)
    except:
        return Response(status=400, response="Pizza order failed validation. Rejecting request.\n")

    # Check the stock to see if order can be placed
    restock_list = check_stock_then_insert(order_dict)
    order_json = json.dumps(order_dict)
    if not restock_list:    
        # If restock_list is empty, then the order was accepted
        logging.debug('Pizza order accepted: ' + order_json)
        return Response(status=200, response="Pizza order accepted: " + order_id)
    else:
        # Else, need to restock item(s) contained in restock_list.
        # Form restock_json with store_id and restock_list, then send it to WFM
        store_id = order_dict[order_id]["storeId"]
        restock_dict = {"storeID": store_id, "restock-list": restock_list}
        restock_json = json.dumps(restock_dict)
        logging.debug('Pizza order rejected:\n' + order_json)
        logging.debug('Order ' + order_id + ' rejected due to insufficient stock.\nRestock Order:\n' + restock_json)
        return Response(status=403, mimetype='application/json', response=restock_json)


# Pizza order endpoint
@app.route('/order', methods=['POST'])
def order_funct():
    data = request.get_json()
    order_dict = json.loads(data)
    return order_manager(order_dict)


# Health check endpoint
@app.route('/health', methods=['POST'])
def health_check():
    return Response(status=200,response="healthy\n")
