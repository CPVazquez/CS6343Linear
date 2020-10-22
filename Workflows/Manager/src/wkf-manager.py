#!/usr/bin/python3
"""Workflow Manager Component

Creates and destroys specified workflows
"""
import logging
import json
from time import sleep
import threading

import requests
import docker
import jsonschema
from flask import Flask, request, Response

__author__ = "Carla Vazquez"
__version__ = "2.0.0"
__maintainer__ = "Carla Vazquez"
__email__ = "cpv150030@utdallas.edu"
__status__ = "Development"

# set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logging.getLogger('docker').setLevel(logging.INFO)
logging.getLogger('requests').setLevel(logging.INFO)

# set up necessary docker clients
client = docker.from_env()
APIclient = docker.APIClient(base_url='unix://var/run/docker.sock')

# set up flask app
app = Flask(__name__)

# set up component port dictionary
portDict = {
    "order-verifier": 1000,
    "delivery-assigner": 3000,
    "cass": 9042,
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


# check that the workflow specification json is valid
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


def start_cass(workflow_json, response_list):
    # look for cass service
    cass_filter = client.services.list(filters={'name': 'cass'})

    origin_url = "http://"+workflow_json["origin"]+":8080/results"

    # if cass service not found
    if len(cass_filter) == 0:

        logging.info("cass doesn't exist")
        logging.info("Spinning up cass")

        # create cass service
        cass_service = client.services.create(
            "trishaire/cass:latest",  # the name of the image
            name="cass",  # name of the service
            endpoint_spec=docker.types.EndpointSpec(
                mode="vip", ports={9042: 9042}
            ),
            networks=['myNet'])   # network

    healthy = False
    count = 0

    # keep pinging the service
    while not healthy:
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
            if count < 60:  # request has not timed out
                logging.info(
                    "Attempt " + str(int(count / 5)) + ", cass is not ready"
                )
                # message = "Attempting to spin up cass"
                # message_dict = {"message": message}
                # requests.post(origin_url, None, json.dumps(message_dict))
                sleep(5)
                count += 5
            else:  # request timed out
                cass_service.remove()
                break

    message = None
    resp = None

    if count < 60:
        logging.info(
            "SUCCESS: cass is ready for connections"
        )
        message = "Component cass of your workflow has been deployed"
        resp = requests.Response()
        resp.status_code = 201
    else:
        logging.info(
            "FAILURE: cass could not be debloyed "
        )
        message = "Timeout. Component cass of your " +\
            "workflow could not be deployed"
        resp = requests.Response()
        resp.status_code = 408

    # send update to the restaurant owner
    message_dict = {"message": message}
    requests.post(origin_url, json=json.dumps(message_dict))
    thread_lock.acquire(blocking=True)
    response_list.append(resp)
    thread_lock.release()


def start_component(component, storeId, data, response_list):
    # check if service exists
    service_filter = client.services.list(filters={'name': component})
    origin_url = "http://" + data["origin"] + ":8080/results"
    service_url = "http://" + component + ":" + str(portDict[component])

    # if not exists
    if len(service_filter) == 0:
        logging.info(component + " doesn't exist")
        logging.info("Spinning up " + component + " ")

        # create the service
        component_service = client.services.create(
            "trishaire/" + component + ":latest",  # the name of the image
            name=component,  # name of service
            endpoint_spec=docker.types.EndpointSpec(
                mode="vip", ports={portDict[component]: portDict[component]}
            ),
            env=["CASS_DB=cass"],  # set environment var
            networks=['myNet'])  # set network

    count = 0

    # wait for component to spin up
    while True:
        try:
            requests.get(service_url+"/health")
        except Exception:
            if count < 15:
                logging.info(
                    "Attempt " + str(int(count / 5)) + ", " + component +
                    " is not ready"
                )
                message = "Attempting to spin up " + component
                message_dict = {"message": message}
                requests.post(origin_url, json=json.dumps(message_dict))
                sleep(5)
                count += 5
            else:
                component_service.remove()
                break
        else:
            break

    if count >= 15:
        logging.info(
            "FAILURE: " + component + " could not be debloyed "
        )
        message = "Timeout. Component " + component +\
            " of your workflow could not be deployed"
        message_dict = {"message": message}
        requests.post(origin_url, json=json.dumps(message_dict))
        resp = requests.Response()
        resp.status_code = 408
        thread_lock.acquire(blocking=True)
        response_list.append(component)
        thread_lock.release()
        return

    logging.info(
        "SUCCESS: " + component + " is healthy"
    )
    # send update to the restaurant owner
    message = "Component " + component + " of your workflow has been deployed"
    message_dict = {"message": message}
    requests.post(origin_url, json=json.dumps(message_dict))

    # send workflow_request to component
    logging.info(
        "sending " + component +
        " workflow specification"
    )
    comp_response = requests.put(
        service_url + "/workflow-requests/" + storeId,
        json=json.dumps(data)
    )
    logging.info(
        "recieved response "+str(comp_response.status_code) + " " +
        comp_response.text + " from " + component
    )

    if comp_response.status_code != 201:
        thread_lock.acquire(blocking=True)
        response_list.append(component)
        thread_lock.release()


def update_component(component, storeId, data, response_list):
    service_url = "http://" + component + ":" + str(portDict[component])

    # send workflow_request to component
    logging.info(
        "sending " + component +
        " workflow update"
    )
    comp_response = requests.put(
        service_url + "/workflow-update/" + storeId,
        json=json.dumps(data)
    )
    logging.info(
        "recieved response " + str(comp_response.status_code) +
        " " + comp_response.text + " from " + component
    )

    if comp_response.status_code != 200:
        thread_lock.acquire(blocking=True)
        response_list.append(component)
        thread_lock.release()


def stop_component(component, storeId, response_list):
    service_url = "http://" + component + ":" + str(portDict[component])

    # check if service exists
    service_filter = client.services.list(filters={'name': component})

    if len(service_filter) == 0:  # if service failed to deploy
        return  # don't send teardown

    logging.info(
        "sent teardown request to " + component
    )
    comp_response = requests.delete(
        service_url + "/workflow-requests/" + storeId,
    )
    logging.info(
        "recieved response " + str(comp_response.status_code) +
        + comp_response.text + " from " + component
    )
    thread_lock.acquire(blocking=True)
    response_list.append(comp_response)
    thread_lock.release()


@app.route("/workflow-requests/<storeId>", methods=["PUT"])
def setup_workflow(storeId):
    logging.info("{:*^74}".format(
        " PUT /workflow-requests/"
        + storeId + " "
    ))
    # get the data from the request
    data = json.loads(request.get_json())
    # verify the request is valid
    valid, mess = verify_workflow(data)

    # if invalid workflow request send back a 400 response
    if not valid:
        logging.info("workflow-request ill formatted")
        logging.info("{:*^74}".format(" Request FAILED "))
        return Response(
            status=400,
            response="workflow-request ill formatted\n" + mess
        )
    # unsuported specifications
    if data["method"] != "persistent":
        logging.info("Unsupported specifications")
        logging.info("{:*^74}".format(" Request FAILED "))
        return Response(
            status=422,
            response="Sorry, edge deployment method is not yet supported!\n" +
                     "Entity could not be processed"
        )
    # conflict
    if storeId in workflows:
        logging.info("workflow already exists")
        logging.info("{:*^74}".format(" Request FAILED "))
        return Response(
            status=409,
            response="Oops! A workflow already exists for this client!\n" +
                     "Please teardown existing workflow before deploying " +
                     "a new one"
        )

    workflows[storeId] = data

    # get the list of components for the workflow
    component_list = data["component-list"].copy()
    failed_list = start_up(storeId, data, component_list)

    if failed_list.count == 0:
        logging.info("{:*^74}".format(" Request SUCCEEDED "))
        return Response(
            status=201
        )
    else:
        teardown(storeId, component_list)
        logging.info("{:*^74}".format(" Request FAILED "))
        return Response(
            status=403,
            response="Workflow deployment failed.\n" +
                     "Invalid workflow specification"
        )


def start_up(storeId, data, component_list):
    thread_list = []
    response_list = []

    # check if the workflow request specifies cass
    has_cass = "cass" in component_list
    if has_cass:
        # remove cass from the component-list
        component_list.remove("cass")
        # startup cass first and foremost
        start_cass(data, response_list)

    # start up the rest of the components
    for comp in component_list:
        x = threading.Thread(
            target=start_component,
            args=(comp, storeId, data, response_list)
        )
        x.start()
        thread_list.append(x)

    # wait for all the threads to terminate
    for x in thread_list:
        x.join()

    return response_list


@app.route("/workflow-update", methods="PUT")
def update_workflow(storeId):
    logging.info("{:*^74}".format(
        " PUT /workflow-update/"
        + storeId + " "
    ))
    # get the data from the request
    data = json.loads(request.get_json())
    # verify the request is valid
    valid, mess = verify_workflow(data)

    # if invalid workflow request send back a 400 response
    if not valid:
        logging.info("workflow-request ill formatted")
        logging.info("{:*^74}".format(" Request FAILED "))
        return Response(
            status=400,
            response="workflow-request ill formatted\n" + mess
        )
    # unsuported specifications
    if data["method"] != "persistent":
        logging.info("Unsupported specifications")
        logging.info("{:*^74}".format(" Request FAILED "))
        return Response(
            status=422,
            response="Sorry, edge deployment method is not yet supported!\n" +
                     "Entity could not be processed"
        )
    if not (storeId in workflows):
        logging.info("workflow does not exists! Nothing to update")
        logging.info("{:*^74}".format(" Request FAILED "))
        return Response(
            status=409,
            response="Oops! A workflow does not exists for this client!\n" +
                     "Nothing to update!"
        )

    list_teardown = list(set(workflows[storeId]["component-list"]) -
                         set(data["component-list"]))
    list_start = list(set(data["component-list"]) -
                      set(workflows[storeId]["component-list"]))
    list_update = list(set(data["component-list"]).intersection(
        set(workflows[storeId]["component-list"])
    ))

    success = True

    logging.info("starting components not in previous workflow")
    failed_list = start_up(storeId, data, list_start)

    if failed_list.count != 0:
        logging.info("failed to start new components")
        teardown(storeId, list_start)
        success = False
    else:
        logging.info("updating components in previous workflow")
        failed_list = update(storeId, data, list_update)

        if failed_list.count != 0:
            logging.info("failed to update existing components")
            # get the comps that succeeded
            undo_update_list = list(set(list_update) - set(failed_list))
            # change their workflows back
            update(storeId, workflows[storeId], undo_update_list)
            # tear down the list_start components
            teardown(storeId, list_start)
            success = False
        else:
            logging.info("removing components no longer needed")
            teardown(storeId, list_teardown)

    if success:
        logging.info("{:*^74}".format(" Request SUCCEEDED "))
        return Response(
            status=200
        )
    else:
        logging.info("{:*^74}".format(" Request FAILED "))
        return Response(
            status=403,
            response="Workflow update failed.\n" +
                     "Invalid workflow specification\n" +
                     "workflow unchanged"
        )


def update(storeId, data, component_list):
    thread_list = []
    response_list = []

    # check if the workflow request specifies cass
    has_cass = "cass" in component_list
    if has_cass:
        # remove cass from the component-list
        component_list.remove("cass")
        # startup cass first and foremost
        start_cass(data, response_list)

    # start up the rest of the components
    for comp in component_list:
        x = threading.Thread(
            target=update_component,
            args=(comp, storeId, data, response_list)
        )
        x.start()
        thread_list.append(x)

    # wait for all the threads to terminate
    for x in thread_list:
        x.join()

    return response_list


# if the recource exists, remove it
@app.route("/workflow-requests/<storeId>", methods=["DELETE"])
def teardown_workflow(storeId):
    logging.info("{:*^74}".format(
        " DELETE /workflow-requests/"
        + storeId + " "
    ))
    if not (storeId in workflows):
        logging.info("Nothing to teardown")
        logging.info("{:*^74}".format(" Request FAILED "))
        return Response(
            status=404,
            response="Workflow doesn't exist. Nothing to teardown"
        )

    # get the list of components for the workflow
    component_list = workflows[storeId]["component-list"].copy()

    teardown(storeId, component_list)

    # delete the given workflow from the dictionary
    del workflows[storeId]

    logging.info("{:*^74}".format(" Request SUCCEEDED "))
    return Response(status=204)


def teardown(storeId, component_list):
    logging.info("Tearing down workflow")

    # if cass exists, remove it from the list
    if "cass" in component_list:
        component_list.remove("cass")

    thread_list = []
    response_list = []

    # remove the workflow from all components
    for comp in component_list:
        x = threading.Thread(
            target=stop_component,
            args=(comp, storeId, response_list)
        )
        x.start()
        thread_list.append(x)

    # wait for all the threads to terminate
    for x in thread_list:
        x.join()


# retrieve the specified resource, if it exists
@app.route("/workflow-requests/<storeId>", methods=["GET"])
def retrieve_workflow(storeId):
    logging.info("{:*^74}".format(
        " GET /workflow-requests/"
        + storeId + " "
    ))
    if not (storeId in workflows):
        logging.info("Nothing to retrieve")
        logging.info("{:*^74}".format(" Request FAILED "))
        return Response(
            status=404,
            response="Workflow doesn't exist. Nothing to retrieve"
        )
    else:
        logging.info("{:*^74}".format(" Request SUCCEEDED "))
        return Response(
            status=200,
            response=json.dumps(workflows[storeId])
        )


# retrieve all resources
@app.route("/workflow-requests", methods=["GET"])
def retrieve_workflows():
    logging.info("{:*^74}".format(
        " GET /workflow-requests "
    ))

    logging.info("{:*^74}".format(" Request SUCCEEDED "))
    return Response(
        status=200,
        response=json.dumps(workflows)
    )


# Health check endpoint
@app.route("/health", methods=["GET"])
def health_check():
    logging.info("{:*^74}".format(
        " GET /health "
    ))
    logging.info("{:*^74}".format(" Request SUCCEEDED "))
    return Response(status=200, response="healthy\n")
