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
logging.getLogger('requests').setLevel(logging.WARNING)

# create endpoint url
url = "http://cluster1-1.utdallas.edu:8080/workflow-requests"
predict_url = "http://cluster1-1.utdallas.edu:"
itemArr = ["Pepperoni", "Sausage", "Beef", "Onion", "Chicken",
           "Peppers", "Olives", "Bacon", "Pineapple", "Mushrooms",
           "Dough", "Cheese", "SpicySauce", "TraditionalSauce"]

# set up flask app
app = Flask(__name__)

# create global var storeSelect
storeSelect = None
method = None
workflow_offset = 0


# create a workflow-request
def update_workflow():
    global storeSelect, method

    if method is None:
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
    response = requests.put(
        "http://cluster1-1.utdallas.edu:8080/workflow-update/" + storeSelect,
        json=workflow_json
    )

    # parse the response
    if response.status_code == 200:
        logging.info(
            str(response.status_code) + " Workflow successfully updated!"
        )
    else:
        logging.info(
            "Workflow update failed: " + str(response.status_code) + " " +
            response.text
        )


# request prediction
def request_prediction():
    global storeSelect

    if not(method is None) and method == "edge" and workflow_offset == 0:
        logging.info("Method is edge, but offset is not set. getting offset")
        get_workflow()

    itemName = input("what item do you want to predict for: ")
    while not(itemName in itemArr):
        itemName = input("invalid item. please enter valid item: ")

    history = input("how far back do you want to look (in days): ")
    history = str(history, "utf-8")
    while not history.isnumeric:
        history = input("thats not a number. please enter an int: ")
        history = str(history, "utf-8")

    days = input("how far in advance do you want to predict (in days): ")
    days = str(days, "utf-8")
    while not days.isnumeric:
        days = input("thats not a number. please enter an int: ")
        days = str(days, "utf-8")

    predictor_json = {
        "itemName": itemName,
        "history": int(history),
        "days": int(days)
    }

    logging.info(
        "Prediction Request Generated:\n" +
        json.dumps(predictor_json, sort_keys=True, indent=4)
    )

    try:
        response = requests.get(
            predict_url + str(4000 + workflow_offset) +
            "/predict-stock/" + storeSelect,
            json=json.dumps(predictor_json)
        )
    except Exception:
        logging.info(
            "error connecting to restocker, not prediction retrieved.")
    else:
        if response.code == 200:
            logging.info("Prediction recieved!")
            logging.info(
                json.dumps(json.loads(response.text), sort_keys=True, indent=4)
            )
        else:
            logging.info("Prediction failed.")


# create a workflow-request
def issue_workflow_request():
    global storeSelect, method

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
          "\t* auto-restocker\n")
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
    global storeSelect, method

    response = requests.delete(url + "/" + storeSelect)
    logging.info(
        "Workflow teardown received the following response: " +
        str(response.status_code) + " " + response.text
    )

    if(response.status_code == 204):
        method = None


# retreive an existing workflow-request
def get_workflow():
    global workflow_offset, method
    response = requests.get(url + "/" + storeSelect)
    if response.status_code == 200:
        respJson = json.loads(response.text)
        if not(method is None) and method == "edge":
            workflow_offset = respJson["workflow-offset"]
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
          "\t2. Update existing workflow\n" +
          "\t3. Teardown workflow\n" +
          "\t4. Get workflow\n" +
          "\t5. Get all workflows\n"
          "\t6. Get prediction\n"
          "\t0. Exit")

    # get the user's choice
    while True:
        choice = input("Pick an option (0-6): ")
        while choice != "1" and choice != "2" and choice != "3" and\
                choice != "4" and choice != "5" and choice != "6" and\
                choice != "0":

            choice = input("Invalid selection. Pick 0-5: ")

        if choice == "1":  # create a workflow-request
            issue_workflow_request()
        elif choice == "2":  # update a workflow
            update_workflow()
        elif choice == "3":  # remove the workflow-request
            issue_workflow_teardown()
        elif choice == "4":  # retrieve the workflow-request
            get_workflow()
        elif choice == "5":  # retrieve all workflow-requests
            get_workflows()
        elif choice == "6":
            request_prediction()
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
