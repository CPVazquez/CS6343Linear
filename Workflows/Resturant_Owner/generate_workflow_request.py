import json
import sys
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

create logger
logging.UPDATE_LEVEL = 25
logging.addLevelName(logging.UPDATE_LEVEL, "UPDATE")
logger = logging.getLogger()
logger.setLevel(logging.UPDATE_LEVEL)

ch = logging.StreamHandler()
ch.setLevel(logging.UPDATE_LEVEL)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
# add formatter to ch
ch.setFormatter(formatter)

# add ch to logger
logger.addHandler(ch)


# logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s")
# logging.setLevel(logging.UPDATE_LEVEL)

url = "http://cluster1-1.utdallas.edu:8080/workflow-request"

# set up flask app
app = Flask(__name__)


@app.route("/results", methods=["POST"])
def print_results():
    mess = json.loads(request.get_json())
    logger.log(logging.UPDATE_LEVEL, mess["message"])
    return Response(status=200)


@app.route("/health", methods=["GET"]) 
def health_check():
    return Response(status=200,response="healthy\n")


def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()


def startup():

    print("Which store are you generating a workflow for? \n\
        A. 7098813e-4624-462a-81a1-7e0e4e67631d\n\
        B. 5a2bb99f-88d2-4612-ac60-774aea9b8de4\n\
        C. b18b3932-a4ef-485c-a182-8e67b04c208c")
    storeSelect = input("Pick a store (A-C): ")

    while storeSelect != "A" and storeSelect != "B" and storeSelect != "C":
        storeSelect = input("Invalid selection. Pick A-C: ")
    
    if storeSelect == "A" :
        storeSelect = "7098813e-4624-462a-81a1-7e0e4e67631d"
    elif storeSelect == "B" :
        storeSelect = "5a2bb99f-88d2-4612-ac60-774aea9b8de4"
    else :
        storeSelect = "b18b3932-a4ef-485c-a182-8e67b04c208c"
    
    method = input("What deployment method do you want to use (persistent or edge): ")

    while method != "persistent" and method != "edge" :
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
        for comp in component_list :
            if comp == "order-verifier" :
                continue
            elif comp == "delivery-assigner" :
                continue
            elif comp == "cass" :
                continue
            elif comp == "restocker" :
                continue
            elif comp == "auto-restocker" :
                continue
            else :
                valid = False
        if valid :
            break 
        else :
            components = input("Invalid component selection. Please enter a space\n\serperated list of valid components: ")

    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)

    workflow_dict = {
        "storeId": storeSelect,
        "method": method,
        "component-list": component_list,
        "origin": ip_address
    }

    workflow_json = json.dumps(workflow_dict)
    logger.log(logging.UPDATE_LEVEL,"\nWorkflow Request Generated:\n"+ json.dumps(workflow_dict, sort_keys=True, indent=4))
    response = requests.post(url, json=workflow_json)
    
    if response.status_code == 200 :
        logger.log(logging.UPDATE_LEVEL,"STATUS UPDATE: Workflow successfully deployed!")   
    else:
        logger.log(logging.UPDATE_LEVEL,"STATUS UPDATE: Workflow deployment failed: " + response.text)
        shutdown_server()

    

if __name__ == "__main__" :
    x = threading.Thread(target=app.run, args=("0.0.0.0",8080))
    x.start()
    sleep(1)
    startup()
