from flask import Flask, request, Response
import jsonschema
import json

app = Flask(__name__)

with open("src/schema.json", "r") as schema:
    schema = json.loads(schema.read())

def verify_order(order):
    global schema
    try:
        jsonschema.validate(instance=order, schema=schema)
    except:
        return Response(response=json.dumps(order),
                status=400,
                mimetype='application/json')

    return Response(response=json.dumps(order),
                status=200,
                mimetype='application/json')


@app.route('/order', methods=['POST'])
def main():
    data = request.get_json()
    nested_order = json.loads(data)
    for order in nested_order:
        return verify_order(nested_order[order])
