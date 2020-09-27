from flask import Flask, request, Response
from cassandra.cluster import Cluster
import docker
import jsonschema
import json
import uuid
import time
import threading
import logging

# os.system("curl --unix-socket /var/run/docker.sock http:/v1.40/services/cass | python  -m json.tool >> /app/src/cassInfo.txt  ")

#cluster = Cluster(["10.0.0.46", "10.0.2.5"])
cluster = Cluster()
session = cluster.connect('pizza_grocery')
get_quantity = session.prepare('SELECT quantity FROM stock  WHERE storeID = ? AND itemName = ?')
add_stock_prepared = session.prepare('UPDATE stock SET quantity = ?  WHERE storeID = ? AND itemName = ?')
get_stores = session.prepare("SELECT storeID FROM stores")
get_items = session.prepare("SELECT name FROM items")


logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


app = Flask(__name__)


with open("src/restock-order.schema.json", "r") as schema:
    schema = json.loads(schema.read())


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


@app.route('/restock', methods=['POST'])
def restocker():

    valid = False
    restock_json = request.get_json(silent=True)
    response = Response(status=400, response="Restocking order ill formated.\nRejecting request.\nPlease correct formating")

    
    if restock_json != None :
        valid = verify_restock_order(restock_json)

        if valid :
            storeID = uuid.UUID(restock_json["storeID"])
            for item_dict in restock_json["restock-list"]:
                session.execute(add_stock_prepared, (item_dict["quantity"], storeID, item_dict["item-name"]))
            response = Response(status=200, response="Filled out the following restock order: \n" + json.dumps(restock_json))

    return response


@app.route('/health', methods=['POST'])
def health_check():
    return Response(status=200,response="healthy")


#scan the database for items that are out of stock or close to it VERSION A
def scan_out_of_stock():
    stores = session.execute(get_stores)
    for store in stores:
        items = session.execute(get_items)
        for item in items:
            quantity = session.execute(get_quantity, (store.storeid, item.name))
            quantity_row = quantity.one()
            if quantity_row != None:
                if quantity_row.quantity < 5.0 :
                    session.execute(add_stock_prepared, ( quantity_row.quantity + 20, store.storeid, item.name))
                    logging.debug(str(store.storeid) + ", " + item.name + " has " + str(quantity_row.quantity + 20.0))
    # threading.Timer(500, scan_out_of_stock).start()

scan_out_of_stock()