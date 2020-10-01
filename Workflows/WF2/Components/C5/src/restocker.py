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
__version__ = "1.0.0"
__maintainer__ = "Carla Vazquez"
__email__ = "cpv150030@utdallas.edu"
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


# open the jsonschema
with open("src/restock-order.schema.json", "r") as schema:
    schema = json.loads(schema.read())


# checks the recieved restock-order against the jsonschema
def verify_restock_order(order):
    global schema
    valid = True
    try:
        jsonschema.validate(instance=order, schema=schema)
    except Exception as inst:
        print(type(inst))    # the exception instance
        print(inst.args)     # arguments stored in .args
        print(inst)          # __str__ allows args to be printed directly,
        print(order)
        valid = False
    return valid

# the restock endpoint
@app.route('/restock', methods=['POST'])
def restocker():

    valid = False
    restock_json = request.get_json(silent=True)
    response = Response(status=400, response="Restocking order ill formated.\
        \nRejecting request.\nPlease correct formating")

    if restock_json != None :
        valid = verify_restock_order(restock_json)

        if valid :
            storeID = uuid.UUID(restock_json["storeID"])
            for item_dict in restock_json["restock-list"]:
                session.execute(add_stock_prepared, (item_dict["quantity"], storeID, item_dict["item-name"]))
            response = Response(status=200, response="Filled out the following \
                restock order: \n" + json.dumps(restock_json))

    logging.debug(response)
    return response

# the health endpoint, so that users can verify that the server
# is up and running
@app.route('/health', methods=['POST'])
def health_check():
    return Response(status=200,response="healthy\n")


#scan the database for items that are out of stock or close to it
def scan_out_of_stock():
    # gets a list of all stores
    stores = session.execute(get_stores)
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
    threading.Timer(300, scan_out_of_stock).start()

# calls the scan_out_of stock function for the first time
scan_out_of_stock()
