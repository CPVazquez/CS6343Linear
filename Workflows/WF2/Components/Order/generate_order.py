from faker import Faker
from queue import Queue
from threading import Thread
import json
import random
import requests
import sys
import uuid

fake = Faker('en_US')

class PizzaOrder:
    # Pizza Attributes
    payment_types = ['PayPal','Google Pay','Apple Pay','Visa','Mastercard','AMEX','Discover','Gift Card']
    crust_types = ['Thin','Traditional']
    sauce_types = ['Spicy','Traditional']
    cheese_amts = ['None','Light','Normal','Extra']
    topping_types = ['Pepperoni','Sausage','Beef','Onion','Chicken','Peppers','Olives','Bacon','Pineapple','Mushrooms']

    def __init__(self):
        self.order_id = str(uuid.uuid4())
        self.store_id = ""
        self.store_lat = 0
        self.store_lon = 0

    def choose_store(self):
        stores = [("7098813e-4624-462a-81a1-7e0e4e67631d", 32.8456, -96.9172),
                  ("5a2bb99f-88d2-4612-ac60-774aea9b8de4", 30.2672, -97.7431),
                  ("b18b3932-a4ef-485c-a182-8e67b04c208c", 29.7604, -95.3698)]
        store = random.randint(0, 2)
        self.store_id = stores[store][0]
        self.store_lat = round((stores[store][1] + random.uniform(-0.037, 0.037)), 6)
        self.store_lon = round((stores[store][2] + random.uniform(-0.0432, 0.0432)), 6)

    def add_more_pizzas(self, order_dict):
        n = round(random.triangular(1, max_pizzas, 1))  # Random int in range 1 <= n <= max_pizzas [mode is 1]
        # At this point, there's 1 pizza in pizzaList from generate_order()
        # Loop adds anywhere from 0 to max_pizzas-1 additional pizzas to pizzaList
        # (initial pizza) + (up to max_pizzas-1 additional pizzas) = max_pizzas
        for _ in range(1, n):
            new_pizza = {
                "crustType": self.crust_types[random.randint(0, 1)],
                "sauceType": self.sauce_types[random.randint(0, 1)],
                "cheeseAmt": self.cheese_amts[random.randint(0, 3)],
                "toppingList": random.sample(self.topping_types, random.randint(0, 9))
            }
            order_dict[self.order_id]["pizzaList"].append(new_pizza)
        return order_dict

    def generate_order(self):
        self.choose_store()
        # Construct the pizza order dict, with a single pizza in pizzaList
        order_dict = {
            self.order_id: {
                "storeId": self.store_id,
                "custName": fake.name(),
                "paymentToken": str(uuid.uuid4()),
                "paymentTokenType": self.payment_types[random.randint(0, 7)],
                "custLocation": {
                    "lat": self.store_lat,
                    "lon": self.store_lon
                },
                "pizzaList": [{
                    "crustType": self.crust_types[random.randint(0, 1)],
                    "sauceType": self.sauce_types[random.randint(0, 1)],
                    "cheeseAmt": self.cheese_amts[random.randint(0, 3)],
                    "toppingList": random.sample(self.topping_types, random.randint(0, 9))
                }]
            }
        }
        # Call add_more_pizzas(..) in return statement to randomly add additional pizzas
        # Upon return from add_more_pizzas(..), order_dict could contain up to max_pizzas
        return self.add_more_pizzas(order_dict)


def post_order(q):
    while True:
        order = q.get()
        order_dict = order.generate_order()
        #print(json.dumps(order_dict, indent=4))
        json_obj = json.dumps(order_dict)
        response = requests.post(url, json=json_obj)
        print(response)
        q.task_done()


if __name__ == "__main__":
    if len(sys.argv) != 5:
        raise ValueError('Incorrect command line arguments provided.')
    # python3 generate_order.py http://0.0.0.0:8080/order 1 10 20
    url = sys.argv[1]               # URL to send post requests
    num_threads = int(sys.argv[2])  # Number of threads to be started
    max_orders = int(sys.argv[3])   # Maximum orders to be generated
    max_pizzas = int(sys.argv[4])   # Maximum number of pizzas allowed per order

    q = Queue(max_orders)

    for _ in range(num_threads):
        t = Thread(target=post_order, args=(q,))
        t.daemon = True
        t.start()

    for _ in range(max_orders):
        pizza_order = PizzaOrder()
        q.put(pizza_order)

    q.join()    # Wait for all PizzaOrder objects to be processed from the queue
