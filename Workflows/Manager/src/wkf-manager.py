# pull the docker sdk library and setup
import docker
client = docker.from_env()

# global reference to the overlay network
overlay_network = (client.networks.list(names=['myNet']))[0]

# pull the flask library and initialize
from flask import Flask, request, Response
app = Flask(__name__)

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

@app.route('/health', methods=['GET'])
def health_check():
    return Response(status=200,response="healthy")

@app.route('/orders', methods=['GET'])
def passon_order():
    # check if database is running, and spin it up if it isn't
    running_database_services = client.services.list(filters={'name': 'cass'})

    if len(running_database_services) == 0:
        print('no database service currently running, spinning up...')
        client.services.create(
            "trishaire/cass", # the name of the image
            name="cass",
            endpoint_spec=docker.types.EndpointSpec(mode="vip", ports={ 9042 : 9042 }),
            networks=['myNet'])
    else:
        print("there is a database running, not spinning up the database")



    running_component1_services = client.services.list(filters={'name' : 'component1_service'})
    if len(running_component1_services) == 0: 
        print('no component1 service currently running, spinning up...')
#        client.services.create(
#            "trishaire/webserver", # the name of the image
#            name="component1_service",
#            endpoint_spec=docker.types.EndpointSpec(mode="vip", ports={ 9042 : 9042 }),
#            
#            )
    else: 
        print("there is a component1 running, not spinning up")

    
    return Response(status=200, response="no u")

@app.route('/')
def hello_world():
    # get the service of a specific name
    running_services = client.services.list(filters={'name' : 'test_pythonsdk_service'})
    if len(running_services) == 0:
        print("i'm gonna make a service")
        client.services.create(
                "apline:latest", # the name of the image
                name="test_pythonsdk_service",
                command="ping",
                args=["1.1.1.1"])
    else: 
        print("i already have a service")
    return Response(status=200, response="Hello, World!")
