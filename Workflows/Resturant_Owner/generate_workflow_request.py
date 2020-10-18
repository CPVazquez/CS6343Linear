import json
import sys
import logging
import threading
import socket

import requests
from flask import Flask, request, Response

__author__ = "Carla Vazquez"
__version__ = "1.0.0"
__maintainer__ = "Carla Vazquez"
__email__ = "cpv150030@utdallas.edu"
__status__ = "Development"

logging.basicConfig(level=logging.DEBUG, 
    format="%(asctime)s - %(levelname)s - %(message)s")

url = "http://cluster1-1.utdallas.edu:8080/workflow-request"

# set up flask app
app = Flask(__name__)


@app.route("/results", methods=["PUT"])
def print_results():
    return Response(status=200)
    print(request.get_data(as_text=True))


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

    #app.run(port=8080, host="0.0.0.0")


    workflow_json = json.dumps(workflow_dict)
    logging.debug("\nWorkflow Request Generated:\n"+ json.dumps(workflow_dict, sort_keys=True, indent=4))
    response = requests.post(url, json=workflow_json)
    
    if response.status_code == 200 :
        logging.debug("Workflow successfully deployed!")   
    else:
        logging.debug("Workflow deployment failed: " + response.text)
        shutdown_server()

    

if __name__ == "__main__" :
    x = threading.Thread(target=app.run, args=("0.0.0.0",8080))
    x.start()
    startup()
