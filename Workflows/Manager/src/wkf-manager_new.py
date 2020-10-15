import requests
import logging
import json
from time import sleep
import threading

import docker
import jsonschema
from flask import Flask, request, Response

__author__ = "Carla Vazquez"
__version__ = "2.0.0"
__maintainer__ = "Carla Vazquez"
__email__ = "cpv150030@utdallas.edu"
__status__ = "Development"

# set up necessary docker clients
client = docker.from_env()
APIclient = docker.APIClient(base_url='unix://var/run/docker.sock')

# set up logging
logging.basicConfig(level=logging.DEBUG, 
    format="%(asctime)s - %(levelname)s - %(message)s")
logging.basicConfig(level=logging.INFO, 
    format="%(asctime)s - %(levelname)s - %(message)s")

# set up flask app
app = Flask(__name__)

# set up component port dictionary
portDict  = {
    "order-verifier" : 1000,
    "delivery-assigner": 3000,
    "auto-restocker": 4000,
    "restocker": 5000
}

# set up thread lock
thread_lock = threading.Lock()

# set up workflow dict
workflows = dict()

# open workflow-request specification
with open("src/workflow-request.schema.json", "r") as schema:
    schema = json.loads(schema.read())

# 
def verify_workflow(data):
    global schema
    valid = True
    mess = None
    try:
        jsonschema.validate(instance=data, schema=schema)
    except Exception as inst:
        valid = False
        logging.debug("workflow-request rejected:\n" + json.dumps(data))
        logging.debug("Request rejected due to failed validation.")
        valid = False
        mess = inst.args[0]
    return valid, mess


def start_cass():
    # look for cass service
    cass_filter = client.services.list(filters={'name': 'cass'})

    # if cass service not found
    if len(cass_filter) == 0:

        logging.debug("{:*^60}".format(" cass doesn't exist "))
        logging.debug("{:*^60}".format(" Spinning up cass "))

        # create cass service
        database_service = client.services.create(
            "trishaire/cass", # the name of the image
            name="cass", # name of the service
            endpoint_spec=docker.types.EndpointSpec(mode="vip", ports={ 9042 : 9042 }),
            networks=['myNet']) #network
        
    healthy = False

    # keep pinging the service
    while not healthy : 
        tasks = client.services.get("cass").tasks()

        for task in tasks:
            tID = task['ID']
            result = APIclient.inspect_task(tID)['Status']['Message']
            if result == 'started':
                healthy = True    
        
        if not healthy:
            logging.debug("cass is not ready")
            sleep(5)

    logging.info("{:*^60}".format(" cass is ready for connections "))


def start_components(component, workflow_json, response_list):

    service_filter = client.services.list(filters={'name': component})

    if len(service_filter) == 0: 
        logging.debug("{:*^60}".format(" " + component + " doesn't exist "))
        logging.debug("{:*^60}".format(" Spinning up " + component + " "))

        # create the order-verifier service
        order_service = client.services.create(
                "trishaire/" + component+":latest",  # the name of the image
            name=component,  # name of service
            endpoint_spec=docker.types.EndpointSpec(mode="vip", ports={ portDict[component] : portDict[component] }),
            env=["CASS_DB=cass"], # set environment var
            networks=['myNet']) # set network

    # wait for component to spin up
    while True:
        try:
            order_response = requests.get("http://"+component+":"+portDict[component]+"/health")
        except:
            continue
        else:
            break
    
    logging.info("{:*^60}".format(" " + component + " is healthy "))
    # send workflow_request to component
    # comp_response = requests.post("http://"+component+":"+portDict[component]+"/workflow-setup", json=json.dumps(workflow_json))
    # thread_lock.acquire(blocking=True)
    # response_list.append(comp_response)
    # thread_lock.release()
    # logging.info("{:*^60}".format(" sent " + component + " workflow specification for " + workflow_json["storeId"]+ " "))



@app.route("/workflow-request", methods=["POST"])
def setup_workflow():
    logging.debug("In the workflow request")
    # get the data from the request
    data = json.loads(request.get_json())
    # verify the request is valid
    valid, mess = verify_workflow(data)

    logging.debug("validating")
    # if invalid workflow request send back a 400 response
    if not valid:
        return Response(status=400, response="workflow-request ill formated\n" + mess)

    logging.debug("validated")
    # get the list of components for the workflow
    component_list = data["component-list"].copy()
    
    # check if the workflow request specifies cass
    has_cass = True
    try:
        component_list.remove("cass")
    except ValueError:
        has_cass = False

    # startup cass first and formost
    if has_cass :
        start_cass()

    thread_list = []
    response_list = []
    # start up the rest of the components
    for comp in component_list:
        x = threading.Thread(target=start_components, args=(comp, data, response_list))
        x.start()
        thread_list.append(x)

    # wait for all the threads to terminate
    for x in thread_list :
        x.join()

    workflows[data["storeID"]] = data
    return Response(status=200, response="Workflow deployed!")

# Health check endpoint
@app.route("/health", methods=["GET"])
def health_check():
    return Response(status=200,response="healthy\n")

