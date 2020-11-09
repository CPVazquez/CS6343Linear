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
__version__ = "3.0.0"
__maintainer__ = "Chris Scott"
__email__ = "christopher.scott@utdallas.edu"
__status__ = "Development"

fake = Faker('en_US')

cluster_url = "http://cluster1-1.utdallas.edu"
port_dict = {
    "order-verifier": 1000,
    "delivery-assigner": 3000,
    "cass": 2000,
    "predictor": 4000,
    "auto-restocker": 4000,
    "restocker": 5000,
    "order-processor": 6000
}


class PizzaOrder:
    # Order Attribute Lists
    payment_types = ['PayPal','Google Pay','Apple Pay','Visa','Mastercard','AMEX','Discover','Gift Card']
    crust_types = ['Thin','Traditional']
    sauce_types = ['Spicy','Traditional']
    cheese_amts = ['None','Light','Normal','Extra']
    topping_types = ['Pepperoni','Sausage','Beef','Onion','Chicken','Peppers','Olives','Bacon','Pineapple','Mushrooms']

    def __init__(self, store_id, store_lat, store_lon, order_date, max_pizzas):
        self.store_id = store_id
        self.cust_name = fake.name()
        self.pay_token = str(uuid.uuid4())
        self.pay_type = self.payment_types[random.randint(0, 7)]
        self.cust_lat = round((store_lat + random.uniform(-0.037, 0.037)), 6)
        self.cust_lon = round((store_lon + random.uniform(-0.0432, 0.0432)), 6)
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


# send pizza-order to first component in store's workflow
def request_order(q, url):
    while True:
        order = q.get()
        order_dict = order.generate_order()
        print("\nPizza Order Request:\n" + json.dumps(order_dict, indent=4))
        response = requests.post(url, json=json.dumps(order_dict))
        print("URL: {}".format(url))
        print("Response: {}, {}".format(response.status_code, response.text))
        q.task_done()


# gets workflow information and forms URL for 1st component and cass
def get_component_urls(store_id):
    wkf_manager_url = cluster_url + ":8080/workflow-requests/" + store_id
    response = requests.get(wkf_manager_url)
    if response.status_code != 200:
        print("Error getting component URLs!\nScript is terminating...")
        exit()
    wkf_data = json.loads(response.text)

    first_comp = wkf_data["component-list"][0]
    if first_comp == "cass":
        first_comp = wkf_data["component-list"][1]

    comp_port = port_dict[first_comp] +\
        (wkf_data["workflow-offset"] if wkf_data["method"] == "edge" else 0)
    comp_url = cluster_url + ":" + str(comp_port) + "/order"

    cass_port = port_dict["cass"] +\
        (wkf_data["workflow-offset"] if wkf_data["method"] == "edge" else 0)
    cass_url = cluster_url + ":" + str(cass_port) + "/coordinates/"
    
    return comp_url, cass_url


# get store latitude and longitude
def get_store_coordinates(store_id, url):
    cass_url = url + store_id
    print("cass_url: " + cass_url)
    response = requests.get(url)
    if response.status_code != 200:
        print("Error getting store coordinates!\nScript is terminating...")
        exit()
    coords = json.loads(response.text)
    return coords["latitude"], coords["longitude"]


if __name__ == "__main__":
    print("\n*** Pizza Order Generator Script - User Input Required ***")

    # Prompt user for storeID
    store_id = input("\nPlease enter the store's UUID: ")
    # while True:
    #     store_id = input("\nPlease enter the store's UUID: ")
    #     try:
    #         if UUID(store_id).version == 4:
    #             break
    #     except:
    #         print("Invalid store UUID. Please try again.")

    # Prompt user for start date selection
    while True:
        input_date = input("\nPlease enter the start date (MM-DD-YYYY): ")
        try:
            month, day, year = input_date.split("-")
            start_date = datetime(int(year), int(month), int(day))
            break
        except:
            print("Invalid date format. Please try again.")

    # Prompt user for days to generate orders
    while True:
        try:
            num_days = int(input("\nEnter the number of days to generate orders (min: 1, max: 365): "))
            if 1 <= num_days <= 365:
                break
        except:
            print("Invalid input. Please try again.")

    # Prompt user for orders generated per day
    while True:
        try:
            orders_per_day = int(input("\nEnter the number of orders to generate per day (min: 1, max: 60): "))
            if 1 <= orders_per_day <= 60:
                break
        except:
            print("Invalid input. Please try again.")

    # Prompt user for max pizzas per order
    while True:
        try:
            max_pizzas = int(input("\nEnter the maximum number of pizzas per order (min: 1, max: 20): "))
            if 1 <= max_pizzas <= 20:
                break
        except:
            print("Invalid input. Please try again.")

    print("\n*** Pizza Order Generator Script - Generating Orders ***")

    first_url, cass_url = get_component_urls(store_id)
    store_lat, store_lon = get_store_coordinates(store_id, cass_url)   
    
    total_orders = num_days * orders_per_day
    q = Queue(total_orders)

    t = threading.Thread(target=request_order, args=(q, first_url))
    t.daemon = True
    t.start()

    date_offset = 0
    for i in range(total_orders):
        if (i != 0) and ((i % orders_per_day) == 0):
            date_offset += 1
            time.sleep(60 - orders_per_day)
        date_str = (start_date + timedelta(days=date_offset)).isoformat()
        pizza_order = PizzaOrder(store_id, store_lat, store_lon, date_str, max_pizzas)
        q.put(pizza_order)
        time.sleep(1)
        
    q.join()    # Wait for all PizzaOrder objects to be processed from the queue
