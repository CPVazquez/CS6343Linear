import json
import logging
import threading
import socket
from time import sleep

import requests
from flask import Flask, request, Response

__author__ = "Carla Vazquez"
__version__ = "1.0.0"
__maintainer__ = "Carla Vazquez"
__email__ = "cpv150030@utdallas.edu"
__status__ = "Development"

logging.UPDATE_LEVEL = 25
logging.addLevelName(logging.UPDATE_LEVEL, "UPDATE")
logging.basicConfig(
    level=logging.UPDATE_LEVEL,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger()
logger.setLevel(logging.UPDATE_LEVEL)

url = "http://cluster1-1.utdallas.edu:8080/workflow-request/"

# set up flask app
app = Flask(__name__)

t = None
storeSelect = None


@app.route("/results", methods=["PUT"])
def print_results():
    mess = json.loads(request.get_json())
    logger.log(logging.UPDATE_LEVEL, mess["message"])
    return Response(status=200)


@app.route("/health", methods=["GET"])
def health_check():
    return Response(status=200, response="healthy\n")


def shutdown_server():
    t.running = False
    t.join()


def issue_workflow_request():
    global storeSelect

    method = input("What deployment method do you want to use "
                   "(persistent or edge): ")

    while method != "persistent" and method != "edge":
        method = input("Invalid selection. Pick persistent or edge: ")

    print("What components do you want?\n\
        * order-verifier\n\
        * delivery-assigner\n\
        * cass\n\
        * restocker\n\
        * auto-restocker")
    components = input("Enter a space seperated list: ")

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
                               " space\nserperated list of valid components: ")

    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)

    workflow_dict = {
        "storeId": storeSelect,
        "method": method,
        "component-list": component_list,
        "origin": ip_address
    }

    workflow_json = json.dumps(workflow_dict)
    logger.log(
        logging.UPDATE_LEVEL,
        "\nWorkflow Request Generated:\n" +
        json.dumps(workflow_dict, sort_keys=True, indent=4)
    )
    response = requests.post(url + storeSelect, json=workflow_json)

    if response.status_code == 200:
        logger.log(logging.UPDATE_LEVEL, "Workflow successfully deployed!")
    else:
        logger.log(
            logging.UPDATE_LEVEL,
            "Workflow deployment failed: " +
            response.text
        )


def issue_workflow_teardown():
    global storeSelect

    response = requests.delete(url + storeSelect)
    logger.log(
        logging.UPDATE_LEVEL,
        "Workflow teardown recieved the following response: " + response.text
    )


def startup():
    global storeSelect

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

    print("What do you want to do?\n" +
          "\t1. Send workflow request\n" +
          "\t2. Teardown workflow\n" +
          "\t3. Exit\n")

    while True:
        choice = input("Pick an option (1-3): ")
        while choice != "1" and choice != "2" and choice != "3":
            choice = input("Invalid selection. Pick 1-3: ")

        if choice == "1":
            issue_workflow_request()
        elif choice == "2":
            issue_workflow_teardown()
        else:
            shutdown_server()
            break


if __name__ == "__main__":
    global t
    t = threading.Thread(target=app.run, args=("0.0.0.0", 8080, False))
    t.start()
    sleep(1)
    startup()
