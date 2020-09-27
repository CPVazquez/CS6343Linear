from flask import Flask, request, Response
from cassandra.cluster import Cluster
import jsonschema
import json
import logging
import time
import uuid

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)

cluster = Cluster(["10.0.0.10", "10.0.2.136"])
session = cluster.connect('pizza_grocery')
check_stock_prepared = session.prepare('SELECT * FROM stock WHERE storeID=?')
dec_stock_prepared = session.prepare('UPDATE stock SET quantity=? WHERE storeID=? AND itemName=?')
#insert_cust_prepared
#insert_pay_prepared
#insert_pizzas_prepared
#insert_items_prepared

with open("src/schema.json", "r") as schema:
    schema = json.loads(schema.read())


def aggregate_supplies(order_dict):
    supplies = {
        'Dough': 0,         'SpicySauce': 0,        'TraditionalSauce': 0,  'Cheese': 0,
        'Pepperoni': 0,     'Sausage': 0,           'Beef': 0,              'Onion': 0,
        'Chicken': 0,       'Peppers': 0,           'Olives': 0,            'Bacon': 0,
        'Pineapple': 0,     'Mushrooms': 0
    }
    for order_id in order_dict:
        index = 0
        for pizza in order_dict[order_id]['pizzaList']:
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

            for topping in order_dict[order_id]['pizzaList'][index]['toppingList']:
                supplies[topping] += 1
            index += 1
    return supplies


def decrement_stock(store_id, instock_dict, required_dict):
    for item_name in required_dict:
        new_quantity = instock_dict[item_name] - required_dict[item_name]
        logging.debug("Decrementing Stock for Store " + str(store_id) + ": Item - " + item_name + ", Quantity - " + new_quantity)
        session.execute(dec_stock_prepared, (new_quantity, store_id, item_name))


#def insert_order(order_dict):
#    for order_id in order_dict:
#        print(order_id)
#        print(order_dict[order_id]["storeId"])
#        print(order_dict[order_id]["custName"])
#        print(order_dict[order_id]["paymentToken"])
#        print(order_dict[order_id]["paymentTokenType"])
#        print(order_dict[order_id]["custLocation"])
#        for pizza in range(len(order_dict[order_id]["pizzaList"])):
#            print(str(uuid.uuid4()))
#            print(order_dict[order_id]["pizzaList"][pizza])


def check_supplies(order_dict):
    required_dict = aggregate_supplies(order_dict)
    restock_list = []
    instock_dict = dict(required_dict)    # Create a copy of required_dict to store instock quantities
    in_stock = True

    for order_id in order_dict:
        store_id = uuid.UUID(order_dict[order_id]["storeId"])

    rows = session.execute(check_stock_prepared, (store_id,))
    for row in rows:
        if row.quantity < required_dict[row.itemname]:
            in_stock = False
            restock_list.append({"item-name": row.itemname, "quantity": row.quantity})
        else:
            instock_dict[row.itemname] = row.quantity

    if in_stock:
        decrement_stock(store_id, instock_dict, required_dict)
        #insert_order(order_dict)

    return in_stock


def verify_order(order_dict):
    global schema
    try:
        for order_id in order_dict:
            jsonschema.validate(instance=order_dict[order_id], schema=schema)
    except:
        return Response(response="JSON failed validation",
                status=400,
                mimetype='application/json')

    if check_supplies(order_dict):
        return Response(response="Order accepted, sufficient supplies",
            status=200,
            mimetype='application/json')
    else:
        # TODO: Notify WFM that a restock is needed
        return Response(response="Order rejected, insufficient supplies",
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
