import os
import logging
import uuid
import json
import requests

from cassandra.query import dict_factory
from cassandra.cluster import Cluster
from flask import Flask, request, Response

from src.config import API_KEY

__author__ = "Randeep Ahlawat"
__version__ = "1.0.0"
__maintainer__ = "Randeep Ahlawat"
__email__ = "randeep.ahalwat@utdallas.edu"
__status__ = "Development"

'''Component for assigning the best delivery entity to an order'''

#Flask application initialzation
app = Flask(__name__)

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s')

logger = logging.getLogger(__name__)

workflows = {}

#Google API URL
URL = "https://maps.googleapis.com/maps/api/directions/json?origin={}, {}&destination={},{}&key={}"

#Connecting to Cassandra Cluster
    
cass_IP = os.environ["CASS_DB"]
cluster = Cluster([cass_IP])
session = cluster.connect('pizza_grocery')
session.row_factory = dict_factory   

#Prepared queries
entity_query = session.prepare("Select name, latitude, longitude from deliveryEntitiesByStore where storeID=? and onDelivery=False ALLOW FILTERING")
store_info_query = session.prepare("Select latitude, longitude from stores where storeID=?")


def _convert_time_str(time):
    time = time.split()        
    if len(time) > 2:
        mins = int(time[2])
        hours = int(time[0])
    else:
        mins = int(time[0])
        hours = 0
    return hours * 60 + mins    

def _get_time(origin, destination):
    url = URL.format(origin[0], origin[1], destination[0], destination[1], API_KEY)        
    response = requests.get(url)
    content = json.loads(response.content.decode())            
    
    time = (content['routes'][0]['legs'][0]['duration']['text'])        
    return _convert_time_str(time)
       

def _get_delivery_time(delivery_entities, customer, store):    
    store = (store['latitude'], store['longitude'])    
    delivery_entities = [(entity['name'], (entity['latitude'], entity['longitude'])) for entity in delivery_entities]        
    best_time = float('inf')
    best_entity = None
    for delivery_entity in delivery_entities:        
        coordinates = delivery_entity[1]
        name = delivery_entity[0]	
        time = _get_time(coordinates, store)                

        if time < best_time:
            best_time = time
            best_entity = name 
    
    time = _get_time(store, customer) + best_time    

    return time, best_entity
    

def _get_entities(store_id):
    entities = []
    rows = session.execute(entity_query, (store_id,))
    for row in rows:
        entities.append(row)
    logger.info("in entities:{}\n".format(entities))
    return entities


def _get_store_info(store_id):    
    row = session.execute(store_info_query, (store_id,)).one()
    return row


def assign_entity(store_id, order):
    '''Assigns the best delivery entity to and order and updates orderTable in the DB.
        
           Parameters:
               store_id(string): Store ID of workflow.
               order(dict): Order dictionary.
           Returns:
               Response (object): Response object for POST Request.
    '''
      
    try:
        store_info = _get_store_info(store_id)
    except:
        return Response(
            status=409,
            response="Store ID not found in Database!\n" +
                     "Please request with valid store ID."   
        )
    try:	
        entities = _get_entities(store_id)    
        if len(entities) == 0:
            return Response(
                status=204,
                response="No Avaiblabe delivery entities for storeID::" + 
                         str(storeID) + "\n" +
                         "Please update delivery entities or wait for entities to finish active deliveries!"            
            )
    except:
        return Response(
            status=502,
            response="Entities table in database corrupted!\n" +
                     "Please recreate delivery entities table."
        )
    
    customer_info = (order['custLocation']['lat'], order['custLocation']['long'])
   
    try:
        time, entity = _get_delivery_time(entities, customer_info, store_info)
    except:
        return Response(
            status=502,
            response="Error in Google API!\n" +
                     "Please contact admin."
            )

    order['deliveredBy'] = entity
    order['estimatedTime'] = time

    return Response(status=200, mimetype='application/json', response=json.dumps(order))


@app.route('/workflow-request/<storeId>', methods=['PUT'])
def register_workflow(storeId):
    '''REST API for registering workflow to delivery assigner service'''
    
    data = request.get_json()

    if storeId in workflows:
        return Response(
            status=409,
            response="Oops! A workflow already exists for this client!\n" +
                     "Please teardown existing workflow before deploying " +
                     "a new one"
        )
    
    workflows[storeID] = data

    return Response(
        status=201,
        response='Valid Workflow registered to delivery assigner component')

    
@app.route('/workflow-request/<storeId>', methods=['DELETE'])
def teardown_workflow(storeId);
    '''REST API for tearing down workflow for delivery assigner service'''

    if storeId not in workflows:
        return Response(
            status=404, 
            response="Workflow does not exist for delivery assigner!\n" +
                     "Nothing to tear down."
        )
    del workflows[storeId]
    
    return Response(
        status=204,
        response="Workflow removed from delivery assigner!"
    )

    
@app.route("/workflow-requests/<storeId>", methods=["GET"])
def retrieve_workflow(storeId):
    if not (storeId in workflows):
        return Response(
            status=404,
            response="Workflow doesn't exist. Nothing to retrieve"
        )
    else:
        return Response(
            status=200,
            response=json.dumps(workflows[storeId])
        )


@app.route("/workflow-requests", methods=["GET"])
def retrieve_workflows():
    return Response(
        status=200,
        response=json.dumps(workflows)
    )


@app.route('/assign-entity/<storeId>', methods=['GET'])
def assign(storeId):
    '''REST API for assigning best delivery entity.'''

    if storeId not in workflows:
        return Response(
            status=404,
            response="Workflow ID does not seem to exist for delivery assigner!\n" +
                     "Please add delivery assigner to the Workflow or create the workflow " +
                     "if it doesnt exist."
    order = request.get_json()
    store_id = uuid.UUID(storeId)    
    response = assign_entity(store_id, order)        
    return response


@app.route('/health', methods=['GET'])
def health_check():
    '''REST API for checking health of task.'''

    return Response(status=200,response="Delivery Assigner is healthy!!")
 
