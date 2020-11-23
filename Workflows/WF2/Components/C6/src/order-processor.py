"""The Order Processor Component for this Cloud Computing project.

Upon receiving a pizza-order request, Order Processor assigns the pizza-order request 
an orderID, calculates the cost of each pizza contained in the pizza-order request, 
calculates the total cost of the pizza-order, and inserts the pizza-order information 
into the database. The request is then sent to the next component in the workflow, if 
one exists.
"""

import json
import logging
import os
import time
import uuid
from datetime import datetime

import jsonschema
import requests
from cassandra.cluster import Cluster
from quart import Quart, Response, request
from quart.utils import run_sync

__author__ = "Chris Scott"
__version__ = "1.0.0"
__maintainer__ = "Chris Scott"
__email__ = "cms190009@utdallas.edu"
__status__ = "Development"

# Connect to Cassandra service
cass_IP = os.environ["CASS_DB"]
cluster = Cluster([cass_IP])
session = cluster.connect('pizza_grocery')

# Cassandra prepared statements
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
        time.sleep(5)
    else:
        break

# Create Quart app
app = Quart(__name__)

# Open jsonschema for workflow-request
with open("src/workflow-request.schema.json", "r") as workflow_schema:
    workflow_schema = json.loads(workflow_schema.read())

# Logging
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logging.getLogger('requests').setLevel(logging.WARNING)
logging.getLogger('quart.app').setLevel(logging.WARNING)
logging.getLogger('quart.serving').setLevel(logging.WARNING)

# Global workflows dict
workflows = dict()


###############################################################################
#                           Helper Functions
###############################################################################

# Calculate pizza price based on ingredients
async def calc_pizza_cost(ingredient_set):
    cost = 0.0

    for ingredient in ingredient_set:

        def select_items():
            return session.execute(select_items_prepared, (ingredient[0],))

        result = await run_sync(select_items)()

        for (name, price) in result:
            cost += price * ingredient[1] 

    return cost


# Insert an order's pizza(s) into 'pizzas' table
async def insert_pizzas(pizza_list):
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
        
        cost = await calc_pizza_cost(ingredient_set)

        def insert_pizza():
            session.execute(insert_pizzas_prepared, (pizza_uuid, ingredient_set, cost))

        await run_sync(insert_pizza)()
    
    return pizza_uuid_set


# Insert order info into DB
async def create_order(order_dict):
    order_uuid = uuid.UUID(order_dict["orderId"])
    store_uuid = uuid.UUID(order_dict["storeId"])
    pay_uuid = uuid.UUID(order_dict["paymentToken"])
    cust_name = order_dict["custName"]
    cust_lat = order_dict["custLocation"]["lat"]
    cust_lon = order_dict["custLocation"]["lon"]
    placed_at = datetime.strptime(order_dict["orderDate"], '%Y-%m-%dT%H:%M:%S')

    valid = True
    mess = None

    # Insert customer information into 'customers' table
    def insert_customers():
        session.execute(insert_customers_prepared, (cust_name, cust_lat, cust_lon))

    try:
        await run_sync(insert_customers)()
    except Exception as inst:
        valid = False
        mess = inst.args[0]
        return valid, mess

    # Insert order payment information into 'payments' table
    def insert_payments():
        session.execute(insert_payments_prepared, (pay_uuid, order_dict["paymentTokenType"]))

    try:
        await run_sync(insert_payments)()
    except Exception as inst:
        valid = False
        mess = inst.args[0]
        return valid, mess

    # Insert the ordered pizzas into 'pizzas' table
    try:
        pizza_uuid_set = await insert_pizzas(order_dict["pizzaList"])
    except Exception as inst:
        valid = False
        mess = inst.args[0]
        return valid, mess

    # Insert order into 'orderTable' table
    def insert_order_table():
        session.execute(
            insert_order_prepared, 
            (order_uuid, store_uuid, cust_name, "", pizza_uuid_set, None, pay_uuid, placed_at, True, -1)
        )

    try:
        await run_sync(insert_order_table)()
    except Exception as inst:
        valid = False
        mess = inst.args[0]
        return valid, mess
    
    # Insert order into 'orderByStore' table
    def insert_order_by_store():
        session.execute(insert_order_by_store_prepared, (store_uuid, placed_at, order_uuid))

    try:
        await run_sync(insert_order_by_store)()
    except Exception as inst:
        valid = False
        mess = inst.args[0]
        return valid, mess

    # Insert order into 'orderByCustomer' table
    def insert_order_by_customer():
        session.execute(insert_order_by_customer_prepared, (cust_name, placed_at, order_uuid))

    try:
        await run_sync(insert_order_by_customer)()
    except Exception as inst:
        valid = False
        mess = inst.args[0]
        return valid, mess
    
    return valid, mess


async def get_next_component(store_id):
    comp_list = workflows[store_id]["component-list"].copy()
    comp_list.remove("cass")
    next_comp_index = comp_list.index("order-processor") + 1
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
    elif component == "restocker":
        url += "5000/order"
    return url


async def send_order_to_next_component(url, order):
    # send order to next component
    def request_post():
        return requests.post(url, json=json.dumps(order))
    
    r = await run_sync(request_post)()

    return Response(status=r.status_code, response=r.text)


# validate workflow-request against schema
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

# if pizza-order is valid, try to create it
@app.route('/order', methods=['POST'])
async def process_order():
    logging.info("{:*^74}".format(" POST /order "))
    start = time.time()
    request_data = await request.get_json()
    order = json.loads(request_data)

    if order["pizza-order"]["storeId"] not in workflows:
        message = "Workflow does not exist. Request Rejected."
        logging.info(message)
        return Response(status=422, response=message)

    order["pizza-order"]["orderId"] = str(uuid.uuid4())
    order_id = order["pizza-order"]["orderId"]
    store_id = order["pizza-order"]["storeId"]
    cust_name = order["pizza-order"]["custName"]

    logging.info("Store " + store_id + ":")
    logging.info("Processing order " + order_id + " for " + cust_name + ".")

    valid, mess = await create_order(order["pizza-order"])

    if not valid:
        # failure of some kind, return error message
        error_mess = "Request rejected, order processing failed:  " + mess
        logging.info(error_mess)
        return Response(status=400, response=error_mess)

    order.update({"processor": "accepted"})

    log_mess = "Order from " + cust_name + " is processed."

    next_comp = await get_next_component(store_id)

    end = time.time() - start

    if next_comp is not None:
        # send order to next component in workflow
        next_comp_url = await get_component_url(next_comp, store_id)
        resp = await send_order_to_next_component(next_comp_url, order)
        if resp.status_code == 200:
            # successful response from next component, return same response
            resp_dict = json.loads(resp.text)
            resp_dict["order-processor_execution_time"] = end
            logging.info(log_mess + " Order sent to next component.")
            return Response(status=resp.status_code, response=json.dumps(resp_dict))
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

    order["order-processor_execution_time"] = end

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
    
    if not ("cass" in data["component-list"]):
        logging.info("workflow-request rejected, cass is a required workflow component")
        return Response(
            status=422, 
            response="workflow-request rejected, cass is a required workflow component\n"
        )

    workflows[storeId] = data

    logging.info("Workflow started for {}".format(storeId))
    
    return Response(
        status=201, 
        response="Order Processor deployed for {}\n".format(storeId)
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
        logging.info("workflow-request rejected, cass is a required workflow component")
        return Response(
            status=422, 
            response="workflow-request rejected, cass is a required workflow component\n"
        )

    workflows[storeId] = data

    logging.info("Workflow updated for {}".format(storeId))

    return Response(
        status=200, 
        response="Order Processor updated for {}\n".format(storeId)
    )


# if the recource exists, remove it
@app.route("/workflow-requests/<storeId>", methods=["DELETE"])
async def teardown_workflow(storeId):
    logging.info("{:*^74}".format(" DELETE /workflow-requests/" + storeId + " "))
    if not (storeId in workflows):
        return Response(
            status=404, 
            response="Workflow doesn't exist. Nothing to teardown.\n"
        )
    else:
        del workflows[storeId]
        return Response(status=204, response="")


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


# Health check endpoint
@app.route('/health', methods=['GET'])
async def health_check():
    logging.info("{:*^74}".format(" GET /health "))
    return Response(status=200,response="healthy\n")
