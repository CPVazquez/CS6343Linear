# Pizza-Order Generator Script

## Written By
Chris Scott

## Description
  * This program generates fake pizza orders for Workflow 2 by:
    * Randomly generating customer details, such as name, location coordinates, and payment information
    * Randomly constructs pizza orders from the valid pizza attributes
  * The script prompts the user for the following information:
    * Store UUID (assigned by Restaurant Owner client)
    * Start date of order generation
      * Valid date in the format MM-DD-YYYY
    * Number of days to generate orders
      * Min: 1
      * Max: 365
    * Number of orders to generate per day:
      * Min: 1
      * Max: 60
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

## Commands
```
pipenv sync
pipenv run python3 generate_order.py
```
Upon running the script, the user will be prompted for the information described above.

[Main README](https://github.com/CPVazquez/CS6343Linear)