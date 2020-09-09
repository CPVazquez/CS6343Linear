from flask import Flask, request, Response
import jsonschema
import json

app = Flask(__name__)

schema = None

def verify_order(order, schema):
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
    with open("./schema.json", "r") as schema:
        schema = json.loads(schema.read())
    order = json.loads(data)  
    return verify_order(order, schema)
