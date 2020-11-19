"""Order Verifier Component

Upon receiving a order request, this component validates the received order against the pizza-order jsonschema.
If the pizza-order is valid, then the order will be passed to the next component in the workflow.
If the pizza-order is invalid, then the request is rejected by this component.
"""

import copy
import json
import logging
import os
import uuid

import jsonschema
import requests
from quart import Quart, Response, request
from quart.utils import run_sync

__author__ = "Chris Scott"
__version__ = "3.0.0"
__maintainer__ = "Chris Scott"
__email__ = "cms190009@utdallas.edu"
__status__ = "Development"

# Create Quart app
app = Quart(__name__)

# Open jsonschema for pizza-order
with open("src/pizza-order.schema.json", "r") as pizza_schema:
    pizza_schema = json.loads(pizza_schema.read())

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

async def get_next_component(store_id):
    comp_list = workflows[store_id]["component-list"].copy()
    comp_list.remove("cass")
    next_comp_index = comp_list.index("order-verifier") + 1
    if next_comp_index >= len(comp_list):
        return None
    return comp_list[next_comp_index]


async def get_component_url(component, store_id):
    comp_name = component +\
        (str(workflows[store_id]["workflow-offset"]) if workflows[store_id]["method"] == "edge" else "")
    url = "http://" + comp_name + ":"
    if component == "delivery-assigner":
        url += "3000/order"
    elif component == "stock-analyzer":
        url += "4000/order"
    elif component == "restocker":
        url += "5000/order"
    elif component == "order-processor":
        url += "6000/order"
    return url


async def send_order_to_next_component(url, order):
    # send order to next component
    def request_post():
        return requests.post(url, json=json.dumps(order))
    
    r = await run_sync(request_post)()
    
    # form log message based on response status code from next component
    message = "Order from " + order["pizza-order"]["custName"] + " is valid."

    if r.status_code == 200:
        logging.info(message + " Order sent to next component.")
    else:
        logging.info(message + " Issue sending order to next component:")
        logging.info(r.text)
        
    return Response(status=r.status_code, response=r.text)


# validate pizza-order against schema
async def verify_order(data):
    global pizza_schema
    valid = True
    mess = None
    try:
        jsonschema.validate(instance=data, schema=pizza_schema)
    except Exception as inst:
        valid = False
        mess = inst.args[0]
    return valid, mess


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

# validate pizza-order request
@app.route('/order', methods=['POST'])
async def order_funct():
    logging.info("{:*^74}".format(" POST /order "))
    request_data = await request.get_json()
    order = json.loads(request_data)

    if order["pizza-order"]["storeId"] not in workflows:
        message = "Workflow does not exist. Request Rejected."
        logging.info(message)
        return Response(status=422, response=message)

    store_id = order["pizza-order"]["storeId"]
    cust_name = order["pizza-order"]["custName"]

    logging.info("Store " + store_id + ":\n    Verifying order from " + cust_name + ".")

    valid, mess = await verify_order(order["pizza-order"])

    if not valid:
        # failure of some kind, return error message
        error_mess = "Request rejected, pizza-order is malformed:  " + mess
        logging.info(error_mess)
        return Response(status=400, response=error_mess)

    order.update({"valid": valid})

    next_comp = await get_next_component(store_id)

    if next_comp is not None:
        # send order to next component in workflow
        next_comp_url = await get_component_url(next_comp, store_id)
        resp = await send_order_to_next_component(next_comp_url, order)
        if resp.status_code == 200:
            return resp
        else:
            order.update({"error": resp.text})
    else:
        logging.info("Order from " + cust_name + " is valid.")

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

    logging.info("Workflow created for {}".format(storeId))
    
    return Response(
        status=201, 
        response="Order Verifier deployed for {}\n".format(storeId)
    )    


# if the resource exists, update it
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
        response="Order Verifier updated for {}\n".format(storeId)
    )


# if the resource exists, remove it
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


# health check endpoint
@app.route('/health', methods=['GET'])
async def health_check():
    logging.info("{:*^74}".format(" GET /health "))
    return Response(status=200,response="healthy\n")
