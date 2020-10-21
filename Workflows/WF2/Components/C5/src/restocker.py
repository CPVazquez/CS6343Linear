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

__author__ = "Carla Vazquez"
__version__ = "2.0.0"
__maintainer__ = "Chris Scott"
__email__ = "cms190009@utdallas.edu"
__status__ = "Development"

# Connect to casandra service
cass_IP = os.environ["CASS_DB"]
cluster = Cluster([cass_IP])
session = cluster.connect('pizza_grocery')

# prepared statements
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

# set up logging
logging.basicConfig(level=logging.DEBUG, 
    format='%(asctime)s - %(levelname)s - %(message)s')

# create flask app
app = Flask(__name__)

# open the restock jsonschema
with open("src/restock-order.schema.json", "r") as restock_schema:
    restock_schema = json.loads(restock_schema.read())

# Open jsonschema for workflow-request
with open("src/workflow-request.schema.json", "r") as workflow_schema:
    workflow_schema = json.loads(workflow_schema.read())

# Global workflows dict
workflows = dict()


# checks the recieved restock-order against the jsonschema
def verify_restock_order(order):
    global restock_schema
    valid = True
    mess = None
    try:
        jsonschema.validate(instance=order, schema=restock_schema)
    except Exception as inst:
        logging.debug(type(inst))    # the exception instance
        logging.debug(inst.args[0])          # __str__ allows args to be loggin.debuged directly,
        logging.debug(order)
        valid = False
        mess = inst.args[0]
    return valid, mess


# the restock endpoint
@app.route('/restock', methods=['POST'])
def restocker():
    valid = False
    restock_dict = json.loads(request.get_json())
    
    store_id = restock_dict["storeID"]
    if store_id not in workflows:
        logging.debug("Restock request is valid, but Workflow does not exist: " + store_id)
        return Response(status=422, response="Restock request is valid, but Workflow does not exist.")

    if restock_dict != None :
        valid, mess = verify_restock_order(restock_dict)

        if valid :
            try: 
                storeID = uuid.UUID(restock_dict["storeID"])
                for item_dict in restock_dict["restock-list"]:
                    session.execute(add_stock_prepared, (item_dict["quantity"],
                        storeID, item_dict["item-name"]))
                response = Response(status=200, response="Filled out the following restock order:\n" + json.dumps(restock_dict))
            except ValueError:
                logging.debug("Exception: badly formed hexadecimal UUID\
                    string")
                response = Response(status=400, response="Restocking order ill formated.\n'storeID' is not in valid UUID format")
        else:
            response = Response(status=400, response="Restocking order ill formated.\n"+mess)

    logging.debug(response)
    return response


# the health endpoint, so that users can verify that the server is up and running
@app.route('/health', methods=['GET'])
def health_check():
    return Response(status=200,response="healthy\n")


def verify_workflow(data):
    global workflow_schema
    valid = True
    mess = None
    try:
        jsonschema.validate(instance=data, schema=workflow_schema)
    except Exception as inst:
        logging.debug("Workflow request rejected, failed validation:\n" + json.dumps(data, indent=4))
        valid = False
        mess = inst.args[0]
    return valid, mess


@app.route("/workflow-requests/<storeId>", methods=['PUT'])
def setup_workflow(storeId):
    if storeId in workflows:
        logging.debug("Workflow " + storeId + " already exists")
        return Response(status=409, response="Workflow " + storeId + " already exists\n")

    data = json.loads(request.get_json())
    logging.debug("workflow-requests data: " + json.dumps(data, indent=4))
    valid, mess = verify_workflow(data)
    if not valid:
        return Response(status=400, response="workflow-request ill formatted\n" + mess)

    workflows[storeId] = data

    logging.debug("Workflow Deployed: Restocker started for Store " + storeId)

    return Response(status=201, response="Restocker deployed for {}\n".format(storeId))    


@app.route("/workflow-requests/<storeId>", methods=["DELETE"])
def teardown_workflow(storeId):
    if storeId not in workflows:
        return Response(status=404, response="Workflow doesn't exist. Nothing to teardown.\n")

    del workflows[storeId]

    logging.debug("Workflow Torn Down: Restocker stopped for Store " + storeId)

    return Response(status=204)


# retrieve the specified resource, if it exists
@app.route("/workflow-requests/<storeId>", methods=["GET"])
def retrieve_workflow(storeId):
    logging.debug("GET /workflow-requests/" + storeId)
    if not (storeId in workflows):
        return Response(status=404, response="Workflow doesn't exist. Nothing to retrieve")
    else:
        return Response(status=200, response=json.dumps(workflows[storeId]))


# retrieve all resources
@app.route("/workflow-requests", methods=["GET"])
def retrieve_workflows():
    logging.debug("GET /workflow-requests")
    return Response(status=200, response=json.dumps(workflows))


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
                    session.execute(add_stock_prepared, ( quantity_row.quantity + 20, store.storeid, item.name))
                    logging.debug(str(store.storeid) + ", " + item.name +
                        " has " + str(quantity_row.quantity + 20.0))
    if app.config["ENV"] == "production": 
        threading.Timer(300, scan_out_of_stock).start()

# calls the scan_out_of stock function for the first time
scan_out_of_stock()
