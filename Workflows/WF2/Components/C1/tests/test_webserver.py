import json
import unittest
import os

from queue import Queue
from threading import Thread
from src.order-verifier import app

app.testing = True

class TestServer(unittest.TestCase):
    def setUp(self):
        self.max_requests = 10

    def test_correct_order(self):
        with app.test_client() as client:
            q = Queue(len(os.listdir("tests/valid")))

            def send_request():
                order = q.get()
                data = json.dumps(order)
                result = client.post('order', json=data)
                self.assertEqual('200 OK', result.status)
                q.task_done()

            for _ in range(self.max_requests):
                t = Thread(target=send_request)
                t.daemon = True
                t.start()

            for entry in os.scandir("tests/valid"):
                if entry.path.endswith(".json"):
                    with open(entry.path, "r") as correct_order:
                        order = json.loads(correct_order.read())
                        q.put(order)

            q.join()


    def test_incorrect_order(self):
        with app.test_client() as client:
            q = Queue(len(os.listdir("tests/invalid")))

            def send_request():
                order = q.get()
                data = json.dumps(order)
                result = client.post('order', json=data)
                self.assertEqual('400 BAD REQUEST', result.status)
                q.task_done()

            for _ in range(self.max_requests):
                t = Thread(target=send_request)
                t.daemon = True
                t.start()

            for entry in os.scandir("tests/invalid"):
                if entry.path.endswith(".json"):
                    with open(entry.path, "r") as incorrect_order:
                        order = json.loads(incorrect_order.read())
                        q.put(order)

            q.join()
