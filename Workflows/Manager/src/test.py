import docker
client = docker.from_env()

def get_network_by_name(network_name):
    return next( x for x in client.networks.list() if x.name == network_name )

overlay_network = get_network_by_name("mynetwork")

from flask import Flask, request, Response
app = Flask(__name__)

@app.route('/dockerize/networks', methods=['GET', 'POST'])
def dockerize_networks_function():
    return Response(status=200,response=overlay_network.name)

@app.route('/dockerize', methods=['GET', 'POST'])
def dockerize_function():
    containers_list = client.containers.list()
    to_sendback = "["
    for i in containers_list: 
        to_sendback += i.name 
        to_sendback += " " 
    to_sendback += "]"
    return Response(status=200,response=to_sendback)

@app.route('/health', methods=['GET', 'POST'])
def health_check():
    return Response(status=200,response="healthy")

@app.route('/')
def hello_world():
    return "Hello, World!"
