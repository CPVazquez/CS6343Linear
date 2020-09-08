from flask import Flask, request, Response

import json

app = Flask(__name__)

def verify_order(order):
    items = order['items']
    for key in items:
        if items[key] < 0:
            return False
    return True

@app.route('/order', methods=['POST'])
def recieve_order():
    data = request.get_json()
    order = json.loads(data)
    if verify_order(order):
        # Initiate Workflow
        # Add order to DB
        return Response(response=json.dumps(order),
                status=200,
                mimetype='application/json')
    else:
        return Response(response=json.dumps(order),
                status=400,
                mimetype='application/json')

if __name__ == "__main__":
    app.run()
