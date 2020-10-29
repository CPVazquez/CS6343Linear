import os
import logging
import uuid
import json
import requests

from cassandra.query import dict_factory
from cassandra.cluster import Cluster
from cassandra.policies import RoundRobinPolicy
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
                    format='%(asctime)s ' + 
                        '%(levelname)-8s %(message)s')

logger = logging.getLogger(__name__)
logging.getLogger('docker').setLevel(logging.INFO)
logging.getLogger('requests').setLevel(logging.INFO)
logging.getLogger('cassandra.cluster').setLevel(logging.ERROR)


workflows = {}

#Google API URL
URL = "https://maps.googleapis.com/maps/api/directions/json?origin={}, " + "{}&destination={},{}&key={}"

#Connecting to Cassandra Cluster
    
cass_IP = os.environ["CASS_DB"]
cluster = Cluster([cass_IP], load_balancing_policy=RoundRobinPolicy())
session = cluster.connect('pizza_grocery')
session.row_factory = dict_factory   

#Prepared queries
entity_query = session.prepare("Select name, latitude, longitude from " + 
    "deliveryEntitiesByStore where storeID=? and " +
    "onDelivery=False ALLOW FILTERING")
store_info_query = session.prepare("Select latitude, " + 
    "longitude from stores where storeID=?")
update_order_query = session.prepare("Update orderTable set deliveredBy=?, " + 
    "estimatedDeliveryTime=? where orderID=?")
select_items_query = session.prepare('Select * from items where name=?')
insert_pizzas_query = session.prepare("Insert into pizzas " + 
    "(pizzaID, toppings, cost) values (?, ?, ?)")
insert_customers_query = session.prepare("Insert into customers " +
    "(customerName, latitude, longitude) values (?, ?, ?)")
insert_payments_query = session.prepare("Insert into payments " +
    "(paymentToken, method) values (?, ?)")
insert_order_query = session.prepare("Insert into orderTable " +
    "(orderID, orderedFrom, orderedBy, deliveredBy, containsPizzas, " +
    "containsItems, paymentID, placedAt, active, estimatedDeliveryTime) " +
    "values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)")
insert_order_by_store_query = session.prepare("Insert into orderByStore (orderedFrom, " +
    "placedAt, orderID) values (?, ?, ?)")
insert_order_by_customer_query = session.prepare("Insert into orderByCustomer (orderedBy, " +
    "placedAt, orderID) values (?, ?, ?)")


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
    url = URL.format(origin[0], origin[1], destination[0],
        destination[1], API_KEY)        
    response = requests.get(url)
    content = json.loads(response.content.decode())            
    
    time = (content['routes'][0]['legs'][0]['duration']['text'])        
    return _convert_time_str(time)
       

def _get_delivery_time(delivery_entities, customer, store):    
    store = (store['latitude'], store['longitude'])    
    delivery_entities = [(entity['name'], (entity['latitude'],
        entity['longitude'])) for entity in delivery_entities]        
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

def _update_order(order_id, entity, time):
    session.execute(update_order_query, (entity, time, order_id))

def _calc_pizza_cost(ingredient_set):
    cost = 0.0
    for ingredient in ingredient_set:
        result = session.execute(select_items_query, (ingredient[0],))
        for (name, price) in result:
            cost += price * ingredient[1] 
    return cost

def _insert_pizzas(pizza_list):
    pizza_uuid_set = set()

    for pizza in pizza_list:
        pizza_uuid = uuid.uuid4()
        pizza_uuid_set.add(pizza_uuid)
        ingredient_set = set()

        if pizza["crustType"] == "Thin":
            ingredient_set.add(("Dough", 1))
        elif pizza["crustType"] == "Traditional":
            ingredient_set.add(("Dough", 2))

        if pizza["sauceType"] == "Spicy":
            ingredient_set.add(("SpicySauce", 1))
        elif pizza["sauceType"] == "Traditional":
            ingredient_set.add(("TraditionalSauce", 1))

        if pizza["cheeseAmt"] == "Light":
            ingredient_set.add(("Cheese", 1))
        elif pizza["cheeseAmt"] == "Normal":
            ingredient_set.add(("Cheese", 2))
        elif pizza["cheeseAmt"] == "Extra":
            ingredient_set.add(("Cheese", 3))

        for topping in pizza["toppingList"]:
            ingredient_set.add((topping, 1))
        
        cost = _calc_pizza_cost(ingredient_set)
        session.execute(insert_pizzas_query, (pizza_uuid, ingredient_set, cost))
    
    return pizza_uuid_set

def _create_order(order_dict):
    order_uuid = uuid.UUID(order_dict["orderId"])
    store_uuid = uuid.UUID(order_dict["storeId"])
    pay_uuid = uuid.UUID(order_dict["paymentToken"])
    cust_name = order_dict["custName"]
    cust_lat = order_dict["custLocation"]["lat"]
    cust_lon = order_dict["custLocation"]["lon"]
    placed_at = datetime.strptime(order_dict["orderDate"], '%Y-%m-%dT%H:%M:%S')

    # Insert customer information into 'customers' table
    session.execute(insert_customers_query, (cust_name, cust_lat, cust_lon))
    # Insert order payment information into 'payments' table
    session.execute(insert_payments_query, (pay_uuid, order_dict["paymentTokenType"]))  
    # Insert the ordered pizzas into 'pizzas' table
    pizza_uuid_set = _insert_pizzas(order_dict["pizzaList"])
    # Insert order into 'orderTable' table
    session.execute(
        insert_order_query, 
        (order_uuid, store_uuid, cust_name, "", pizza_uuid_set, None, pay_uuid, placed_at, True, -1)
    )
    # Insert order into 'orderByStore' table
    session.execute(insert_order_by_store_query, (store_uuid, placed_at, order_uuid))
    # Insert order into 'orderByCustomer' table
    session.execute(insert_order_by_customer_query, (cust_name, placed_at, order_uuid))


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
                         "Please update delivery entities or " + 
                         "wait for entities to finish active deliveries!"            
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
    logger.info("For order of Customer {} to store {}, Delivery Entity::{}, " +
        "Estimated Time::{} mins.".format(
        order['custName'], storeId, entity, time
    ))

    response_json = {
        "custName": order['custName'],        
        "deliveredBy": entity,
        "estimatedTime": time
    }

    return Response(
        status=200,
        mimetype='application/json',
        response=json.dumps(response_json)
    )


@app.route('/workflow-requests/<storeId>', methods=['PUT'])
def register_workflow(storeId):
    '''REST API for registering workflow to delivery assigner service'''
    
    data = request.get_json()

    logger.info("Received workflow request for store::{},\nspecs:{}\n".format(
        storeId, data))

    if storeId in workflows:
        logger.info("Workflow for store::{} already registered!!\nRequest Denied.\n".format(
            storeId))
        return Response(
            status=409,
            response="Oops! A workflow already exists for this client!\n" +
                     "Please teardown existing workflow before deploying " +
                     "a new one\n"
        )
    
    workflows[storeId] = data

    logger.info("Workflow request for store::{} accepted\n".format(storeId))
    return Response(
        status=201,
        response='Valid Workflow registered to delivery assigner component\n')

    
@app.route('/workflow-requests/<storeId>', methods=['DELETE'])
def teardown_workflow(storeId):
    '''REST API for tearing down workflow for delivery assigner service'''
    logger.info('Received teardown request for store::{}\n'.format(storeId))
    if storeId not in workflows:
        logger.info('Nothing to tear down, store::{} does not exist\n'.format(storeId))
        return Response(
            status=404, 
            response="Workflow does not exist for delivery assigner!\n" +
                     "Nothing to tear down.\n"
        )

    del workflows[storeId]
    
    logger.info('Store::{} deleted!!\n'.format(storeId))
    return Response(
        status=204,
        response="Workflow removed from delivery assigner!\n"
    )

    
@app.route("/workflow-requests/<storeId>", methods=["GET"])
def retrieve_workflow(storeId):
    if not (storeId in workflows):
        logger.info('Workflow not registered to delivery-assigner\n')
        return Response(
            status=404,
            response="Workflow doesn't exist. Nothing to retrieve\n"
        )
    else:
        logger.info('{} Workflow found on delivery-assigner\n'.format(storeId))
        return Response(
            status=200,
            response=json.dumps(workflows[storeId]) + '\n'
        )


@app.route("/workflow-requests", methods=["GET"])
def retrieve_workflows():
    logger.info('Received request for workflows\n')
    return Response(
        status=200,
        response='worflows::' + json.dumps(workflows) + '\n'
    )


@app.route('/assign-entity/<storeId>', methods=['GET'])
def assign(storeId):
    '''REST API for assigning best delivery entity.'''

    if storeId not in workflows:
        logger.info("StoreId not in workflows of delivery assigner.")
        return Response(
            status=404,
            response="Workflow ID does not seem to exist for delivery assigner!\n" +
                     "Please add delivery assigner to the Workflow or " + 
                     "create the workflow if it doesnt exist."
	)
    order = request.get_json()   
    if orderId not in order:
       order['orderId'] = uuid.uuid4()       
       _create_order(order)

    store_id = uuid.UUID(storeId)    
    entity, time, response = assign_entity(store_id, order)            

    
    try:
        _update_order(order['orderId'], entity, time)
    except:
        return Response(
            status=509,
            response="Unable to update order with delivery entity and estimated time!" +
                         "Order does not exist."
        )
    return response


@app.route('/health', methods=['GET'])
def health_check():
    '''REST API for checking health of task.'''
    logger.info("Checking health of delivery assigner.\n")
    return Response(status=200,response="Delivery Assigner is healthy!!\n")
 
