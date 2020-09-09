import json
import unittest
import jsonschema

from webserver import app

app.testing = True

class TestServer(unittest.TestCase):    
    def test_correct_order(self):
        with app.test_client() as client:
            with open("./correct-orders.json", "r") as correct_orders:                
                orders = json.loads(correct_orders.read())
            for key in orders:
                order = orders[key]
                data = json.dumps(order)
                result = client.post('/order', json=data)            
                self.assertEqual('200 OK', result.status)

    def test_incorrect_order(self):
        with app.test_client() as client:            
            with open("./incorrect-orders.json", "r") as incorrect_orders:
                orders = json.loads(incorrect_orders.read())
            for key in orders:
                order = orders[key]
                data = json.dumps(order)
                result = client.post('/order', json=data)            
                self.assertEqual('400 BAD REQUEST', result.status)     

