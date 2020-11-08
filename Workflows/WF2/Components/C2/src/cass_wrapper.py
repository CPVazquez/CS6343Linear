""" Cass_wrapper

when recieveing a workflow setup request checks to see if the store already
exists in the database. If it does, then it just resets stock. If it doesn't,
then preforms the necessary inserts.
"""
import uuid
import random
import json
from time import sleep

import logging
import jsonschema
from cassandra.cluster import Cluster
from flask import Flask, request, Response

__author__ = "Carla Vazquez"
__version__ = "1.0.0"
__maintainer__ = "Carla Vazquez"
__email__ = "cpv150030@utdallas.edu"
__status__ = "Development"

# Connect to Cassandra service
session = None
stores = 0
ready = False

# try connecting to cassandra
while True:
    try:
        cluster = Cluster()
        session = cluster.connect('pizza_grocery')
    except Exception:
        sleep(5)
    else:
        logging.info("Connected to Cass")
        break

# try preparring the statements
while True:
    try:
        storeCheck = session.prepare("SELECT * FROM stores WHERE storeID=?")
        storeInsert = session.prepare("INSERT INTO stores \
            (storeID, latitude, longitude, sellsPizza) VALUES(?, ?, ?, ?)")
        insertIngredient = session.prepare("INSERT INTO stock \
            (storeID, itemName, quantity) VALUES (?, ?, ?)")
        update_stock_prepared = session.prepare('\
            UPDATE stock \
            SET quantity=? \
            WHERE storeID=? AND itemName=?\
        ')
        insertEntity = session.prepare("INSERT INTO deliveryEntitiesByStore \
            (storeID, name, latitude, longitude, status, onDelivery) VALUES \
                (?, ?, ?, ?, ?, ?)")
    except Exception:
        sleep(5)
    else:
        logging.info("prepared statements loaded")
        ready = True
        break

items = ['Dough', 'SpicySauce', 'TraditionalSauce', 'Cheese',
         'Pepperoni', 'Sausage', 'Beef', 'Onion', 'Chicken', 'Peppers',
         'Olives', 'Bacon', 'Pineapple', 'Mushrooms']

# create workflow dictionalry
workflows = dict()

# Create Flask app
app = Flask(__name__)

# Open jsonschema for workflow-request
with open("src/workflow-request.schema.json", "r") as workflow_schema:
    workflow_schema = json.loads(workflow_schema.read())


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


# when recieveing a workflow request
@app.route("/workflow-requests/<storeId>", methods=['PUT'])
def setup_workflow(storeId):
    global session, stores

    logging.info("PUT /workflow-requests/" + storeId)
    data = json.loads(request.get_json())
    valid, mess = verify_workflow(data)

    # check if request is valid
    if not valid:
        logging.info("workflow-request ill formatted")
        return Response(
            status=400, response="workflow-request ill formatted\n" + mess)

    if storeId in workflows:
        logging.info("Workflow " + storeId + " already exists")
        return Response(
            status=409, response="Workflow " + storeId + " already exists\n")

    if not ("cass" in data["component-list"]):
        logging.info(
            "workflow-request rejected, cass is a required workflow component")
        return Response(
            status=422,
            response="workflow-request rejected," +
                     " cass is a required workflow component\n")

    # if it is, insert it into the workflow dictionary
    workflows[storeId] = data

    # convert storeId from string to UUID
    storeUUID = uuid.UUID(storeId)

    # check if the store already exists in the database
    storeExists = False
    rows = session.execute(storeCheck, (storeUUID, ))
    for row in rows:
        storeExists = True
        break

    # if it doesn't
    if not storeExists:
        stores += 1

        # pick a location
        x = random.uniform(30.0, 33.0)
        y = random.uniform(-97.0, -94.0)

        # insert store
        session.execute(storeInsert, (storeUUID, x, y, True))
        for item in items:  # insert stock
            session.execute(insertIngredient, (storeUUID, item, 100))
        for i in range(1, 6):  # insert delievery entities
            session.execute(
                insertEntity,
                (storeUUID, "de"+str(stores)+str(i), x, y, "AVAILABLE", False))
    else:  # if it does
        for item in items:  # update stock
            session.execute(update_stock_prepared, (100, storeUUID, item))

    return Response(status=201, response="store entered into the database")


# when updating a request
@app.route("/workflow-update/<storeId>", methods=['PUT'])
def update_workflow(storeId):
    logging.info("PUT /workflow-update/" + storeId)
    data = json.loads(request.get_json())
    valid, mess = verify_workflow(data)

    # check if the request is valid
    if not valid:
        logging.info("workflow-request ill formatted")
        return Response(
            status=400, response="workflow-request ill formatted\n" + mess)

    if not ("cass" in data["component-list"]):
        logging.info(
            "workflow-request rejected, cass is a required workflow component")
        return Response(
            status=422,
            response="workflow-request rejected," +
                     " cass is a required workflow component\n")

    # update workflow dictionary
    workflows[storeId] = data

    logging.info("Workflow updated for {}\n".format(storeId))

    return Response(
        status=200,
        response="Order Verifier updated for {}\n".format(storeId))


# remove workflow if it exists
@app.route("/workflow-requests/<storeId>", methods=["DELETE"])
def teardown_workflow(storeId):
    logging.info("DELETE /workflow-requests/" + storeId)
    if not (storeId in workflows):
        return Response(
            status=404,
            response="Workflow doesn't exist. Nothing to teardown.\n")
    else:
        del workflows[storeId]
        return Response(status=204)


# get the workflow from the component
@app.route("/workflow-requests/<storeId>", methods=["GET"])
def retrieve_workflow(storeId):
    logging.info("GET /workflow-requests/" + storeId)
    if not (storeId in workflows):
        return Response(
            status=404,
            response="Workflow doesn't exist. Nothing to retrieve.\n")
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
    if ready:
        return Response(status=200, response="healthy\n")
    else:
        return Response(status=400, response="unhealthy\n")


if __name__ == "__main__":
    app.run("0.0.0.0", 2000, False)
