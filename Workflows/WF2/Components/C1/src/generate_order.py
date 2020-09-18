from faker import Faker
from queue import Queue
from threading import Thread
import requests
import json
import random
import base64

fake = Faker('en_US')
max_orders = 100    # Maximum orders to be generated
max_pizzas = 20     # Maximum number of pizzas allowed per order
num_threads = 5     # Number of threads to be started
url = "http://0.0.0.0:8080/order"

class PizzaOrder:
    # List of Pizza Attributes
    payment_types = ['PayPal','Google Pay','Apple Pay','Visa','Mastercard','AMEX','Discover','Gift Card']
    crust_types = ['Thin','Traditional']
    sauce_types = ['Spicy','Traditional']
    cheese_amts = ['None','Light','Normal','Extra']
    topping_types = ['Pepperoni','Sausage','Beef','Onion','Chicken','Peppers','Olives','Bacon','Pineapple','Mushrooms']

    def __init__(self, order_num):
        self.order_num = order_num
        self.order_name = "order" + str(order_num).zfill(4)

    def get_store_id(self):
        return str(base64.b64encode('RichardsonTX'.encode('utf-8')), 'utf-8')

    def get_payment_token(self):
        return str(base64.b64encode('PaymentToken'.encode('utf-8')), 'utf-8')

    def get_payment_token_type(self):
        return self.payment_types[random.randint(0, 7)]

    def add_more_pizzas(self, order_dict):
        n = round(random.triangular(1, max_pizzas, 1))  # Random int in range 1 <= n <= max_pizzas [mode is 1]
        # At this point, there's 1 pizza in pizzaList from generate_order()
        # For loop adds anywhere from 0 to 19 additional pizzas to pizzaList
        # (initial pizza) + (up to 19 additional pizzas) = max_pizzas
        for _ in range(1, n):
            new_pizza = {
                "crustType": self.crust_types[random.randint(0, 1)],
                "sauceType": self.sauce_types[random.randint(0, 1)],
                "cheeseAmt": self.cheese_amts[random.randint(0, 3)],
                "toppingList": random.sample(self.topping_types, random.randint(0, 9))
            }
            order_dict[self.order_name]["pizzaList"].append(new_pizza)
        return order_dict

    def generate_order(self):
        # Construct the pizza order dict, with a single pizza in pizzaList
        order_dict = {
            self.order_name: {
                "storeId": self.get_store_id(),
                "custName": fake.name(),
                "paymentToken": self.get_payment_token(),
                "paymentTokenType": self.get_payment_token_type(),
                "custLocation": {
                    "lat": round(random.uniform(-90.0, 90.0), 4),
                    "lon": round(random.uniform(-180.0, 180.0), 4)
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
        #print(response)
        q.task_done()


if __name__ == "__main__":
    q = Queue(max_orders)

    for _ in range(num_threads):
        t = Thread(target=post_order, args=(q,))
        t.daemon = True
        t.start()

    for order_num in range(max_orders):
        pizza_order = PizzaOrder(order_num)
        q.put(pizza_order)

    q.join()    # Wait for all PizzaOrder objects to be processed from the queue
