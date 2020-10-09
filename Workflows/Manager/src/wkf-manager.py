# be able to make HTTP requests
import requests
import logging
from time import sleep
# pull the docker sdk library and setup
import docker
client = docker.from_env()

has_dockerized = False

# set up logging
logging.basicConfig(level=logging.DEBUG, 
    format='%(asctime)s - %(levelname)s - %(message)s')

# pull the flask library and initialize
from flask import Flask, request, Response
app = Flask(__name__)

# function to see if there is a database running, start it if it isn't, and then return the virtual IP
def get_or_launch_db():
    # check if database is running, and spin it up if it isn't
    running_database_services = client.services.list(filters={'name': 'cass'})
    
    # the reference to the Service
    database_service = None

    if len(running_database_services) == 0:
        logging.debug("the database doesn't exist, spin it up")
        database_service = client.services.create(
            "trishaire/cass", # the name of the image
            name="cass",
            endpoint_spec=docker.types.EndpointSpec(mode="vip", ports={ 9042 : 9042 }),
            networks=['myNet'])
    else:
        logging.debug("the database exists")
        database_service = running_database_services[0]
        
    APIclient = docker.APIClient(base_url='unix://var/run/docker.sock')

    healthy = False

    while not healthy : 
        tasks = client.services.get("cass").tasks()

        for task in tasks:
            tID = task['ID']
            result = APIclient.inspect_task(tID)['Status']['Message']
            if result == 'started':
                healthy = True    
        
        if not healthy:
            logging.debug("Cass failed health check")
            sleep(5)

    logging.debug('Cass is healthy!')

    return database_service

    # get the virtual IP of the database service, to pass to 
    #db_virtualip = database_service.attrs['Endpoint']['VirtualIPs'][1]['Addr']

    #return db_virtualip

@app.route('/dockerize', methods=['GET'])
def dockerize_function():
    #launch the db
    get_or_launch_db()
    
    sleep(10)

    # Launch component 1

    running_order_services = client.services.list(filters={'name' : 'order-verifier'})
   
    # the reference to the Service
    order_service = None

    if len(running_order_services) == 0: 
        logging.debug("the order service doesn't exist, spin it up")
        order_service = client.services.create(
            "trishaire/order-verifier",  # the name of the image
            name="order-verifier",
            endpoint_spec=docker.types.EndpointSpec(mode="vip", ports={ 1000 : 1000 }),
            env=["CASS_DB=cass"],
            networks=['myNet'])
    else: 
        logging.debug("the order service exists")
        order_service = running_order_services[0]

    logging.debug("*** ORDER SERVICE ***")
    logging.debug(order_service)

    sleep(10)

    order_response = requests.get("http://order-verifier:1000/health")

    logging.debug("*** THE RESPONSE ***")
    logging.debug(order_response)

    # launch component 3

    running_delivery_services = client.services.list(filters={'name' : 'delivery-assigner'})
   
    # the reference to the Service
    delivery_service = None

    if len(running_delivery_services) == 0: 
        logging.debug("the delivery service doesn't exist, spin it up")
        delivery_service = client.services.create(
            "trishaire/delivery-assigner",  # the name of the image
            name="delivery-assigner",
            endpoint_spec=docker.types.EndpointSpec(mode="vip", ports={ 3000 : 3000 }),
            env=["CASS_DB=cass"],
            networks=['myNet'])
    else: 
        logging.debug("the delivery service exists")
        delivery_service = running_delivery_services[0]

    logging.debug("*** DELIVERY SERVICE ***")
    logging.debug(delivery_service)

    sleep(10)

    delivery_response = requests.get("http://delivery-assigner:3000/health")

    logging.debug("*** THE RESPONSE ***")
    logging.debug(delivery_response)

    # Launch component 4

    running_auto_restocker_services = client.services.list(filters={'name' : 'auto-restocker'})
   
    # the reference to the Service
    auto_restocker_service = None

    if len(running_auto_restocker_services) == 0: 
        logging.debug("the auto restocker service doesn't exist, spin it up")
        auto_restocker_service = client.services.create(
            "trishaire/auto-restocker",  # the name of the image
            name="auto-restocker",
            endpoint_spec=docker.types.EndpointSpec(mode="vip", ports={ 4000 : 4000 }),
            env=["CASS_DB=cass"],
            networks=['myNet'])
    else: 
        logging.debug("the auto restocker service exists")
        auto_restocker_service = running_auto_restocker_services[0]

    logging.debug("*** AUTO RESTOCKER SERVICE ***")
    logging.debug(auto_restocker_service)

    sleep(10)

    auto_restocker_response = requests.get("http://auto-restocker:4000/health")

    logging.debug("*** THE RESPONSE ***")
    logging.debug(auto_restocker_response)


    # Launch component 5

    running_restocker_services = client.services.list(filters={'name' : 'restocker'})
   
    # the reference to the Service
    restocker_service = None

    if len(running_restocker_services) == 0: 
        logging.debug("the restocker service doesn't exist, spin it up")
        restocker_service = client.services.create(
            "trishaire/restocker",  # the name of the image
            name="restocker",
            endpoint_spec=docker.types.EndpointSpec(mode="vip", ports={ 5000 : 5000 }),
            env=["CASS_DB=cass"],
            networks=['myNet'])
    else: 
        logging.debug("the restocker service exists")
        restocker_service = running_restocker_services[0]

    logging.debug("*** RESTOCKER SERVICE ***")
    logging.debug(restocker_service)

    sleep(10)

    restocker_response = requests.get("http://restocker:5000/health")

    logging.debug("*** THE RESPONSE ***")
    logging.debug(restocker_response)

    to_return = "success" + order_response.text + delivery_response.text + auto_restocker_response.text + restocker_response.text

    has_dockerized = True

    return Response(status=200,response=to_return)

@app.route('/order', methods=['POST'])
def pass_on_order():
    #launch the db
    get_or_launch_db()

    if has_dockerized == False:
        dockerize_function()


    order_response = requests.post("http://order-verifier:1000/order",
            json=request.json)

    full_response = order_response.text + " *** " 
    # this means the order is correct, pass to component 3
    if order_response.status_code == 200:
        del_response = requests.post("http://delivery-assigner:3000/assign-entity",
            json=order_response.json(), headers={'Content-type': 'application/json'})
        full_response = full_response + " delivered " + del_response.text
    elif order_response.status_code == 403:
        rest_response = requests.post("http://restocker:5000/restock",
            json=order_response.json())
        full_response = full_response + " restocked " + rest_response.text
        

    logging.debug("*** THE RESPONSE ***")
    logging.debug(order_response)
    logging.debug("*** FULL RESPONSE ***")
    logging.debug(full_response)

    return Response(status=200, response=full_response)

# Health check endpoint
@app.route('/health', methods=['GET', 'POST'])
def health_check():
    return Response(status=200,response="healthy\n")

