"""Order Verifier Component

Upon receiving a Pizza Order, this component validates the order and checks the store's stock.
If sufficient stock exists, Order Verifier decrements the store's stock and creates the order. 
Otherwise, Order Verifier requests a restock before decrementing stock and creating the order.
"""

import copy
import json
import logging
import os
import threading
import time
import uuid
from datetime import datetime

import jsonschema
import requests
from cassandra.cluster import Cluster
from flask import Flask, Response, request

from flask import Flask, request, Response
from cassandra.cluster import Cluster
import jsonschema

__author__ = "Chris Scott"
__version__ = "2.0.0"
__maintainer__ = "Chris Scott"
__email__ = "cms190009@utdallas.edu"
__status__ = "Development"

# Connect to Cassandra service
cass_IP = os.environ["CASS_DB"]
cluster = Cluster([cass_IP])
session = cluster.connect('pizza_grocery')

# Cassandra prepared statements
count = 0
while True:
    try:
        select_items_prepared = session.prepare('SELECT * FROM items WHERE name=?')
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
    except:
        count += 1
        if count <= 5:
            time.sleep(5)
        else:
            exit()
    else:
        break

# Create Flask app
app = Flask(__name__)

# Open jsonschema for workflow-request
with open("src/workflow-request.schema.json", "r") as workflow_schema:
    workflow_schema = json.loads(workflow_schema.read())

# Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logging.getLogger('requests').setLevel(logging.INFO)

# Global workflows dict
workflows = dict()


# Calculate pizza price based on ingredients
def calc_pizza_cost(ingredient_set):
    cost = 0.0
    for ingredient in ingredient_set:
        result = session.execute(select_items_prepared, (ingredient[0],))
        for (name, price) in result:
            cost += price * ingredient[1] 
    return cost


# Insert an order's pizza(s) into 'pizzas' table
def insert_pizzas(pizza_list):
    pizza_uuid_set = set()

    for pizza in pizza_list:
        pizza_uuid = uuid.uuid4()
        pizza_uuid_set.add(pizza_uuid)
        ingredient_set = set()

        if pizza["crustType"] == "Thin":
            ingredient_set.add(("Dough", 1))
        elif pizza["crustType"] == "Traditional":
            ingredient_set.add(("Dough", 2))

        if pizza["sauceType"] == "Spicy":
            ingredient_set.add(("SpicySauce", 1))
        elif pizza["sauceType"] == "Traditional":
            ingredient_set.add(("TraditionalSauce", 1))

        if pizza["cheeseAmt"] == "Light":
            ingredient_set.add(("Cheese", 1))
        elif pizza["cheeseAmt"] == "Normal":
            ingredient_set.add(("Cheese", 2))
        elif pizza["cheeseAmt"] == "Extra":
            ingredient_set.add(("Cheese", 3))

        for topping in pizza["toppingList"]:
            ingredient_set.add((topping, 1))
        
        cost = calc_pizza_cost(ingredient_set)
        session.execute(insert_pizzas_prepared, (pizza_uuid, ingredient_set, cost))
    
    return pizza_uuid_set


# Insert order info into DB
def create_order(order_dict):
    order_uuid = uuid.UUID(order_dict["orderId"])
    store_uuid = uuid.UUID(order_dict["storeId"])
    pay_uuid = uuid.UUID(order_dict["paymentToken"])
    cust_name = order_dict["custName"]
    cust_lat = order_dict["custLocation"]["lat"]
    cust_lon = order_dict["custLocation"]["lon"]
    placed_at = datetime.strptime(order_dict["orderDate"], '%Y-%m-%dT%H:%M:%S')

    valid = True
    mess = None
    try:
        # Insert customer information into 'customers' table
        session.execute(insert_customers_prepared, (cust_name, cust_lat, cust_lon))
        # Insert order payment information into 'payments' table
        session.execute(insert_payments_prepared, (pay_uuid, order_dict["paymentTokenType"]))  
        # Insert the ordered pizzas into 'pizzas' table
        pizza_uuid_set = insert_pizzas(order_dict["pizzaList"])
        # Insert order into 'orderTable' table
        session.execute(
            insert_order_prepared, 
            (order_uuid, store_uuid, cust_name, "", pizza_uuid_set, None, pay_uuid, placed_at, True, -1)
        )
        # Insert order into 'orderByStore' table
        session.execute(insert_order_by_store_prepared, (store_uuid, placed_at, order_uuid))
        # Insert order into 'orderByCustomer' table
        session.execute(insert_order_by_customer_prepared, (cust_name, placed_at, order_uuid))
    except Exception as inst:
        valid = False
        mess = inst.args[0]
    
    return valid, mess


def get_next_component(store_id):
    comp_list = workflows[store_id]["component-list"].copy()
    comp_list.remove("cass")
    next_comp_index = comp_list.index("order-verifier") + 1
    if next_comp_index >= len(comp_list):
        return None
    return comp_list[next_comp_index]


def get_component_url(component, store_id):
    comp_name = component +\
        (str(workflows[store_id]["workflow-offset"]) if workflows[store_id]["method"] == "edge" else "")
    url = "http://" + comp_name + ":"
    if component == "delivery-assigner":
        url += "3000/order"
    elif component == "auto-restocker" or component == "predictor":
        url += "4000/order"
    elif component == "restocker":
        url += "5000/order"
    elif component == "order-processor":
        url += "6000/order"
    return url


def send_order_to_next_component(url, order):
    cust_name = order["pizza-order"]["custName"]
    response = requests.post(url, json=json.dumps(order))
    if response.status_code == 200:
        logging.info("Processed order for {}. Order sent to next component.".format(cust_name))
    else:
        logging.info("Processed order for {}. Issue sending order to next component.".format(cust_name))


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


# if pizza-order is valid, try to create it
@app.route('/order', methods=['POST'])
def order_funct():
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

    store_id = order["pizza-list"]["storeId"]
    order["pizza-list"]["orderId"] = str(uuid.uuid4())
    order_id = order["pizza-list"]["orderId"]
    cust_name = order["pizza-list"]["custName"]

    logging.info("Processing order " + order_id + " for " + cust_name + " from store " + store_id)

    valid, mess = create_order(order["pizza-list"])

    if valid:
        order.update({"processor": "accepted"})
        # send order
        return Response(status=200)
    else:
        order.update({"processor": "rejected"})
        message = "Failed to process order request:\n" + mess
        logging.info(message)
        # report failure
        return Response(status=400, text=message)


# validate workflow-request against schema
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
    logging.info("PUT /workflow-requests/" + storeId)
    data = json.loads(request.get_json())
    valid, mess = verify_workflow(data)

    if not valid:
        logging.info("workflow-request ill formatted")
        return Response(status=400, response="workflow-request ill formatted\n" + mess)

    if storeId in workflows:
        logging.info("Workflow " + storeId + " already exists")
        return Response(status=409, response="Workflow " + storeId + " already exists\n")
    
    if not ("cass" in data["component-list"]):
        logging.info("workflow-request rejected, cass is a required workflow component")
        return Response(status=422, response="workflow-request rejected, cass is a required workflow component\n")

    workflows[storeId] = data

    logging.info("Workflow started for {}\n".format(storeId))
    
    return Response(status=201, response="Order Verifier deployed for {}\n".format(storeId))    


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
        logging.info("workflow-request rejected, cass is a required workflow component")
        return Response(status=422, response="workflow-request rejected, cass is a required workflow component\n")

    workflows[storeId] = data

    logging.info("Workflow updated for {}\n".format(storeId))

    return Response(status=200, response="Order Verifier updated for {}\n".format(storeId))


# if the recource exists, remove it
@app.route("/workflow-requests/<storeId>", methods=["DELETE"])
def teardown_workflow(storeId):
    logging.info("DELETE /workflow-requests/" + storeId)
    if not (storeId in workflows):
        return Response(status=404, response="Workflow doesn't exist. Nothing to teardown.\n")
    else:
        del workflows[storeId]
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


# Health check endpoint
@app.route('/health', methods=['GET'])
def health_check():
    logging.info("GET /health")
    return Response(status=200,response="healthy\n")
