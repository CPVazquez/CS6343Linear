# be able to make HTTP requests
import requests

# pull the docker sdk library and setup
import docker
client = docker.from_env()

# global reference to the overlay network
overlay_network = (client.networks.list(names=['myNet']))[0]

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
        print("the database doesn't exist, spin it up")
        database_service = client.services.create(
            "trishaire/cass", # the name of the image
            name="cass",
            endpoint_spec=docker.types.EndpointSpec(mode="vip", ports={ 9042 : 9042 }),
            networks=['myNet'])
    else:
        print("the database exists")
        database_service = running_database_services[0]

    return database_service

    # get the virtual IP of the database service, to pass to 
    #db_virtualip = database_service.attrs['Endpoint']['VirtualIPs'][1]['Addr']

    #return db_virtualip

# get the name of the network
@app.route('/dockerize/networks', methods=['GET'])
def dockerize_networks_function():
    return Response(status=200,response=overlay_network.name)

@app.route('/dockerize', methods=['GET'])
def dockerize_function():
    containers_list = client.containers.list()
    to_sendback = "["
    for i in containers_list: 
        to_sendback += i.name 
        to_sendback += " " 
    to_sendback += "]"
    return Response(status=200,response=to_sendback)

@app.route('/orders', methods=['POST'])
def pass_on_order():
    #launch the db
    get_or_launch_db()

    running_order_services = client.services.list(filters={'name' : 'order-verifier'})
   
    # the reference to the Service
    order_service = None

    if len(running_order_services) == 0: 
        print("the order service doesn't exist, spin it up")
        order_service = client.services.create(
            "trishaire/order-verifier",  # the name of the image
            name="order-verifier",
            endpoint_spec=docker.types.EndpointSpec(mode="vip", ports={ 8080 : 8080 }),
            env=["CASS_DB=cass"],
            networks=['myNet'])
    else: 
        print("the order service exists")
        order_service = running_order_services[0]

    print("*** ORDER SERVICE ***")
    print(order_service)

    order_response = requests.post("http://localhost:8080/orders",
        json=request.get_json())

    print("*** THE RESPONSE ***")
    print(order_response)

    return Response(status=200, response="no u")

# Health check endpoint
@app.route('/health', methods=['POST'])
def health_check():
    return Response(status=200,response="healthy\n")

