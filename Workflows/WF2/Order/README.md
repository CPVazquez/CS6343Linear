# Pizza-Order Generator Script

## Written By
Chris Scott

## Description
* This program generates fake pizza orders for Workflow 2 by:
  * Randomly generating customer details, such as name, location coordinates, and payment information
  * Randomly constructs pizza orders from the valid pizza attributes
* The script prompts the user for the following information:
  * Store UUID (assigned by Restaurant Owner client)
  * Start date of order generation:
    * Valid date in the format MM-DD-YYYY
  * Number of days to generate orders:
    * Min: 1
    * Max: 365
  * Number of orders to generate per day:
    * Min: 1
    * Max: 60
  * Limit on the number of pizzas allowed per order:
    * Min: 1
    * Max: 20
  * Detailed results of processed pizza-order:
    * If enabled, the processed pizza-order JSON object will be printed, in addition to success/failure status.
    * If disabled, only the success/failure status will be printed for each order. In the event of a failure, an error message will also be printed.

## Setup
Machine requirements:
* Python 3

Package requirements:
* pipenv

Packages installed on pipenv virtual environment:
  * faker
  * requests

## Commands
  ```
  pipenv sync
  pipenv run python3 generate_order.py
  ```
Upon running the script, the user will be prompted for the information described above.

[Main README](https://github.com/CPVazquez/CS6343Linear)