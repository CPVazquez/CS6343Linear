import os
import logging
import uuid
import json

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

#Google API URL
URL = "https://maps.googleapis.com/maps/api/directions/json?origin={}, {}&destination={},{}&key={}"

#Connecting to Cassandra Cluster
    
cass_IP = os.environ["CASS_DB"]
cluster = Cluster([cass_IP])
session = cluster.connect('pizza_grocery')
session.row_factory = dict_factory   

#Prepared queries
order_info_query = session.prepare("Select orderedFrom, orderedBy from orderTable where orderID=?")
entity_query = session.prepare("Select name, latitude, longitude from deliveryEntitiesByStore where storeID=? and onDelivery=False ALLOW FILTERING")
store_info_query = session.prepare("Select latitude, longitude from stores where storeID=?")
customer_info_query = session.prepare("Select latitude, longitude from customers where customerName=?")
verify_order_query = session.prepare("Select * from orderTable where orderID=?")
update_order_query = session.prepare("Update orderTable set deliveredBy=?, estimatedDeliveryTime=? where orderID=?")


def _get_order_ids():
    rows = session.execute("Select orderID from orderTable")
    for row in rows:
        logger.info("Order ID::{}".format(row['orderid']))

if __name__ == "__main__":
    _get_order_ids()

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
    customer =  (customer['latitude'], customer['longitude'])
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
    

def _verify_order(order_id):
    row = session.execute(verify_order_query, (order_id,)).one()
    logger.info("Updated Order :: {}".format(row))

def _update_order(order_id, entity, time):
    session.execute(update_order_query, (entity, time, order_id))

def _get_entities(store_id):
    entities = []
    rows = session.execute(entity_query, (store_id,))
    for row in rows:
        entities.append(row)
    return entities

def _get_order_info(order_id):
    row = session.execute(order_info_query, (order_id,)).one()
    return row

def _get_store_info(store_id):
    row = session.execute(store_info_query, (store_id,)).one()
    return row

def _get_customer_info(customer_name):
    row = session.execute(customer_info_query, (customer_name,)).one()
    return row


def assign_entity(order_id):
    '''Assigns the best delivery entity to and order and updates orderTable in the DB.
        
           Parameters:
               order-id (UUID): OrderId for requested order.
           Returns:
               Response (object): Response object for POST Request.
    '''

    try:
        order_info = _get_order_info(order_id)  
        store_info = _get_store_info(order_info['orderedfrom'])
        entities = _get_entities(order_info['orderedfrom'])    
        customer_info = _get_customer_info(order_info['orderedby'])
    except:
        return Response(status=400, response="Wrong order ID inputted")
    try:
        time, entity = _get_delivery_time(entities, customer_info, store_info)
    except:
        return Response(status=500, reponse="Google API unresponsive")

    logger.info('Best Time ::{}'.format(time))
    logger.info('Best Entity::{}'.format(entity))	
    update_order(order_id, entity, time)
    return Response(status=200, response="For Order ID: {}, Selected Entity: {}, Estimated Time: {}".format(order_id, entity, time))


@app.route('/assign-entity', methods=['POST'])
def assign():
    '''REST API for assigning best delivery entity.'''

    data = request.get_json()
    order_id = uuid.UUID(data['order_id'])
    logger.info('Order ID :: {}'.format(order_id))
    return assign_entity(order_id)


@app.route('/health', methods=['GET'])
def health_check():
    '''REST API for checking health of task.'''

    return Response(status=200,response="healthy")


def _test():
    order_id = session.execute("Select orderID from orderTable").one()['orderid']
    order_info = get_order_info(order_id)  
    store_info = get_store_info(order_info['orderedfrom'])
    entities = get_entities(order_info['orderedfrom'])    
    customer_info = get_customer_info(order_info['orderedby'])
    logger.info('Entities :: {}'.format(entities))
    logger.info('Order Info :: {}'.format(order_info))
    logger.info('Store info :: {}'.format(store_info))		
    logger.info('Customer Info :: {}'.format(customer_info))

    time, entity = get_delivery_time(entities, customer_info, store_info)
    logger.info('Best Time ::{}'.format(time))
    logger.info('Best Entity::{}'.format(entity))	
    verify_order(order_id)

     
   
	
		
        
    
