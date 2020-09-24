Generate Order

Requirements:
  - Python 3.8
  - Install Faker Python package (https://pypi.org/project/Faker/)
    This program uses Faker to randomly generate customer names.

Function:
  - This program generates fake pizza orders for Workflow 2.
  - Randomly select a pizza store location from the 3 preset locations.
  - Randomly generate customer details, such as name, location coordinates,
    and payment information.
  - Randomly construct pizza order from the valid pizza attributes.
  - A single pizza order will, at minimum, contain one pizza, but may contain
    up to max_pizzas. max_pizzas is a command line argument. Default is 20.
  - The user specifies how many pizza orders to create via command line
    argument (max_orders).
  - This program has threading functionality, but it may not be of any
    significant use. The number of threads is specified via command
    line argument (num_threads).
  - URL for posting order requests is also specified via command line
    argument (url).

Command:
  - python3 generate_order.py <url> <num_threads> <max_orders> <max_pizzas>

    Replace the bracketed variables with your information. Example:

    python3 generate_order.py http://0.0.0.0:8080/order 1 10 20
