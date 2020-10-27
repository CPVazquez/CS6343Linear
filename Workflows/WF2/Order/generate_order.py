import json
import random
import sys
import threading
import time
import uuid
from datetime import datetime, timedelta
from queue import Queue

import requests
from faker import Faker

__author__ = "Chris Scott"
__version__ = "2.0.0"
__maintainer__ = "Chris Scott"
__email__ = "christopher.scott@utdallas.edu"
__status__ = "Development"

fake = Faker('en_US')

cluster = "cluster1-1.utdallas.edu"


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

    def __init__(self, store, order_date, max_pizzas):
        self.store_id = self.stores[store][0]
        self.cust_name = fake.name()
        self.pay_token = str(uuid.uuid4())
        self.pay_type = self.payment_types[random.randint(0, 7)]
        self.cust_lat = round((self.stores[store][1] + random.uniform(-0.037, 0.037)), 6)
        self.cust_lon = round((self.stores[store][2] + random.uniform(-0.0432, 0.0432)), 6)
        self.order_date = order_date
        self.max_pizzas = max_pizzas

    def add_pizzas(self):
        # Generate a list of random pizzas in the range of 1 to max_pizzas
        pizza_list = []
        n = round(random.triangular(1, self.max_pizzas, 1))  # 1 <= n <= max_pizzas (mode is 1)
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
            "orderDate": self.order_date,
            "pizzaList": self.add_pizzas()
        }
        return order_dict


def request_order(q, url_list):
    while True:
        order = q.get()
        order_dict = order.generate_order()
        print("\nPizza Order Request:\n" + json.dumps(order_dict, indent=4))
        for url in url_list:
            response = requests.post(url, json=json.dumps(order_dict))
            if (response.status_code == 201) or (response.status_code == 200):
                print("Request Accepted - {} {}".format(str(response.status_code), response.text))
            else:
                print("Request Rejected - {} {}".format(str(response.status_code), response.text))
        q.task_done()      


if __name__ == "__main__":
    print("\n*** Pizza Order Generator Script - User Input Required ***\n")

    print("0 - StoreID 7098813e-4624-462a-81a1-7e0e4e67631d")
    print("1 - StoreID 5a2bb99f-88d2-4612-ac60-774aea9b8de4")
    print("2 - StoreID b18b3932-a4ef-485c-a182-8e67b04c208c")
    while True:
        try:
            store = int(input("Select a Store Workflow by entering 0, 1, or 2: "))
        except ValueError:
            print("Could not convert input data to integer. Please try again.")
        if (store >= 0) & (store <= 2):
            print()
            break
        else:
            print("Input data outside of valid input range. Please try again.")

    url_list = list()
    while True:
        result = input("Is Order Verifier included in this Workflow (y/n)? ")
        result = result.lower()
        if result == "y":
            url_list.append("http://"+cluster+":1000/order")
            print()
            break
        elif result == "n":
            print()
            break
        else:
            print("Please respond 'y' for yes or 'n' for no. Please try again.")
            continue
    if result == "n":
        while True:
            result = input("Is Delivery Assigner included in this Workflow (y/n)? ")
            result = result.lower()
            if result == "y":
                url_list.append("http://"+cluster+":3000/assign-entity")
                print()
                break
            elif result == "n":
                print()
                break
            else:
                print("Please respond 'y' for yes or 'n' for no. Please try again.")
                continue
        while True:
            result = input("Is Auto-Restocker included in this Workflow (y/n)? ")
            result = result.lower()
            if result == "y":
                url_list.append("http://"+cluster+":4000/auto-restock")
                print()
                break
            elif result == "n":
                print()
                break
            else:
                print("Please respond 'y' for yes or 'n' for no. Please try again.")
                continue

    while True:
        valid = True
        result = input("Please enter the start date in format MM-DD-YYYY: ")
        try:
            month, day, year = result.split("-")
            start_date = datetime(int(year), int(month), int(day))
        except:
            valid = False
            print("Invalid date. Please try again.")
        if valid:
            print()
            break

    while True:
        try:
            num_days = int(input("Enter the number of days to generate orders (min: 1, max: 365): "))
        except ValueError:
            print("Could not convert input data to integer. Please try again.")
        if (num_days >= 1) & (num_days <= 365):
            print()
            break
        else:
            print("Input data outside of valid input range. Please try again.")

    while True:
        try:
            orders_per_day = int(input("Enter the number of orders to generate per day (min: 1, max: 1000): "))
        except ValueError:
            print("Could not convert input data to integer. Please try again.")
        if (orders_per_day >= 1) & (orders_per_day <= 1000):
            print()
            break
        else:
            print("Input data outside of valid input range. Please try again.")

    while True:
        try:
            max_pizzas = int(input("Enter the maximum number of pizzas per order (min: 1, max: 20): "))
        except ValueError:
            print("Could not convert input data to integer. Please try again.")
        if (max_pizzas >= 1) & (max_pizzas <= 20):
            print()
            break
        else:
            print("Input data outside of valid input range. Please try again.")

    print("\n*** Pizza Order Generator Script - Generating Orders ***")

    total_orders = num_days * orders_per_day

    q = Queue(total_orders)

    t = threading.Thread(target=request_order, args=(q,url_list))
    t.daemon = True
    t.start()

    offset = -1
    for i in range(total_orders):
        if (i % orders_per_day) == 0:
            offset += 1
        date_str = (start_date + timedelta(days=offset)).isoformat()
        pizza_order = PizzaOrder(store, date_str, max_pizzas)
        q.put(pizza_order)
        time.sleep(1)
        
    q.join()    # Wait for all PizzaOrder objects to be processed from the queue
