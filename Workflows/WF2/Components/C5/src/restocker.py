from flask import Flask, request, Response
from cassandra.cluster import Cluster
import jsonschema
import json
import uuid

cluster = Cluster("10.0.1.3")
session = cluster.connect('pizza_grocery')
add_stock_prepared = session.prepare('UPDATE stock SET quantity = ?  WHERE store = ? AND itemName = ?')

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

    
    if restock_json != None :
        valid = verify_restock_order(restock_json)

        if valid :
            storeID = uuid.UUID(restock_dictionary["storeID"])
            for item_dict in restock_dictionary["restock-list"]:
                session.execute(add_stock_prepared, item_dict["quantity"], storeID, item_dict["item-name"])

    return Response(status=200, response="1" if valid else "0")
        


        