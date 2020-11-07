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
            print("URL: {}".format(url))
            print("Response: {}, {}".format(response.status_code, response.text))
        q.task_done()


if __name__ == "__main__":
    cluster = "cluster1-1.utdallas.edu"
    port_dict = {
        "order-verifier": 1000,
        "delivery-assigner": 3000,
        "auto-restocker": 4000
    }

    print("\n*** Pizza Order Generator Script - User Input Required ***\n")

    # User selection of store
    print("Which store are you generating a workflow for? \n" +
          "\tA. 7098813e-4624-462a-81a1-7e0e4e67631d\n" +
          "\tB. 5a2bb99f-88d2-4612-ac60-774aea9b8de4\n" +
          "\tC. b18b3932-a4ef-485c-a182-8e67b04c208c")
    store_select = input("Pick a store (A-C): ")
    
    while (store_select != "A") and (store_select != "B") and (store_select != "C"):
        store_select = input("Invalid input. Pick A-C: ")

    if store_select == "A":
        store = 0
    elif store_select == "B":
        store = 1
    else:
        store = 2

    # Deployment method selection
    deployment = input("\nWhat is the deployment method (persistent or edge)? ")

    while (deployment != "persistent") and (deployment != "edge"):
        deployment = input("Invalid input. Type persistent or edge: ")

    if deployment == "edge":
        wkf_offset = input("Please enter the workflow-offset (1-3): ")
        while (wkf_offset != "1") and (wkf_offset != "2") and (wkf_offset != "3"):
            wkf_offset = input("Invalid input. Type 1-3: ")
        for comp in port_dict:
            port_dict[comp] += int(wkf_offset)

    # Component URL(s)
    url_list = list()
    result = input("\nIs Order Verifier included in this Workflow (y/n)? ")

    while (result != "y") and (result != "n"):
        result = input("Invalid input. Type y or n: ") 

    if result == "y":
            url_list.append("http://" + cluster + ":" + str(port_dict["order-verifier"]) + "/order")
    else:
        result = input("\nIs Delivery Assigner included in this Workflow (y/n)? ")
        while (result != "y") and (result != "n"):
            result = input("Invalid input. Type y or n: ") 
        if result == "y":
            url_list.append("http://" + cluster + ":" + str(port_dict["delivery-assigner"]) + "/order")

        result = input("\nIs Auto-Restocker included in this Workflow (y/n)? ")
        while (result != "y") and (result != "n"):
            result = input("Invalid input. Type y or n: ")
        if result == "y":
            url_list.append("http://" + cluster + ":" + str(port_dict["auto-restocker"]) + "/order")

    # Start date selection
    while True:
        result = input("\nPlease enter the start date in format MM-DD-YYYY: ")
        try:
            month, day, year = result.split("-")
            start_date = datetime(int(year), int(month), int(day))
            break
        except:
            print("Invalid input. Please try again.")

    # Days to generate orders
    while True:
        try:
            num_days = int(input("\nEnter the number of days to generate orders (min: 1, max: 365): "))
            if 1 <= num_days <= 365:
                break
            else:
                continue
        except:
            print("Invalid input. Please try again.")

    # Order generated per day
    while True:
        try:
            orders_per_day = int(input("\nEnter the number of orders to generate per day (min: 1, max: 60): "))
            if 1 <= orders_per_day <= 60:
                break
            else:
                continue
        except:
            print("Invalid input. Please try again.")

    # Max pizzas per order
    while True:
        try:
            max_pizzas = int(input("\nEnter the maximum number of pizzas per order (min: 1, max: 20): "))
            if 1 <= max_pizzas <= 20:
                break
            else:
                continue
        except:
            print("Invalid input. Please try again.")

    print("\n*** Pizza Order Generator Script - Generating Orders ***")

    total_orders = num_days * orders_per_day
    q = Queue(total_orders)

    t = threading.Thread(target=request_order, args=(q,url_list))
    t.daemon = True
    t.start()

    date_offset = 0
    for i in range(total_orders):
        if (i != 0) and ((i % orders_per_day) == 0):
            date_offset += 1
            time.sleep(60 - orders_per_day)
        date_str = (start_date + timedelta(days=date_offset)).isoformat()
        pizza_order = PizzaOrder(store, date_str, max_pizzas)
        q.put(pizza_order)
        time.sleep(1)
        
    q.join()    # Wait for all PizzaOrder objects to be processed from the queue
