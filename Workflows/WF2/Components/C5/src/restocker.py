#!/usr/bin/env python

"""The Restocker Component for this Cloud Computing project.

This component recieves restocking orders sent to the workflow manager. The restock orders follow the format of the restock-order.shema.json file in the shema folder. The component also scans the database every 5 minutes to check for items that might need to be restocked.
"""
import json
import time
import threading
import logging
import os

from flask import Flask, request, Response
from cassandra.cluster import Cluster
import docker
import jsonschema
import uuid

__author__ = "Carla Vazquez, Chris Scott"
__version__ = "2.0.0"
__maintainer__ = "Chris Scott"
__email__ = "cms190009@utdallas.edu"
__status__ = "Development"

# Connect to casandra service
cass_IP = os.environ["CASS_DB"]
cluster = Cluster([cass_IP])
session = cluster.connect('pizza_grocery')

# prepared statements
while True:
    try:
        get_quantity = session.prepare('\
            SELECT quantity \
            FROM stock  \
            WHERE storeID = ? AND itemName = ?\
        ')
        add_stock_prepared = session.prepare('\
            UPDATE stock \
            SET quantity = ?  \
            WHERE storeID = ? AND itemName = ?\
        ')
        get_stores = session.prepare("SELECT storeID FROM stores")
        get_items = session.prepare("SELECT name FROM items")
        select_stock_prepared = session.prepare('SELECT * FROM stock WHERE storeID=?')
        update_stock_prepared = session.prepare('\
            UPDATE stock \
            SET quantity=? \
            WHERE storeID=? AND itemName=?\
        ')
    except:
        time.sleep(5)
    else:
        break

# set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# create flask app
app = Flask(__name__)

# Open jsonschema for workflow-request
with open("src/workflow-request.schema.json", "r") as workflow_schema:
    workflow_schema = json.loads(workflow_schema.read())

# Global pizza items/ingredients dict
items_dict = {
    'Dough': 0,         'SpicySauce': 0,        'TraditionalSauce': 0,  'Cheese': 0,
    'Pepperoni': 0,     'Sausage': 0,           'Beef': 0,              'Onion': 0,
    'Chicken': 0,       'Peppers': 0,           'Olives': 0,            'Bacon': 0,
    'Pineapple': 0,     'Mushrooms': 0
}

# Global workflows dict
workflows = dict()


def get_next_component(store_id):
    comp_list = workflows[store_id]["component-list"].copy()
    comp_list.remove("cass")
    next_comp_index = comp_list.index("restocker") + 1
    if next_comp_index >= len(comp_list):
        return None
    return comp_list[next_comp_index]


def get_component_url(component, store_id):
    comp_name = component +\
        (str(workflows[store_id]["workflow-offset"]) if workflows[store_id]["method"] == "edge" else "")
    url = "http://" + comp_name + ":"
    if component == "order-verifier":
        url += "1000/order"
    elif component == "delivery-assigner":
        url += "3000/order"
    elif component == "auto-restocker":
        url += "4000/order"
    elif component == "order-processor":
        url += "6000/order"
    return url


def send_order_to_next_component(url, order):
    cust_name = order["pizza-order"]["custName"]
    response = requests.post(url, json=json.dumps(order))
    if response.status_code == 200:
        logging.info("Processed order for {}. Order sent to next component.".format(cust_name))
    else:
        logging.info("Processed order for {}. Issue sending order to next component:".format(cust_name))
        logging.info(response.text)


def send_results_to_client(store_id, order):
    origin_url = "http://" + workflows[store_id]["origin"] + ":8080/results"
    cust_name = order["pizza-order"]["custName"]
    message = "Order for " + cust_name

    if "assignment" in order:
        delivery_entity = order["assignment"]["deliveredBy"]
        estimated_time = str(order["assignment"]["estimatedTime"])
        message += " will be delivered in " + estimated_time
        message += " minutes by delivery entity " + delivery_entity + "."
    else:
        message += " has been placed."

    response = requests.post(origin_url, json=json.dumps({"message": message}))
    if response.status_code == 200:
        logging.info("Restuarant Owner recieved results for order from " + cust_name)
    else:
        logging.info("Issue sending results for order from " + cust_name + "\n" + response.txt)


# Decrement a store's stock for the order about to be placed
def decrement_stock(store_uuid, instock_dict, required_dict):
    for item_name in required_dict:
        quantity = instock_dict[item_name] - required_dict[item_name]
        session.execute(update_stock_prepared, (quantity, store_uuid, item_name))


# Aggregate all ingredients for a given order
def aggregate_ingredients(pizza_list):
    ingredients = items_dict.copy()

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


# Check stock at a given store to determine if order can be filled
def check_stock(store_uuid, order_dict):
    instock_dict = items_dict.copy()
    required_dict = aggregate_ingredients(order_dict["pizzaList"])
    restock_list = list()

    # If insufficient stock, restock_list contains items for restock
    # Otherwise, restock_list is an empty list
    rows = session.execute(select_stock_prepared, (store_uuid,))
    for row in rows:
        if row.quantity < required_dict[row.itemname]:
            restock_list.append({"item-name": row.itemname, "quantity": required_dict[row.itemname]})
        instock_dict[row.itemname] = row.quantity

    return instock_dict, required_dict, restock_list


# the order endpoint
@app.route('/order', methods=['POST'])
def restocker():
    logging.info("POST /order")
    data = json.loads(request.get_json())
    
    if "pizza-order" not in data:
        order = {"pizza-order": data}
    else:
        order = data.copy()

    if order["pizza-order"]["storeId"] not in workflows:
        message = "Workflow does not exist. Request Rejected."
        logging.info(message)
        return Response(status=422, text=message)

    store_id = order["pizza-order"]["storeId"]
    store_uuid = uuid.UUID(store_id)

    valid = True
    mess = None
    try:
        # check stock
        instock_dict, required_dict, restock_list = check_stock(store_uuid, order["pizza-order"])

        # restock, if needed
        if restock_list:
            # perform restock
            for item_dict in restock_list:
                quantity = item_dict["quantity"] + 20
                session.execute(add_stock_prepared, (quantity, store_uuid, item_dict["item-name"]))

        # decrement stock
        decrement_stock(store_uuid, instock_dict, required_dict)
    except Exception as inst:
        valid = False
        mess = inst.args[0]

    if valid:
        # update order with restock status
        logging.info("Restock successful")
        return Response(status=200)
    else:
        # update order with restock status
        logging.info("Restocker failure for order request:\n" + mess)
        return Response(status=400)


def verify_workflow(data):
    global workflow_schema
    valid = True
    mess = None
    try:
        jsonschema.validate(instance=data, schema=workflow_schema)
    except Exception as inst:
        valid = False
        mess = inst.args[0]
    return valid, mess


# if workflow-request is valid and does not exist, create it
@app.route("/workflow-requests/<storeId>", methods=['PUT'])
def setup_workflow(storeId):
    data = json.loads(request.get_json())
    valid, mess = verify_workflow(data)

    if not valid:
        logging.info("workflow-request ill formatted")
        return Response(status=400, response="workflow-request ill formatted\n" + mess)

    if storeId in workflows:
        logging.info("Workflow " + storeId + " already exists")
        return Response(status=409, response="Workflow " + storeId + " already exists\n")

    workflows[storeId] = data

    logging.info("Workflow started for Store " + storeId)

    return Response(status=201, response="Restocker deployed for {}\n".format(storeId))    


# if the recource exists, update it
@app.route("/workflow-update/<storeId>", methods=['PUT'])
def update_workflow(storeId):
    logging.info("PUT /workflow-update/" + storeId)
    data = json.loads(request.get_json())
    valid, mess = verify_workflow(data)

    if not valid:
        logging.info("workflow-request ill formatted")
        return Response(status=400, response="workflow-request ill formatted\n" + mess)

    if not ("cass" in data["component-list"]):
        logging.info("Update rejected, cass is a required workflow component")
        return Response(status=422, response="Update rejected, cass is a required workflow component.\n")

    workflows[storeId] = data

    logging.info("Restocker updated for Store " + storeId)

    return Response(status=200, response="Restocker updated for {}\n".format(storeId))


@app.route("/workflow-requests/<storeId>", methods=["DELETE"])
def teardown_workflow(storeId):
    if storeId not in workflows:
        return Response(status=404, response="Workflow doesn't exist. Nothing to teardown.\n")
    else:
        del workflows[storeId]
        logging.info("Restocker stopped for {}\n".format(storeId))
        return Response(status=204)


# retrieve the specified resource, if it exists
@app.route("/workflow-requests/<storeId>", methods=["GET"])
def retrieve_workflow(storeId):
    logging.info("GET /workflow-requests/" + storeId)
    if not (storeId in workflows):
        return Response(status=404, response="Workflow doesn't exist. Nothing to retrieve.\n")
    else:
        return Response(status=200, response=json.dumps(workflows[storeId]))


# retrieve all resources
@app.route("/workflow-requests", methods=["GET"])
def retrieve_workflows():
    logging.info("GET /workflow-requests")
    return Response(status=200, response=json.dumps(workflows))


# the health endpoint, so that users can verify that the server is up and running
@app.route('/health', methods=['GET'])
def health_check():
    logging.info("GET /health")
    return Response(status=200,response="healthy\n")


# scan the database for items that are out of stock or close to it
def scan_out_of_stock():
    # gets a list of active store workflows
    stores = workflows.keys()
    # loops through said stores
    for store in stores:
        # gets a list of all items
        items = session.execute(get_items)
        # loops through said items
        for item in items:
            # if the item exsists at the store
            quantity = session.execute(get_quantity, (store.storeid, item.name))
            quantity_row = quantity.one()
            if quantity_row != None:
                # and it is low in quantity
                if quantity_row.quantity < 5.0 :
                    # restock it
                    session.execute(add_stock_prepared, (quantity_row.quantity + 20, store.storeid, item.name))
                    logging.info(str(store.storeid) + ", " + item.name +
                        " has " + str(quantity_row.quantity + 20.0))
    if app.config["ENV"] == "production": 
        threading.Timer(60, scan_out_of_stock).start()

# calls the scan_out_of_stock function for the first time
# scan_out_of_stock()
