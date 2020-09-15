#!/usr/bin/python3

from faker import Faker
import json
import random
import base64

fake = Faker('en_US')

def generate_order(order_num):
    # Lists of valid order attribute/values
    payment_types = ['PayPal','Google Pay','Apple Pay','Visa','Mastercard','AMEX','Discover','Gift Card']
    crust_types = ['Thin','Traditional']
    sauce_types = ['Spicy','Traditional']
    cheese_amts = ['None','Light','Normal','Extra']
    topping_types = ['Pepperoni','Sausage','Beef','Onion','Chicken','Peppers','Olives','Bacon','Pineapple','Mushrooms']

    # 'store_id' is base64 encoding of string "RichardsonTX"
    # Placeholder, will change when pizza locations are finalized
    store_id = str(base64.b64encode('RichardsonTX'.encode('utf-8')), 'utf-8')
    payment_token_type = payment_types[random.randint(0, 7)]
    # 'payment_token' is base64 encoding of 'payment_token_type'
    payment_token = str(base64.b64encode(payment_token_type.encode('utf-8')), 'utf-8')

    # Construct the order dict
    order = {
        ('order' + str(order_num)): {
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
    return order

def main():
    for i in range(1000,1005):
        order = generate_order(i)
        print(json.dumps(order, indent=4))
        file_name = 'order' + str(i) + '.json'
        with open(file_name, 'w') as json_file:
            json.dump(order, json_file, indent=4)


if __name__ == "__main__":
    main()
