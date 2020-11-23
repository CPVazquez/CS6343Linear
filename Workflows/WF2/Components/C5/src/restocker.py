"""The Restocker Component for this Cloud Computing project.

Upon receiving a pizza-order request, Restocker aggregates the pizza ingredients from 
the pizzas contained in the pizza-order and checks the store’s stock to determine if 
there is sufficient stock to fill the order. If the current stock is insufficient, 
then a restock is performed for the deficient items so that the order can be filled. 
Once there is sufficient stock, this component decrements the store’s stock by the 
required amounts to fill the order, and the request is sent to the next component 
in the workflow, if one exists. The request is then sent to the next component in 
the workflow, if one exists. As a secondary function, this component scans the 
database at the end of every workflow day to check for items that might need to be 
restocked. If stock quantity for any item is below 10, then that item is restocked 
to a quantity of 50.
"""

import json
import logging
import os
import threading
import time
import uuid

import jsonschema
import requests
from cassandra.cluster import Cluster
from quart import Quart, Response, request
from quart.utils import run_sync

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
    except Exception:
        time.sleep(5)
    else:
        break

# set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logging.getLogger('requests').setLevel(logging.WARNING)
logging.getLogger('quart.app').setLevel(logging.WARNING)
logging.getLogger('quart.serving').setLevel(logging.WARNING)

# create Quart app
app = Quart(__name__)

# Open jsonschema for workflow-request
with open("src/workflow-request.schema.json", "r") as workflow_schema:
    workflow_schema = json.loads(workflow_schema.read())

# Global pizza items/ingredients dict
items_dict = {
    'Dough': 0,         'SpicySauce': 0,        'TraditionalSauce': 0,
    'Cheese': 0,        'Pepperoni': 0,         'Sausage': 0,
    'Beef': 0,          'Onion': 0,             'Chicken': 0,
    'Peppers': 0,           'Olives': 0,            'Bacon': 0,
    'Pineapple': 0,     'Mushrooms': 0
}

# Global workflows dict
workflows = dict()


###############################################################################
#                           Helper Functions
###############################################################################

async def get_next_component(store_id):
    comp_list = workflows[store_id]["component-list"].copy()
    comp_list.remove("cass")
    next_comp_index = comp_list.index("restocker") + 1
    if next_comp_index >= len(comp_list):
        return None
    return comp_list[next_comp_index]


async def get_component_url(component, store_id):
    comp_name = component +\
        (str(workflows[store_id]["workflow-offset"]) if workflows[store_id]["method"] == "edge" else "")
    url = "http://" + comp_name + ":"
    if component == "order-verifier":
        url += "1000/order"
    elif component == "delivery-assigner":
        url += "3000/order"
    elif component == "stock-analyzer":
        url += "4000/order"
    elif component == "order-processor":
        url += "6000/order"
    return url


async def send_order_to_next_component(url, order):
    # send order to next component
    def request_post():
        return requests.post(url, json=json.dumps(order))

    r = await run_sync(request_post)()
        
    return Response(status=r.status_code, response=r.text)


# Decrement a store's stock for the order about to be placed
async def decrement_stock(store_uuid, instock_dict, required_dict):

    def update_stock_prepared_execute():
        session.execute(update_stock_prepared, (quantity, store_uuid, item_name))

    for item_name in required_dict:
        quantity = instock_dict[item_name] - required_dict[item_name]
        await run_sync(update_stock_prepared_execute)()


# Aggregate all ingredients for a given order
async def aggregate_ingredients(pizza_list):
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
async def check_stock(store_uuid, order_dict):
    instock_dict = items_dict.copy()
    required_dict = await aggregate_ingredients(order_dict["pizzaList"])
    restock_list = list()   # restock_list will be empty if no items need restocking

    def check_stock_execute():
        return session.execute(select_stock_prepared, (store_uuid,))

    rows = await run_sync(check_stock_execute)()
    for row in rows:
        if row.quantity < required_dict[row.itemname]:
            quantity_difference = \
                required_dict[row.itemname] - instock_dict[row.itemname]
            restock_list.append(
                {"item-name": row.itemname, "quantity": quantity_difference}
            )
        instock_dict[row.itemname] = row.quantity

    return instock_dict, required_dict, restock_list


async def verify_workflow(data):
    global workflow_schema
    valid = True
    mess = None
    try:
        jsonschema.validate(instance=data, schema=workflow_schema)
    except Exception as inst:
        valid = False
        mess = inst.args[0]
    return valid, mess


###############################################################################
#                           API Endpoints
###############################################################################

# the order endpoint
@app.route('/order', methods=['POST'])
async def restocker():
    logging.info("{:*^74}".format(" POST /order "))
    start = time.time()
    request_data = await request.get_json()
    order = json.loads(request_data)

    if order["pizza-order"]["storeId"] not in workflows:
        message = "Workflow does not exist. Request Rejected."
        logging.info(message)
        return Response(status=422, response=message)

    cust_name = order["pizza-order"]["custName"]
    store_id = order["pizza-order"]["storeId"]
    store_uuid = uuid.UUID(store_id)

    logging.info("Store " + store_id + ":")
    logging.info("Checking stock for order from " + cust_name + ".")

    valid = True
    mess = None

    def add_stock_prepared_execute():
        return session.execute(
                    add_stock_prepared,
                    (new_quantity, store_uuid, item_dict["item-name"])
                )

    try:
        # check stock
        instock_dict, required_dict, restock_list = \
            await check_stock(store_uuid, order["pizza-order"])
        # restock, if needed
        if restock_list:
            # perform restock
            for item_dict in restock_list:
                new_quantity = \
                    item_dict["quantity"] + instock_dict[item_dict["item-name"]] + 10
                instock_dict[item_dict["item-name"]] = new_quantity
                await run_sync(add_stock_prepared_execute)()
        # decrement stock
        await decrement_stock(store_uuid, instock_dict, required_dict)
    except Exception as inst:
        valid = False
        mess = inst.args[0]

    if not valid:
        # failure of some kind, return error message
        error_mess = "Request rejected, restock failed:  " + mess
        logging.info(error_mess)
        return Response(status=400, response=error_mess)

    order.update({"stock": {"status": "sufficient", "restocked": restock_list}})

    log_mess = "Sufficient stock for order from " + cust_name + "."

    next_comp = await get_next_component(store_id)

    end = time.time() - start
    order["restocker_execution_time"] = end

    if next_comp is not None:
        # send order to next component in workflow
        next_comp_url = await get_component_url(next_comp, store_id)
        resp = await send_order_to_next_component(next_comp_url, order)
        if resp.status_code == 200:
            # successful response from next component, return same response
            logging.info(log_mess + " Order sent to next component.")
            return resp
        elif resp.status_code == 208:
            # an error occurred in the workflow but has been handled already
            # return the response unchanged
            return resp
        else:
            # an error occurred in the next component, add the response status
            # code and text to 'error' key in order dict and return it
            logging.info(log_mess + " Issue sending order to next component:")
            logging.info(resp.text)
            order.update({"error": {"status-code": resp.status_code, "text": resp.text}})
            return Response(status=208, response=json.dumps(order))
    
    # last component, print successful log message and return processed order
    logging.info(log_mess)

    return Response(status=200, response=json.dumps(order))
        

# if workflow-request is valid and does not exist, create it
@app.route("/workflow-requests/<storeId>", methods=['PUT'])
async def setup_workflow(storeId):
    logging.info("{:*^74}".format(" PUT /workflow-requests/" + storeId + " "))
    request_data = await request.get_json()
    data = json.loads(request_data)
    # verify the workflow-request is valid
    valid, mess = await verify_workflow(data)

    if not valid:
        logging.info("workflow-request ill formatted")
        return Response(
            status=400,
            response="workflow-request ill formatted\n" + mess
        )

    if storeId in workflows:
        logging.info("Workflow " + storeId + " already exists")
        return Response(
            status=409,
            response="Workflow " + storeId + " already exists\n"
        )

    workflows[storeId] = data

    logging.info("Workflow started for Store " + storeId)

    return Response(
        status=201,
        response="Restocker deployed for {}\n".format(storeId)
    )


# if the recource exists, update it
@app.route("/workflow-update/<storeId>", methods=['PUT'])
async def update_workflow(storeId):
    logging.info("{:*^74}".format(" PUT /workflow-update/" + storeId + " "))
    request_data = await request.get_json()
    data = json.loads(request_data)
    # verify the workflow-request is valid
    valid, mess = await verify_workflow(data)

    if not valid:
        logging.info("workflow-request ill formatted")
        return Response(
            status=400,
            response="workflow-request ill formatted\n" + mess
        )

    if not ("cass" in data["component-list"]):
        logging.info("Update rejected, cass is a required workflow component")
        return Response(
            status=422,
            response="Update rejected, cass is a required workflow component.\n"
        )

    workflows[storeId] = data

    logging.info("Restocker updated for Store " + storeId)

    return Response(
        status=200,
        response="Restocker updated for {}\n".format(storeId)
    )


# delete the specified resource, if it exists
@app.route("/workflow-requests/<storeId>", methods=["DELETE"])
async def teardown_workflow(storeId):
    logging.info("{:*^74}".format(" DELETE /workflow-requests/" + storeId + " "))
    if storeId not in workflows:
        return Response(
            status=404,
            response="Workflow doesn't exist. Nothing to teardown.\n"
        )
    else:
        del workflows[storeId]
        logging.info("Restocker stopped for {}".format(storeId))
        return Response(status=204, response="restocker stopped")


# retrieve the specified resource, if it exists
@app.route("/workflow-requests/<storeId>", methods=["GET"])
async def retrieve_workflow(storeId):
    logging.info("{:*^74}".format(" GET /workflow-requests/" + storeId + " "))
    if not (storeId in workflows):
        return Response(
            status=404,
            response="Workflow doesn't exist. Nothing to retrieve.\n"
        )
    else:
        return Response(
            status=200,
            response=json.dumps(workflows[storeId])
        )


# retrieve all resources
@app.route("/workflow-requests", methods=["GET"])
async def retrieve_workflows():
    logging.info("{:*^74}".format(" GET /workflow-requests "))
    return Response(status=200, response=json.dumps(workflows))


# the health endpoint, to verify that the server is up and running
@app.route('/health', methods=['GET'])
async def health_check():
    logging.info("{:*^74}".format(" GET /health "))
    return Response(status=200, response="healthy\n")


###############################################################################
#                    Periodic Scan DB Stock for Restock
###############################################################################

# scan the database for items that are out of stock or close to it
def scan_out_of_stock():
    # gets a list of active store workflows
    stores = workflows.keys()

    # loops through said stores
    for store_id in stores:
        store_uuid = uuid.UUID(store_id)
        # gets a list of all items
        items = session.execute(get_items)
        # loops through said items
        for item in items:
            # if the item exsists at the store
            quantity = session.execute(get_quantity, (store_uuid, item.name))
            quantity_row = quantity.one()
            if quantity_row is not None:
                # and it is low in quantity
                if quantity_row.quantity < 10.0:
                    # restock it
                    new_quantity = 50
                    session.execute(add_stock_prepared, (new_quantity, store_uuid, item.name))
                    logging.info("Store " + store_id + " Daily Scan:")
                    logging.info(item.name + " restocked to " + str(new_quantity))
    # if app.config["ENV"] == "production":
    threading.Timer(60, scan_out_of_stock).start()


# call scan_out_of_stock() for the first time
scan_out_of_stock()
