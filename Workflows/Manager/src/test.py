import docker
client = docker.from_env()

from flask import Flask, request, Response
app = Flask(__name__)

@app.route('/dockerize', methods=['POST'])
def dockerize_function():
    containers_list = client.containers.list()
    to_sendback = "["
    for i in containers_list: 
        to_sendback += i.name 
        to_sendback += " " 
    to_sendback += "]"

    return Response(status=200,response=to_sendback)

@app.route('/health', methods=['POST'])
def health_check():
    return Response(status=200,response="healthy")

@app.route('/')
def hello_world():
    return "Hello, World!"
