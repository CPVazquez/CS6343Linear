import json
import unittest

from webserver import app

app.testing = True

class TestServer(unittest.TestCase):
    def test_correct_order(self):
        with app.test_client() as client:
            order = {'items': {'pizza' : 1, 'coke' : 2}}
            data = json.dumps(order)
            result = client.post('/', json=data)            
            self.assertEqual('200 OK', result.status)

    def test_incorrect_order(self):
        with app.test_client() as client:
            order = {'items': {'pizza' : 1, 'code' : -1}}
            data = json.dumps(order)
            result = client.post('/', json=data)
            self.assertEqual('400 BAD REQUEST', result.status)

            

