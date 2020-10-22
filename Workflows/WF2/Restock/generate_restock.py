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

cluster = "cluster1-1.utdallas.edu"


class Restock:
    # Restock Attribute Lists
    stores = ["7098813e-4624-462a-81a1-7e0e4e67631d", 
              "5a2bb99f-88d2-4612-ac60-774aea9b8de4", 
              "b18b3932-a4ef-485c-a182-8e67b04c208c"]
    restock_items = ['Dough', 'Cheese', 'SpicySauce', 'TraditionalSauce', 
                     'Pepperoni', 'Sausage', 'Beef', 'Onion', 'Chicken', 
                     'Peppers', 'Olives', 'Bacon', 'Pineapple', 'Mushrooms']

    def __init__(self, store):
        self.store_id = self.stores[store]

    def add_restock(self):
        # Generate a list of random items in the range of 1 to 14 (length of restock_items/items_list)
        items_list = self.restock_items.copy()
        restock_list = []
        n = round(random.triangular(1, len(items_list), 1))  # 1 <= n <= len(items_list) (mode is 1)
        for _ in range(n):
            restock = {
                "item-name": items_list.pop(random.randint(0, (len(items_list) - 1))),
                "quantity": random.randint(1, 5)
            }
            restock_list.append(restock)
        return restock_list

    def generate_restock(self):
        # Construct the restock dict
        restock_dict = {
            "storeID": self.store_id,
            "restock-list": self.add_restock()
        }
        return restock_dict


def request_restock(q, url):
    while True:
        restock = q.get()
        restock_dict = restock.generate_restock()
        print("Generated Restock Request:\n" + json.dumps(restock_dict, indent=4))
        response = requests.post(url, json=json.dumps(restock_dict))
        if response.status_code == 200:
            print("Request Accepted - {} {}".format(str(response.status_code), response.text))
        else:
            print("Request Rejected - {} {}".format(str(response.status_code), response.text))
        q.task_done()


if __name__ == "__main__":
    print("\n*** Restock Generator Script - User Input Required ***\n")
    
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
            max_restocks = int(input("Enter the number of restocks to generate (min: 1, max: 1000): "))
        except ValueError:
            print("Could not convert input data to integer. Please try again.")
        if (max_restocks >= 1) & (max_restocks <= 1000):
            print()
            break

    print("\n*** Restock Generator Script - Generating Restocks ***\n")

    url = "http://"+cluster+":5000/restock"

    q = Queue(max_restocks)

    t = Thread(target=request_restock, args=(q,url))
    t.daemon = True
    t.start()

    for _ in range(max_restocks):
        restock = Restock(store)
        q.put(restock)
        time.sleep(3)

    q.join()    # Wait for all Restock objects to be processed from the queue
