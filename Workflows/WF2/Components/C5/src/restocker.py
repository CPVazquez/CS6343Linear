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
    except:
        count += 1
        if count <= 5:
            time.sleep(5)
        else:
            exit()
    else:
        break

# set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

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
def verify_restock_order(data):
    global restock_schema
    valid = True
    mess = None
    try:
        jsonschema.validate(instance=data, schema=restock_schema)
    except Exception as inst:
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
        message = "restock-order is valid, but {} doesn't exist".format(store_id)
        logging.info(message)
        return Response(status=422, response=message)

    if restock_dict != None:
        valid, mess = verify_restock_order(restock_dict)
        if valid:
            try: 
                storeID = uuid.UUID(restock_dict["storeID"])
                for item_dict in restock_dict["restock-list"]:
                    session.execute(add_stock_prepared, (item_dict["quantity"], storeID, item_dict["item-name"]))
                message = "Restock successful:\n" + json.dumps(restock_dict)
                logging.info(message)
                response = Response(status=200, response=message)
            except ValueError:
                logging.info("Exception: badly formed hexadecimal UUID string")
                response = Response(status=400, response="restock-order 'storeID' is not in valid UUID format")
        else:
            logging.info("restock-order request ill formatted")
            response = Response(status=400, response="restock-order ill formated\n"+mess)

    logging.info(response)
    return response


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
        return Response(status=422, response="Update rejected, cass is a required workflow component\n")

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
    #if app.config["ENV"] == "production": 
    threading.Timer(300, scan_out_of_stock).start()

# calls the scan_out_of stock function for the first time
#scan_out_of_stock()
