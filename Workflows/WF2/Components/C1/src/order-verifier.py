"""Order Verifier Component

Upon receiving an order from the Workflow Manager (WFM), this component validates the order, checks if sufficient stock exists, and if the stock exists, then it creates the order. If sufficient stock is not available, this component recreates a restock order and provides it as a response to the WFM.
"""

from flask import Flask, request, Response
from cassandra.cluster import Cluster
from datetime import datetime, timedelta, date
import copy
import jsonschema
import json
import logging
import requests
import threading
import time
import uuid
import os

__author__ = "Chris Scott"
__version__ = "1.0.0"
__maintainer__ = "Chris Scott"
__email__ = "christopher.scott@utdallas.edu"
__status__ = "Development"

# Connect to Cassandra service
cass_IP = os.environ["CASS_DB"]
cluster = Cluster([cass_IP])
session = cluster.connect('pizza_grocery')

# Cassandra prepared statements
select_stock_prepared = session.prepare('SELECT * FROM stock WHERE storeID=?')
select_items_prepared = session.prepare('SELECT * FROM items WHERE name=?')
select_stock_tracker_prepared = session.prepare('\
    SELECT * \
    FROM stockTracker \
    WHERE storeID=? AND itemName=? AND dateSold=?\
')
update_stock_prepared = session.prepare('\
    UPDATE stock \
    SET quantity=? \
    WHERE storeID=? AND itemName=?\
')
update_stock_tracker_prepared = session.prepare('\
    UPDATE stockTracker \
    SET quantitySold=? \
    WHERE storeID=? AND itemName=? AND dateSold=?\
')
insert_customers_prepared = session.prepare('\
    INSERT INTO customers (customerName, latitude, longitude) \
    VALUES (?, ?, ?)\
')
insert_payments_prepared = session.prepare('\
    INSERT INTO payments (paymentToken, method) \
    VALUES (?, ?)\
')
insert_pizzas_prepared = session.prepare('\
    INSERT INTO pizzas (pizzaID, toppings, cost) \
    VALUES (?, ?, ?)\
')
insert_order_prepared = session.prepare('\
    INSERT INTO orderTable \
        (orderID, orderedFrom, orderedBy, deliveredBy, containsPizzas, \
            containsItems, paymentID, placedAt, active, estimatedDeliveryTime) \
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)\
')
insert_order_by_store_prepared = session.prepare('\
    INSERT INTO orderByStore (orderedFrom, placedAt, orderID) \
    VALUES (?, ?, ?)\
')
insert_order_by_customer_prepared = session.prepare('\
    INSERT INTO orderByCustomer (orderedBy, placedAt, orderID) \
    VALUES (?, ?, ?)\
')
insert_stock_tracker_prepared = session.prepare('\
    INSERT INTO stockTracker (storeID, itemName, quantitySold, dateSold) \
    VALUES (?, ?, ?, ?)\
')

# Create Flask app
app = Flask(__name__)

# Open jsonschema for pizza orders
with open("src/pizza-order.schema.json", "r") as schema:
    schema = json.loads(schema.read())

# Logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Global variable stock_tracker_offset is used to artificially accelerate timestamps in stockTracker table
# The purpose of this is to provide sufficient data for Component 4
stock_tracker_offset = -10

# Global dict of pizza items/ingredients
items_dict = {
    'Dough': 0,         'SpicySauce': 0,        'TraditionalSauce': 0,  'Cheese': 0,
    'Pepperoni': 0,     'Sausage': 0,           'Beef': 0,              'Onion': 0,
    'Chicken': 0,       'Peppers': 0,           'Olives': 0,            'Bacon': 0,
    'Pineapple': 0,     'Mushrooms': 0
}


# Aggregate all ingredients for a given order
def aggregate_ingredients(pizza_list):
    ingredients = copy.deepcopy(items_dict)

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
def decrement_stock(store_uuid, in_stock_dict, req_item_dict):
    for item_name in req_item_dict:
        new_quantity = in_stock_dict[item_name] - req_item_dict[item_name]
        session.execute(update_stock_prepared, (new_quantity, store_uuid, item_name))


# Calculate pizza price based on ingredients
def calc_pizza_cost(topping_set):
    # Note: topping_set also contains dough amount, sauce type, and cheese amount,
    # in addition to the toppings. Name was selected to be consistent with DB naming
    cost = 0.0
    for topping in topping_set:
        result = session.execute(select_items_prepared, (topping[0],))
        for (name, price) in result:
            cost += price * topping[1] 
    return cost


# Insert an order's pizza(s) into 'pizzas' table
def insert_pizzas(pizza_list):
    pizza_uuid_set = set()

    for pizza in pizza_list:
        pizza_uuid = uuid.uuid4()
        pizza_uuid_set.add(pizza_uuid)
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
    
    return pizza_uuid_set


# Function to periodically increment the global variable stock_tracker_offset
def inc_stock_tracker_offset():
    global stock_tracker_offset
    stock_tracker_offset += 1
    threading.Timer(900, inc_stock_tracker_offset).start()  # 900 seconds for prepop image


# Insert or update stockTracker table for items sold per day
def stock_tracker_mgr(store_uuid, req_item_dict):
    date_sold = datetime.combine(date.today(), datetime.min.time())
    #offset_date = date.today() + timedelta(days=stock_tracker_offset)
    #date_sold = datetime.combine(offset_date, datetime.min.time())
    logging.debug("Inserting in stockTracker for Date: " + str(date_sold))
    for item_name in req_item_dict:
        rows = session.execute(select_stock_tracker_prepared, (store_uuid, item_name, date_sold))
        if not rows:
            session.execute(insert_stock_tracker_prepared, (store_uuid, item_name, req_item_dict[item_name], date_sold))
        else:
            for row in rows:
                quantity = row.quantitysold + req_item_dict[item_name]
                session.execute(update_stock_tracker_prepared, (quantity, store_uuid, item_name, date_sold))


# Insert order info into DB
def create_order(order_id, order_dict, req_item_dict):
    order_uuid = uuid.UUID(order_id)
    store_uuid = uuid.UUID(order_dict["storeId"])
    pay_uuid = uuid.UUID(order_dict["paymentToken"])
    cust_name = order_dict["custName"]
    cust_lat = order_dict["custLocation"]["lat"]
    cust_lon = order_dict["custLocation"]["lon"]
    placed_at = datetime.now()

    # Insert customer information into 'customers' table
    session.execute(insert_customers_prepared, (cust_name, cust_lat, cust_lon))
    # Insert order payment information into 'payments' table
    session.execute(insert_payments_prepared, (pay_uuid, order_dict["paymentTokenType"]))  
    # Insert the ordered pizzas into 'pizzas' table
    pizza_uuid_set = insert_pizzas(order_dict["pizzaList"])
    # Insert order into 'orderTable' table
    session.execute(insert_order_prepared, 
        (order_uuid, store_uuid, cust_name, "", pizza_uuid_set, None, pay_uuid, placed_at, True, -1)
    )
    # Insert order into 'orderByStore' table
    session.execute(insert_order_by_store_prepared, (store_uuid, placed_at, order_uuid))
    # Insert order into 'orderByCustomer' table
    session.execute(insert_order_by_customer_prepared, (cust_name, placed_at, order_uuid))
    # Insert or update 'stockTracker' table
    stock_tracker_mgr(store_uuid, req_item_dict)
 

# Check stock at a given store to determine if order can be filled
def check_stock(order_id, order_dict):
    in_stock_dict = copy.deepcopy(items_dict)
    store_id = uuid.UUID(order_dict["storeId"])
    req_item_dict = aggregate_ingredients(order_dict["pizzaList"])
    restock_list = []

    # If there is insufficient stock, restock_list contains items for restock
    # Otherwise, restock_list is an empty list
    rows = session.execute(select_stock_prepared, (store_id,))
    for row in rows:
        if row.quantity < req_item_dict[row.itemname]:
            restock_list.append({"item-name": row.itemname, "quantity": req_item_dict[row.itemname]})
        else:
            in_stock_dict[row.itemname] = row.quantity

    return in_stock_dict, req_item_dict, restock_list


# Manages order placement and restock, if needed
def order_manager(order_dict):
    # Validate order against schema
    global schema
    try:
        jsonschema.validate(instance=order_dict, schema=schema)
    except:
        logging.debug('Request rejected, failed validation:\n' + json.dumps(order_dict))
        return Response(status=400, response="Request rejected, failed validation")

    order_id = str(uuid.uuid4())  # Assign order_id to order_dict
    logging.debug('Order request received: ' + order_id)

    # Check the stock to see if order can be placed
    in_stock_dict, req_item_dict, restock_list = check_stock(order_id, order_dict)

    if restock_list:    
        # Restock item(s) contained in restock_list before creating order
        restock_dict = {"storeID": order_dict["storeId"], "restock-list": restock_list}
        logging.debug('Order ' + order_id + ' requires restock')
        #response = requests.post("http://restocker:5000/restock", json=restock_dict)
        response = requests.post("http://0.0.0.0:5000/restock", json=restock_dict)
        logging.debug(response.text)
        if response.status_code != 200:
            # Restock was unsuccesful, must reject order request
            return Response(status=response.status_code, response=response.text)

    # Decrement stock and create the order
    decrement_stock(uuid.UUID(order_dict["storeId"]), in_stock_dict, req_item_dict)
    create_order(order_id, order_dict, req_item_dict)

    # Assign delivery entity
    logging.debug('Assigning delivery entity for Order ' + order_id)
    #response = requests.post("http://delivery-assigner:3000/assign-entity", json={"order_id":order_id})
    response = requests.post("http://0.0.0.0:3000/assign-entity", json={"order_id":order_id})
    logging.debug(response.text)
    if response.status_code != 200:
        # Could not assign delivery entity, but order has been created
        return Response(status=response.status_code, response=response.text)

    # The order has now been created
    logging.debug('Pizza Order ' + order_id + ' has been placed.')
    return Response(status=200, response=response.text)


# Pizza order endpoint
@app.route('/order', methods=['POST'])
def order_funct():
    data = request.get_json()
    order_dict = json.loads(data)
    return order_manager(order_dict)


# Health check endpoint
@app.route('/health', methods=['GET'])
def health_check():
    return Response(status=200,response="healthy\n")


# First call to inc_stock_tracker_day function
#inc_stock_tracker_offset()
