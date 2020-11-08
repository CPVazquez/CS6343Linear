# Generate Order Script

## Written By
Chris Scott

## Description
  * This program generates fake pizza orders for Workflow 2 by:
    * Randomly generating customer details, such as name, location coordinates, and payment information
    * Randomly constructs pizza orders from the valid pizza attributes
  * The script prompts the user for the following information:
    * A pizza store location from the 3 preset locations:
      * 0 for StoreID 7098813e-4624-462a-81a1-7e0e4e67631d
      * 1 for StoreID 5a2bb99f-88d2-4612-ac60-774aea9b8de4
      * 2 for StoreID b18b3932-a4ef-485c-a182-8e67b04c208c
    * Workflow component(s) to receive pizza-order 
      * Order Verifier XOR (Delivery Assigner OR Auto-Restocker)
    * Start date of order generation
      * Valid date in the format MM-DD-YYYY
    * Number of days to generate orders
      * Min: 1
      * Max: 365
    * Number of orders to generate per day:
      * Min: 1
      * Max: 1000
    * Limit on the number of pizzas allowed per order:
      * Min: 1
      * Max: 20

## Setup
Machine requirements:
* Python 3.8

Package requirements:
* pipenv

Packages installed on pipenv virtual environment:
  * Install Faker Python package (https://pypi.org/project/Faker/)
    * This program uses Faker to randomly generate customer names.
  * Install Requests Python package (https://pypi.org/project/requests/2.7.0/)

## Setup
Machine requirements:
* Python 3.8

Package requirements:
* pipenv

Packages installed on pipenv virtual environment:
  * Install Faker Python package (https://pypi.org/project/Faker/)
    * This program uses Faker to randomly generate customer names.
  * Install Requests Python package (https://pypi.org/project/requests/2.7.0/)


## Commands
```
python3 generate_order.py
```
Upon running the script, the user will be prompted for the information described above.

[Main README](https://github.com/CPVazquez/CS6343Linear)