from faker import Faker
from queue import Queue
from threading import Thread
import json
import random
import requests
import sys
import time
import uuid

__author__ = "Chris Scott"
__version__ = "1.0.0"
__maintainer__ = "Chris Scott"
__email__ = "christopher.scott@utdallas.edu"
__status__ = "Development"

fake = Faker('en_US')

class PizzaOrder:
    # Order Attribute Lists
    stores = [("7098813e-4624-462a-81a1-7e0e4e67631d", 32.8456, -96.9172),
              ("5a2bb99f-88d2-4612-ac60-774aea9b8de4", 30.2672, -97.7431),
              ("b18b3932-a4ef-485c-a182-8e67b04c208c", 29.7604, -95.3698)]
    payment_types = ['PayPal','Google Pay','Apple Pay','Visa','Mastercard','AMEX','Discover','Gift Card']
    crust_types = ['Thin','Traditional']
    sauce_types = ['Spicy','Traditional']
    cheese_amts = ['None','Light','Normal','Extra']
    topping_types = ['Pepperoni','Sausage','Beef','Onion','Chicken','Peppers','Olives','Bacon','Pineapple','Mushrooms']

    def __init__(self, store):
        self.store_id = self.stores[store][0]
        self.cust_name = fake.name()
        self.pay_token = str(uuid.uuid4())
        self.pay_type = self.payment_types[random.randint(0, 7)]
        self.cust_lat = round((self.stores[store][1] + random.uniform(-0.037, 0.037)), 6)
        self.cust_lon = round((self.stores[store][2] + random.uniform(-0.0432, 0.0432)), 6)

    def add_pizzas(self):
        # Generate a list of random pizzas in the range of 1 to max_pizzas
        pizza_list = []
        n = round(random.triangular(1, max_pizzas, 1))  # 1 <= n <= max_pizzas (mode is 1)
        for _ in range(n):
            pizza = {
                "crustType": self.crust_types[random.randint(0, 1)],
                "sauceType": self.sauce_types[random.randint(0, 1)],
                "cheeseAmt": self.cheese_amts[random.randint(0, 3)],
                "toppingList": random.sample(self.topping_types, random.randint(0, 9))
            }
            pizza_list.append(pizza)
        return pizza_list

    def generate_order(self):
        # Construct the pizza order dict, with a single pizza in pizzaList
        order_dict = {
            "storeId": self.store_id,
            "custName": self.cust_name,
            "paymentToken": self.pay_token,
            "paymentTokenType": self.pay_type,
            "custLocation": {
                "lat": self.cust_lat,
                "lon": self.cust_lon
            },
            "pizzaList": self.add_pizzas()
        }
        return order_dict


def post_order(q, url):
    while True:
        order = q.get()
        order_dict = order.generate_order()
        print("\nPizza Order Request:\n" + json.dumps(order_dict, indent=4))
        response = requests.post(url, json=json.dumps(order_dict))
        if response.status_code == 200:
            print("Request accepted - " + response.text)
        else:
            print("Request rejected - " + response.text)
        q.task_done()


if __name__ == "__main__":
    print("\n*** Pizza Order Generator Script - User Input Required ***\n")
    url = input("Enter Order Verifier URL: ")
    print()
    while True:
        try:
            num_threads = int(input("Enter the number of threads to start (min: 1, max: 10): "))
        except ValueError:
            print("Could not convert input data to integer. Please try again.")
        if (num_threads >= 1) & (num_threads <= 10):
            print()
            break
    print("0 - StoreID 7098813e-4624-462a-81a1-7e0e4e67631d")
    print("1 - StoreID 5a2bb99f-88d2-4612-ac60-774aea9b8de4")
    print("2 - StoreID b18b3932-a4ef-485c-a182-8e67b04c208c")
    while True:
        try:
            store = int(input("Select a store from above by entering 0, 1, or 2: "))
        except ValueError:
            print("Could not convert input data to integer. Please try again.")
        if (store >= 0) & (store <= 2):
            print()
            break
    while True:
        try:
            max_orders = int(input("Enter the number of pizza orders to generate (min: 1, max: 1000): "))
        except ValueError:
            print("Could not convert input data to integer. Please try again.")
        if (max_orders >= 1) & (max_orders <= 1000):
            print()
            break
    while True:
        try:
            max_pizzas = int(input("Enter the maximum number of pizzas per order (min: 1, max: 20): "))
        except ValueError:
            print("Could not convert input data to integer. Please try again.")
        if (max_pizzas >= 1) & (max_pizzas <= 20):
            print()
            break
    print("\n*** Pizza Order Generator Script - Generating Orders ***\n")

    q = Queue(max_orders)

    for _ in range(num_threads):
        t = Thread(target=post_order, args=(q,url))
        t.daemon = True
        t.start()

    for _ in range(max_orders):
        pizza_order = PizzaOrder(store)
        q.put(pizza_order)
        time.sleep(3)

    q.join()    # Wait for all PizzaOrder objects to be processed from the queue
