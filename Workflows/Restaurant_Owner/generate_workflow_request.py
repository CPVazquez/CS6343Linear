"""Restaurant Owner (client)

requests workflows and receives updates
"""
import json
import logging
import multiprocessing
import socket
from time import sleep

import requests
from flask import Flask, request, Response

__author__ = "Carla Vazquez"
__version__ = "1.0.0"
__maintainer__ = "Carla Vazquez"
__email__ = "cpv150030@utdallas.edu"
__status__ = "Development"

# set up logging\
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# create endpoint url
url = "http://cluster1-1.utdallas.edu:8080/workflow-requests"

# set up flask app
app = Flask(__name__)

# create global var storeSelect
storeSelect = None


# create a workflow-request
def issue_workflow_request():
    global storeSelect

    # get deployment method
    method = input("What deployment method do you want to use "
                   "(persistent or edge): ")

    while method != "persistent" and method != "edge":
        method = input("Invalid selection. Pick persistent or edge: ")

    # get component-list
    print("What components do you want?\n" +
          "\t* order-verifier\n" +
          "\t* delivery-assigner\n" +
          "\t* cass\n" +
          "\t* restocker\n" +
          "\t* auto-restocker")
    components = input("Enter a space separated list: ")

    while True:
        valid = True
        components = components.lower()
        component_list = components.split()
        for comp in component_list:
            if comp == "order-verifier":
                continue
            elif comp == "delivery-assigner":
                continue
            elif comp == "cass":
                continue
            elif comp == "restocker":
                continue
            elif comp == "auto-restocker":
                continue
            else:
                valid = False
        if valid:
            break
        else:
            components = input("Invalid component selection. Please enter a" +
                               " space\nseparated list of valid components: ")

    # retrieve host ip
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)

    # create the json object
    workflow_dict = {
        "method": method,
        "component-list": component_list,
        "origin": ip_address
    }

    # send the workflow-request to the workflow manager
    workflow_json = json.dumps(workflow_dict)
    logging.info(
        "\nWorkflow Request Generated:\n" +
        json.dumps(workflow_dict, sort_keys=True, indent=4)
    )
    response = requests.put(url + "/" + storeSelect, json=workflow_json)

    # parse the response
    if response.status_code == 201:
        logging.info(
            str(response.status_code) + " Workflow successfully deployed!"
        )
    else:
        logging.info(
            "Workflow deployment failed: " + str(response.status_code) + " " +
            response.text
        )


# remove an existing workflow-request
def issue_workflow_teardown():
    global storeSelect

    response = requests.delete(url + "/" + storeSelect)
    logging.info(
        "Workflow teardown received the following response: " +
        str(response.status_code) + " " + response.text
    )


# retreive an existing workflow-request
def get_workflow():
    response = requests.get(url + "/" + storeSelect)
    if response.status_code == 200:
        logging.info(
            json.dumps(json.loads(response.text), sort_keys=True, indent=4)
        )
    else:
        logging.info(
            str(response.status_code) + " " + response.text
        )


# retrieve all workflows
def get_workflows():
    response = requests.get(url)
    logging.info(
        json.dumps(json.loads(response.text), sort_keys=True, indent=4)
    )


# do setup and get user input
def startup():
    global storeSelect, t

    # pick the store this restaurant is representing
    print("Which store are you generating a workflow for? \n" +
          "\tA. 7098813e-4624-462a-81a1-7e0e4e67631d\n" +
          "\tB. 5a2bb99f-88d2-4612-ac60-774aea9b8de4\n" +
          "\tC. b18b3932-a4ef-485c-a182-8e67b04c208c")
    storeSelect = input("Pick a store (A-C): ")

    while storeSelect != "A" and storeSelect != "B" and storeSelect != "C":
        storeSelect = input("Invalid selection. Pick A-C: ")

    if storeSelect == "A":
        storeSelect = "7098813e-4624-462a-81a1-7e0e4e67631d"
    elif storeSelect == "B":
        storeSelect = "5a2bb99f-88d2-4612-ac60-774aea9b8de4"
    else:
        storeSelect = "b18b3932-a4ef-485c-a182-8e67b04c208c"

    choice = None

    # print choice menu only once
    print("What do you want to do?\n" +
          "\t1. Send workflow request\n" +
          "\t2. Teardown workflow\n" +
          "\t3. Get workflow\n" +
          "\t4. Get all workflows\n"
          "\t0. Exit")

    # get the user's choice
    while True:
        choice = input("Pick an option (0-4): ")
        while choice != "1" and choice != "2" and choice != "3" and\
                choice != "4" and choice != "0":

            choice = input("Invalid selection. Pick 0-4: ")

        if choice == "1":  # create a workflow-request
            issue_workflow_request()
        elif choice == "2":  # remove the workflow-request
            issue_workflow_teardown()
        elif choice == "3":  # retrieve the workflow-request
            get_workflow()
        elif choice == "4":  # retrieve all workflow-requests
            get_workflows()
        else:  # exit
            t.terminate()
            break


# an endpoint to receive updates at
@app.route("/results", methods=["POST"])
def print_results():
    mess = json.loads(request.get_json())
    logging.info(mess["message"])
    return Response(status=200)


# Health check endpoint
@app.route("/health", methods=["GET"])
def health_check():
    return Response(status=200, response="healthy\n")


if __name__ == "__main__":
    global t

    t = multiprocessing.Process(target=app.run, args=("0.0.0.0", 8080, False))
    t.start()
    sleep(1)
    startup()
