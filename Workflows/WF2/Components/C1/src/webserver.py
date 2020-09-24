from flask import Flask, request, Response
from cassandra.cluster import Cluster
import jsonschema
import json

app = Flask(__name__)

cluster = Cluster(['10.0.0.56'])
session = cluster.connect('pizza_grocery')
check_stock_prepared = session.prepare('SELECT quantity FROM stock WHERE store = ? and itemName = ?')
decrement_stock_prepared = session.prepare('UPDATE stock SET quantity = ? WHERE store = ? AND itemName = ?')

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

def decrement_supplies(store_id, instock_dict, supply_dict):
    for item in supply_dict:
        session.execute(decrement_stock_prepared, (instock_dict[item] - supply_dict[item]), store_id, item)


def check_supplies(order_dict):
    supply_dict = aggregate_supplies(order_dict)
    restock_list = []
    instock_dict = dict(supply_dict)    # Create a copy of supply_dict to store instock quantities
    in_stock = True

    for order_id in order_dict:
        store_id = order_dict[order_id]["storeId"]

    for item in supply_dict:
        quantity = session.execute(check_stock_prepared, store_id, item)
        if quantity > supply_dict[item]:
            in_stock = False
            restock_list.append({"item-name": item, "quantity": quantity})
        else:
            instock_dict[item] = quantity

    print(json.dumps(restock_list))

    if in_stock:
        decrement_supplies(store_id, instock_dict, supply_dict)

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
