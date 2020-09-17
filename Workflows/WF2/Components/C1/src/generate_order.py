#!/usr/bin/python3

from faker import Faker
from queue import Queue
from threading import Thread
import requests
import json
import random
import base64

# Globals
fake = Faker('en_US')
max_orders = 1     # Maximum orders to be generated
num_threads = 1     # Number of threads to be started
url = "http://0.0.0.0:8080/order"

# TODO: update to pull data from DB, when it's operational
def generate_order(order_num):
    # Lists containing valid order properties
    payment_types = ['PayPal','Google Pay','Apple Pay','Visa','Mastercard','AMEX','Discover','Gift Card']
    crust_types = ['Thin','Traditional']
    sauce_types = ['Spicy','Traditional']
    cheese_amts = ['None','Light','Normal','Extra']
    topping_types = ['Pepperoni','Sausage','Beef','Onion','Chicken','Peppers','Olives','Bacon','Pineapple','Mushrooms']

    # 'store_id' is base64 encoding of string "RichardsonTX"
    store_id = str(base64.b64encode('RichardsonTX'.encode('utf-8')), 'utf-8')
    payment_token_type = payment_types[random.randint(0, 7)]
    # 'payment_token' is base64 encoding of 'payment_token_type'
    payment_token = str(base64.b64encode(payment_token_type.encode('utf-8')), 'utf-8')

    # Construct an order dict:
    # - Generate fake data for "storeId" ... "paymentTokenType"
    # - Generate random coordinates ("lat" & "lon") from valid range
    # - Randomly select pizza attributes from above Lists
    order_dict = {
        ('order' + str(order_num).zfill(3)): {
            "storeId": store_id,
            "custName": fake.name(),
            "paymentToken": payment_token,
            "paymentTokenType": payment_token_type,
            "custLocation": {
                "lat": round(random.uniform(-90.0, 90.0), 4),
                "lon": round(random.uniform(-180.0, 180.0), 4)
            },
            "pizzaList": [{
                "crustType": crust_types[random.randint(0, 1)],
                "sauceType": sauce_types[random.randint(0, 1)],
                "cheeseAmt": cheese_amts[random.randint(0, 3)],
                "toppingList": random.sample(topping_types, random.randint(0, 9))
            }]
        }
    }
    return order_dict

def post_order(q):
    while True:
        order_dict = q.get()
        order_json = json.dumps(order_dict)
        r = requests.post(url, json=order_json)
        print('Response Text: ' + r.text)
        print('-->Response Status Code: ' + str(r.status_code) + '\n')
        q.task_done()

if __name__ == "__main__":
    q = Queue(max_orders)

    for _ in range(num_threads):
        t = Thread(target=post_order, args=(q,))
        t.daemon = True
        t.start()

    for order_num in range(max_orders):
        order_dict = generate_order(order_num)
        q.put(order_dict)

    q.join()
