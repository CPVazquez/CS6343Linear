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


def start_cass(workflow_json):
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
        # retrieve the tasks of the cass servcie
        tasks = client.services.get("cass").tasks()

        # see if at least one of the tasks is healthy
        for task in tasks:
            tID = task['ID']
            result = APIclient.inspect_task(tID)['Status']['Message']
            if result == 'started':
                healthy = True    
        
        # if none of the tasks are healthy, wait a bit before
        # trying again
        if not healthy:
            logging.debug("cass is not ready")
            sleep(5)

    logging.debug("{:*^60}".format(" cass is ready for connections "))

    #send update to the resturant owner
    origin_url = "http://"+workflow_json["origin"]+":8080/results"
    message = "Component cass of your workflow has been deployed"
    message_dict = {"message": message}


def start_components(component, workflow_json, response_list):

    # check if service exists
    service_filter = client.services.list(filters={'name':component})
    service_url = "http://" + component + ":" + str(portDict[component])

    # if not exists
    if len(service_filter) == 0: 
        logging.debug("{:*^60}".format(" " + component + " doesn't exist "))
        logging.debug("{:*^60}".format(" Spinning up " + component + " "))

        # create the service
        service = client.services.create(
                "trishaire/" + component+":latest",  # the name of the image
            name=component,  # name of service
            endpoint_spec=docker.types.EndpointSpec(mode="vip", ports={ portDict[component] : portDict[component] }),
            env=["CASS_DB=cass"], # set environment var
            networks=['myNet']) # set network

    # wait for component to spin up
    while True:
        try:
            service_response = requests.get(service_url+"/health")
        except:
            sleep(1)
        else:
            break
    
    logging.debug("{:*^60}".format(" " + component + " is healthy "))

    #send update to the resturant owner
    origin_url = "http://"+workflow_json["origin"]+":8080/results"
    message = "Component " + component + " of your workflow has been deployed"
    message_dict = {"message": message}

    requests.post(origin_url, json=json.dumps(message_dict))
    # send workflow_request to component
    # logging.debug("{:*^60}".format(" sent " + component + " workflow specification for " + workflow_json["storeId"]+ " "))
    # service_response = requests.post(service_url+"/workflow-setup", json=json.dumps(workflow_json))
    # logging.debug("{:*^60}".format(" recieved response from " + component + " for workflow specification " + workflow_json["storeId"]+ " "))
    # thread_lock.acquire(blocking=True)
    # response_list.append(comp_response)
    # thread_lock.release()
    



@app.route("/workflow-request", methods=["POST"])
def setup_workflow():
    # get the data from the request
    data = json.loads(request.get_json())
    # verify the request is valid
    valid, mess = verify_workflow(data)

    # if invalid workflow request send back a 400 response
    if not valid:
        return Response(status=400, response="workflow-request ill formated\n" + mess)

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
        start_cass(data)

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

    delploy_successful = True

    for resp in response_list:
        if resp.status_code != 200:
            delploy_successful = False

    if delploy_successful: 
        workflows[data["storeId"]] = data
        return Response(status=200, response="Workflow deployed!")
    else :
        return Response(status=404, response="Worflow deployment failed.\nInvalid workflow specification")


# Health check endpoint
@app.route("/health", methods=["GET"])
def health_check():
    return Response(status=200,response="healthy\n")

