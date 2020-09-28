from flask import Flask, request, Response
from cassandra.cluster import Cluster
from datetime import datetime
import jsonschema
import json
import logging
import time
import uuid

#logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)

cluster = Cluster()     # Add Cassandra VIPs here
session = cluster.connect('pizza_grocery')
check_stock_prepared = session.prepare('SELECT * FROM stock WHERE storeID=?')
dec_stock_prepared = session.prepare('UPDATE stock SET quantity=? WHERE storeID=? AND itemName=?')
insert_cust_prepared = session.prepare('INSERT INTO customers (customerName, latitude, longitude) VALUES (?, ?, ?)')
insert_pay_prepared = session.prepare('INSERT INTO payments (paymentToken, method) VALUES (?, ?)')
insert_pizzas_prepared = session.prepare('INSERT INTO pizzas (pizzaID, toppings, cost) VALUES (?, ?, ?)')
insert_order_prepared = session.prepare('INSERT INTO orderTable (orderID, orderedFrom, orderedBy, delivieredBy, containsPizzas, containsItems, paymentID, placedAt, active, estimatedDeliveryTime) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)')
item_price_prepared = session.prepare('SELECT * FROM items WHERE name=?')

with open("src/schema.json", "r") as schema:
    schema = json.loads(schema.read())


def aggregate_supplies(pizza_list):
    supplies = {'Dough': 0,         'SpicySauce': 0,        'TraditionalSauce': 0,  'Cheese': 0,
                'Pepperoni': 0,     'Sausage': 0,           'Beef': 0,              'Onion': 0,
                'Chicken': 0,       'Peppers': 0,           'Olives': 0,            'Bacon': 0,
                'Pineapple': 0,     'Mushrooms': 0}

    for pizza in pizza_list:
        if pizza['crustType'] == 'Thin':
            supplies['Dough'] += 1
        elif pizza['crustType'] == 'Traditional':
            supplies['Dough'] += 2

        if pizza['sauceType'] == 'Spicy':
            supplies['SpicySauce'] += 1
        elif pizza['sauceType'] == 'Traditional':
            supplies['TraditionalSauce'] += 1

        if pizza['cheeseAmt'] == 'Light':
            supplies['Cheese'] += 1
        elif pizza['cheeseAmt'] == 'Normal':
            supplies['Cheese'] += 2
        elif pizza['cheeseAmt'] == 'Extra':
            supplies['Cheese'] += 3

        for topping in pizza["toppingList"]:
            supplies[topping] += 1

    return supplies


def decrement_stock(store_id, instock_dict, required_dict):
    for item_name in required_dict:
        new_quantity = instock_dict[item_name] - required_dict[item_name]
        session.execute(dec_stock_prepared, (new_quantity, store_id, item_name))


def calc_pizza_cost(topping_set):
    cost = 0.0

    for topping in topping_set:
        result = session.execute(item_price_prepared, (topping[0],))
        for (name, price) in result:
            cost += price * topping[1] 

    return cost


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


def insert_order(order_id, order_dict):
    # Insert customer information into 'customers' table
    session.execute(insert_cust_prepared, (order_dict[order_id]["custName"], order_dict[order_id]["custLocation"]["lat"], order_dict[order_id]["custLocation"]["lon"]))
    
    # Insert payment information into 'payments' table
    session.execute(insert_pay_prepared, (uuid.UUID(order_dict[order_id]["paymentToken"]), order_dict[order_id]["paymentTokenType"]))
    
    # Insert pizzas into 'pizzas' table
    pizza_uuid_set = insert_pizzas(order_dict[order_id]["pizzaList"])
    
    # Insert order into 'orderTable'
    order_uuid = uuid.UUID(order_id)
    store_uuid = uuid.UUID(order_dict[order_id]["storeId"])
    pay_uuid = uuid.UUID(order_dict[order_id]["paymentToken"])
    session.execute(insert_order_prepared, (order_uuid, store_uuid, order_dict[order_id]["custName"], "", pizza_uuid_set, None, pay_uuid, datetime.now(), True, -1))


def check_stock(order_dict):
    in_stock = True
    instock_dict = {'Dough': 0,         'SpicySauce': 0,        'TraditionalSauce': 0,  'Cheese': 0,
                    'Pepperoni': 0,     'Sausage': 0,           'Beef': 0,              'Onion': 0,
                    'Chicken': 0,       'Peppers': 0,           'Olives': 0,            'Bacon': 0,
                    'Pineapple': 0,     'Mushrooms': 0}
    for order_id in order_dict:
        store_id = uuid.UUID(order_dict[order_id]["storeId"])
    required_dict = aggregate_supplies(order_dict[order_id]["pizzaList"])
    restock_list = []

    rows = session.execute(check_stock_prepared, (store_id,))
    for row in rows:
        if row.quantity < required_dict[row.itemname]:
            in_stock = False
            restock_list.append({"item-name": row.itemname, "quantity": row.quantity})
        else:
            instock_dict[row.itemname] = row.quantity

    if in_stock:
        decrement_stock(store_id, instock_dict, required_dict)
        insert_order(order_id, order_dict)

    return restock_list


def verify_order(order_dict):
    global schema
    try:
        for order_id in order_dict:
            jsonschema.validate(instance=order_dict[order_id], schema=schema)
    except:
        return Response(response="JSON failed validation",
                status=400,
                mimetype='application/json')

    restock_list = check_stock(order_dict)
    if not restock_list:    # If restock_list is empty
        return Response(response="Order accepted, sufficient supplies",
            status=200,
            mimetype='application/json')
    else:
        for order_id in order_dict:
            store_id = order_dict[order_id]["storeId"]
        restock_dict = {"storeID": store_id, "restock-list": restock_list}
        return Response(response=json.dumps(restock_dict),
            status=400,
            mimetype='application/json')


@app.route('/order', methods=['POST'])
def order_funct():
    data = request.get_json()
    order_dict = json.loads(data)
    return verify_order(order_dict)


@app.route('/health', methods=['POST'])
def health_check():
    return Response(status=200,response="healthy")
