import json
import unittest
import jsonschema
from queue import Queue
from threading import Thread
from src.webserver import app

app.testing = True

class TestServer(unittest.TestCase):    
    def setUp(self):
        self.max_requests = 4
        

    def test_correct_order(self):        
        with app.test_client() as client:
            with open("./tests/correct-orders.json", "r") as correct_orders:                
                orders = json.loads(correct_orders.read())

            q = Queue(len(orders))

            def send_request():
                order = q.get()
                data = json.dumps(order)
                result = client.post('./order', json=data)
                print('ok')
                self.assertEqual('200 OK', result.status)
                q.task_done()

            for _ in range(self.max_requests):
                t = Thread(target=send_request)
                t.daemon = True
                t.start()

            for key in orders:
                q.put(orders[key])
            q.join()
                

    def test_incorrect_order(self):
        with app.test_client() as client:            
            with open("./tests/incorrect-orders.json", "r") as incorrect_orders:                
                orders = json.loads(incorrect_orders.read())

            q = Queue(len(orders))

            def send_request():
                order = q.get()
                data = json.dumps(order)
                result = client.post('./order', json=data)
                print('notok')
                self.assertEqual('400 BAD REQUEST', result.status)
                q.task_done()

            for _ in range(self.max_requests):
                t = Thread(target=send_request)
                t.daemon = True
                t.start()

            for key in orders:
                q.put(orders[key])
            q.join()
