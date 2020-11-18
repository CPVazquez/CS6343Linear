#!/usr/bin/python3
"""Workflow Manager Component

Creates and destroys specified workflows
"""
import logging
import json
from time import sleep

import requests
import docker
import jsonschema
from quart import Quart, request, Response
from quart.utils import run_sync

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
logging.getLogger('docker').setLevel(logging.WARNING)
logging.getLogger('requests').setLevel(logging.WARNING)
logging.getLogger('quart.app').setLevel(logging.WARNING)
logging.getLogger('quart.serving').setLevel(logging.WARNING)

# # set up necessary docker clients
client = docker.from_env()
APIclient = docker.APIClient(base_url='unix://var/run/docker.sock')

# set up flask app
app = Quart(__name__)

# set up component port dictionary
portDict = {
    "order-verifier": 1000,
    "delivery-assigner": 3000,
    "cass": 2000,
    "stock-analyzer": 4000,
    "restocker": 5000,
    "order-processor": 6000
}

workflowOffset = 1

# set up workflow dict
workflows = dict()

# open workflow-request specification
with open("src/workflow-request.schema.json", "r") as schema:
    schema = json.loads(schema.read())


###############################################################################
#                           Helper Functions
###############################################################################

# check that the workflow specification json is valid
async def verify_workflow(data):
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


async def start_component(component, storeId, data, response_list):
    timeOut = False
    # check if service exists
    comp_name = component +\
        (str(data["workflow-offset"]) if data["method"] == "edge" else "")
    pubPort = portDict[component] +\
        (data["workflow-offset"] if data["method"] == "edge" else 0)
    service_filter = client.services.list(filters={'name': comp_name})
    origin_url = "http://" + data["origin"] + ":8080/results"
    cass_name = "cass" +\
        (str(data["workflow-offset"]) if data["method"] == "edge" else "")

    component_service = None

    # if not exists
    if len(service_filter) == 0:
        logging.info(comp_name + " doesn't exist")
        logging.info("Spinning up " + comp_name + " ")

        if component != "cass":
            # create the service
            component_service = client.services.create(
                "trishaire/" + component + ":async",  # the name of the image
                name=comp_name,  # name of service
                endpoint_spec=docker.types.EndpointSpec(
                    mode="vip", ports={pubPort: portDict[component]}
                ),
                env=["CASS_DB="+cass_name],  # set environment var
                networks=['myNet'])  # set network
        else:
            portCass = 9042 +\
                (data["workflow-offset"] if data["method"] == "edge" else 0)
            component_service = client.services.create(
                "trishaire/" + component + ":async",  # the name of the image
                name=comp_name,  # name of service
                endpoint_spec=docker.types.EndpointSpec(
                    mode="vip", ports={pubPort: portDict[component],
                                       portCass: 9042}
                ),
                networks=['myNet'])  # set network

    if component == "cass":
        count = await spinup_cass(component, component_service, cass_name)
        if count < 9:
            count = await spinup_component(
                component, data, origin_url, component_service
            )
    else:
        count = await spinup_component(
            component, data, origin_url, component_service
        )

    if count < 4:
        logging.info("SUCCESS: " + comp_name + " is healthy")
        # send update to the restaurant owner
        message = "Component " + comp_name +\
            " of your workflow has been deployed"
    else:
        logging.info("FAILURE: " + comp_name + " could not be deployed ")
        message = "Timeout. Component " + comp_name +\
            " of your workflow could not be deployed"
        response_list.append(component)
        timeOut = True

    def send_message():
        return requests.post(origin_url, json=json.dumps({"message": message}))

    await run_sync(send_message)()

    return timeOut


async def spinup_component(component, data, origin_url, component_service):
    count = 0
    comp_name = component +\
        (str(data["workflow-offset"]) if data["method"] == "edge" else "")
    service_url = "http://" + comp_name + ":" + str(portDict[component])

    def gethealth():
        return requests.get(service_url+"/health")

    def sleepfor5():
        sleep(5)

    def send_message():
        return requests.post(origin_url, json=json.dumps(message_dict))

    # wait for component to spin up
    while True:
        try:
            logging.debug(service_url)
            await run_sync(gethealth)()
        except Exception as ex:
            logging.debug(type(ex))
            logging.debug(ex)
            if count < 4:
                logging.info(
                    "Attempt " + str(count) + ", component " + comp_name +
                    " is not ready"
                )
                message = "Attempting to spin up " + comp_name
                message_dict = {"message": message}
                await run_sync(send_message)()
                await run_sync(sleepfor5)()
                count += 1
            else:
                component_service.remove()
                break
        else:
            break
    return count


async def spinup_cass(component, component_service, cass_name):
    healthy = False
    count = 0

    def sleepfor5():
        sleep(5)

    # keep pinging the service
    while not healthy:
        # retrieve the tasks of the cass servcie
        tasks = client.services.get(cass_name).tasks()

        # see if at least one of the tasks is healthy
        for task in tasks:
            tID = task['ID']
            result = APIclient.inspect_task(tID)['Status']['Message']
            if result == 'started':
                healthy = True

        # if none of the tasks are healthy, wait a bit before
        # trying again
        if not healthy:
            if count < 9:  # request has not timed out
                logging.info(
                    "Attempt " + str(count) + ", " + cass_name +
                    " database is not ready"
                )
                await run_sync(sleepfor5)()
                count += 1
            else:  # request timed out
                component_service.remove()
                break
    return count


async def comp_action(action, component, storeId, data, response_list=None):

    def requestPUT():
        return requests.put(
            service_url + "/workflow-requests/" + storeId,
            json=json.dumps(data)
        )

    def requestUPDATE():
        return requests.put(
            service_url + "/workflow-update/" + storeId,
            json=json.dumps(data)
        )

    def requestDELETE():
        return requests.delete(
            service_url + "/workflow-requests/" + storeId)

    # check if service exists
    comp_name = component +\
        (str(data["workflow-offset"]) if data["method"] == "edge" else "")
    service_url = "http://" + comp_name + ":" + str(portDict[component])
    service_filter = None

    if action == "teardown":
        # check if service exists
        service_filter = client.services.list(filters={'name': comp_name})
        if len(service_filter) == 0:
            return

    if action == "start":
        timeOut = await start_component(
            component, storeId, data, response_list)
        if timeOut:
            return

    # send workflow_request to component
    logging.info("sent workflow " + action + " to " + component)
    if action == "start":
        comp_response = await run_sync(requestPUT)()
    elif action == "update":
        comp_response = await run_sync(requestUPDATE)()
    else:
        comp_response = await run_sync(requestDELETE)()
        if data["method"] == "edge":
            service_filter[0].remove()
        else:  # if no other workflow is using it, remove it.
            canTearDown = True
            for store in workflows:
                if store != storeId:
                    if component in workflows[store]["component-list"]:
                        canTearDown = False
                        break
            if canTearDown:
                service_filter[0].remove()

    logging.info(
        "recieved response " + str(comp_response.status_code) +
        " " + comp_response.text + " from " + component
    )

    if (action == "update" and comp_response.status_code != 200) or\
       (action == "start" and comp_response.status_code != 201):
        response_list.append(component)


async def start_threads(action, storeId, component_list, data):
    response_list = []

    # check if the workflow request specifies cass
    if "cass" in component_list:
        # if starting
        if action == "start":
            # remove cass from the component-list
            component_list.remove("cass")
            # startup cass first and foremost
            await comp_action("start", "cass", storeId, data, response_list)

    # start threads for the rest of the components
    for comp in component_list:
        if response_list:
            break
        await comp_action(action, comp, storeId, data, response_list)

    return response_list


###############################################################################
#                           API Endpoints
###############################################################################
@app.route("/workflow-requests/<storeId>", methods=["PUT"])
async def setup_workflow(storeId):
    global workflowOffset

    logging.info("{:*^74}".format(
        " PUT /workflow-requests/"
        + storeId + " "
    ))
    # get the data from the request
    requestData = await request.get_json()
    data = json.loads(requestData)
    # verify the request is valid
    valid, mess = await verify_workflow(data)

    # if invalid workflow request send back a 400 response
    if not valid:
        logging.info("workflow-request ill formatted")
        logging.info("{:*^74}".format(" Request FAILED "))
        return Response(
            status=400,
            response="workflow-request ill formatted\n" + mess
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

    if data["method"] == "edge":
        data["workflow-offset"] = workflowOffset
        workflowOffset += 1
    workflows[storeId] = data

    # get the list of components for the workflow
    component_list = data["component-list"].copy()
    failed_list = await start_threads("start", storeId, component_list, data)

    if len(failed_list) == 0:
        logging.info("{:*^74}".format(" Request SUCCEEDED "))
        return Response(
            status=201, response="success"
        )
    else:
        component_list = data["component-list"].copy()
        await start_threads("teardown", storeId, component_list, data)
        del workflows[storeId]
        logging.info("{:*^74}".format(" Request FAILED "))
        return Response(
            status=403,
            response="Workflow deployment failed.\n" +
                     "Invalid workflow specification"
        )


@app.route("/workflow-update/<storeId>", methods=["PUT"])
async def update_workflow(storeId):
    logging.info("{:*^74}".format(
        " PUT /workflow-update/"
        + storeId + " "
    ))
    # get the data from the request
    requestData = await request.get_json()
    data = json.loads(requestData)
    # verify the request is valid
    valid, mess = await verify_workflow(data)

    # if invalid workflow request send back a 400 response
    if not valid:
        logging.info("workflow-request ill formatted")
        logging.info("{:*^74}".format(" Request FAILED "))
        return Response(
            status=400,
            response="workflow-request ill formatted\n" + mess
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

    if data["method"] == "edge":
        data["workflow-offset"] = workflows[storeId]["workflow-offset"]

    logging.info("starting components not in previous workflow")
    failed_list = await start_threads("start", storeId, list_start, data)

    if failed_list:
        logging.info("failed to start new components")
        await start_threads("teardown", storeId, list_start, data)
        success = False
    else:
        logging.info("updating components in previous workflow")
        failed_list = await start_threads("update", storeId, list_update, data)

        if failed_list:
            logging.info("failed to update existing components")
            # get the comps that succeeded
            undo_update_list = list(set(list_update) - set(failed_list))
            # change their workflows back
            await start_threads(
                "update", storeId, undo_update_list, workflows[storeId]
            )
            # tear down the list_start components
            await start_threads("teardown", storeId, list_start, data)
            success = False
        else:
            logging.info("removing components no longer needed")
            await start_threads(
                "teardown", storeId, list_teardown, workflows[storeId]
            )

    if success:
        workflows[storeId] = data
        logging.info("{:*^74}".format(" Request SUCCEEDED "))
        return Response(
            status=200, response="success"
        )
    else:
        logging.info("{:*^74}".format(" Request FAILED "))
        return Response(
            status=403,
            response="Workflow update failed.\n" +
                     "Invalid workflow specification\n" +
                     "workflow unchanged"
        )


# if the recource exists, remove it
@app.route("/workflow-requests/<storeId>", methods=["DELETE"])
async def teardown_workflow(storeId):
    logging.info("{:*^74}".format(
        " DELETE /workflow-requests/" + storeId + " "))
    if not (storeId in workflows):
        logging.info("Nothing to teardown")
        logging.info("{:*^74}".format(" Request FAILED "))
        return Response(
            status=404,
            response="Workflow doesn't exist. Nothing to teardown"
        )

    # get the list of components for the workflow
    component_list = workflows[storeId]["component-list"].copy()
    # teardown components
    await start_threads(
        "teardown", storeId, component_list, workflows[storeId])
    # delete the given workflow from the dictionary
    del workflows[storeId]

    logging.info("{:*^74}".format(" Request SUCCEEDED "))
    return Response(status=204, response="success")


# retrieve the specified resource, if it exists
@app.route("/workflow-requests/<storeId>", methods=["GET"])
async def retrieve_workflow(storeId):
    logging.info("{:*^74}".format(" GET /workflow-requests/" + storeId + " "))
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
async def retrieve_workflows():
    logging.info("{:*^74}".format(" GET /workflow-requests "))
    logging.info("{:*^74}".format(" Request SUCCEEDED "))
    return Response(
        status=200,
        response=json.dumps(workflows)
    )


# Health check endpoint
@app.route("/health", methods=["GET"])
async def health_check():
    logging.info("{:*^74}".format(" GET /health "))
    logging.info("{:*^74}".format(" Request SUCCEEDED "))
    return Response(status=200, response="healthy\n")
