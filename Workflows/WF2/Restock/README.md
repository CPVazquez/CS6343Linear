# Generate Order Script

## Written By
Chris Scott

## Requirements:
  * Python 3.8
  * Install Requests Python package (https://pypi.org/project/requests/2.7.0/)

## Description
  * This program generates restock orders for Workflow 2
  * The script prompts the user for the following information:
    * URL for Order Verifier
    * Number of threads to start:
      * Min: 1
      * Max: 10
    * A pizza store location from the 3 preset locations:
      * 0 for StoreID 7098813e-4624-462a-81a1-7e0e4e67631d
      * 1 for StoreID 5a2bb99f-88d2-4612-ac60-774aea9b8de4
      * 2 for StoreID b18b3932-a4ef-485c-a182-8e67b04c208c
    * Total number of restock orders to generate:
      * Min: 1
      * Max: 1000

## Setup
Machine requirements:
* Python 3.8

Package requirements:
* pipenv

Packages installed on pipenv virtual environment:
  * Install Requests Python package (https://pypi.org/project/requests/2.7.0/)

## Commands
```
python3 generate_restock.py
```
Upon running the script, the user will be prompted for the information described above.

[Main README](https://github.com/CPVazquez/CS6343)