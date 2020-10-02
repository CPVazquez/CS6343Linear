import requests
import json
from config import API_KEY
import os
import logging
import uuid
from cassandra.query import dict_factory
from cassandra.cluster import Cluster
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s')

logger = logging.getLogger(__name__)

 
URL = "https://maps.googleapis.com/maps/api/directions/json?origin={},{}&destination={},{}&key={}"

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
    
        

def get_delivery_time(delivery_entities, customer, store):    
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
    
    


ip = os.environ.get('CASSANDRA_IP')    
cluster = Cluster([ip])
session = cluster.connect('pizza_grocery')
session.row_factory = dict_factory   
order_info_query = session.prepare("Select orderedFrom, orderedBy from orderTable where orderID=?")
entity_query = session.prepare("Select name, latitude, longitude from deliveryEntitiesByStore where storeID=? and onDelivery=False ALLOW FILTERING")
store_info_query = session.prepare("Select latitude, longitude from stores where storeID=?")
customer_info_query = session.prepare("Select latitude, longitude from customers where customerName=?")

def get_entities(store_id):
    entities = []
    rows = session.execute(entity_query, (store_id,))
    for row in rows:
        entities.append(row)
    return entities

def get_order_info(order_id):
    row = session.execute(order_info_query, (order_id,)).one()
    return row

def get_store_info(store_id):
    row = session.execute(store_info_query, (store_id,)).one()
    return row

def get_customer_info(customer_name):
    row = session.execute(customer_info_query, (customer_name,)).one()
    return row


def test():
    order_id = uuid.UUID('1e803ed4-6b35-4e88-aa78-bc27847fdd1a')    
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

if __name__ == "__main__":
    #store = {'latitude':32.984363, 'longitude':-96.749689) #utd
    #customer = ('latitude':32.998323, -96.775618) #pearl on frankford
    #delivery_entities = [(32.993394, -96.768680), (32.998795, -96.734466), (32.988504, -96.770228)] #palencia, marquis, chatham
    #logger.info(get_delivery_time(store, customer, delivery_entities))
    test()
     
   
	
		
        
    
