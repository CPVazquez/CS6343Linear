import os
import logging
import uuid
import json
import requests
from datetime import datetime
import time

from cassandra.query import dict_factory
from cassandra.cluster import Cluster
from cassandra.policies import RoundRobinPolicy
from quart import Quart, Response, request
from quart.utils import run_sync

from src.config import API_KEY

__author__ = "Randeep Ahlawat"
__version__ = "1.0.0"
__maintainer__ = "Randeep Ahlawat"
__email__ = "randeep.ahalwat@utdallas.edu"
__status__ = "Development"

'''Component for assigning the best delivery entity to an order'''

#Quart application initialzation
app = Quart(__name__)

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

count = 0
#Prepared queries
while True:
    try:
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
    except:
        count +=1 
        if count <= 5:
            time.sleep(5)
        else:
            exit()

    else:
        break



async def _convert_time_str(time):
    time = time.split()        
    if len(time) > 2:
        mins = int(time[2])
        hours = int(time[0])
    else:
        mins = int(time[0])
        hours = 0
    return hours * 60 + mins    

async def _get_time(origin, destination):
    url = URL.format(origin[0], origin[1], destination[0],
        destination[1], API_KEY)  
    def request_get():
        return requests.get(url)
    
    response = await run_sync(request_get)()      
    
    content = json.loads(response.content.decode())            
    if len(content['routes']) == 0:
        return 0 
    time = (content['routes'][0]['legs'][0]['duration']['text'])        
    return await _convert_time_str(time)
       

async def _get_delivery_time(delivery_entities, customer, store):    
    store = (store['latitude'], store['longitude'])    
    delivery_entities = [(entity['name'], (entity['latitude'],
        entity['longitude'])) for entity in delivery_entities]        
    best_time = float('inf')
    best_entity = None
    for delivery_entity in delivery_entities:        
        coordinates = delivery_entity[1]
        name = delivery_entity[0]	
        time = await _get_time(coordinates, store)                

        if time < best_time:
            best_time = time
            best_entity = name 
   	
    store_to_cust = await _get_time(store, customer)
     
    time = store_to_cust + best_time

    return time, best_entity
    

async def _get_entities(store_id):
    entities = []
    rows = session.execute(entity_query, (store_id,))
    for row in rows:
        entities.append(row)
    logger.info("in entities:{}\n".format(entities))
    return entities


async def _get_store_info(store_id):    
    row = session.execute(store_info_query, (store_id,)).one()
    return row

async def _update_order(order_id, entity, time):
    session.execute(update_order_query, (entity, time, order_id))

async def _calc_pizza_cost(ingredient_set):
    cost = 0.0
    for ingredient in ingredient_set:
        result = session.execute(select_items_query, (ingredient[0],))
        for row in result:
            cost += row['price'] * ingredient[1] 
    return cost

async def _insert_pizzas(pizza_list):
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

async def _create_order(order_dict):
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
    pizza_uuid_set = await _insert_pizzas(order_dict["pizzaList"])
    # Insert order into 'orderTable' table
    
    session.execute(
        insert_order_query, 
        (order_uuid, store_uuid, cust_name, "", pizza_uuid_set, None, pay_uuid, placed_at, True, -1)
    )
    
    # Insert order into 'orderByStore' table
    session.execute(insert_order_by_store_query, (store_uuid, placed_at, order_uuid))
    # Insert order into 'orderByCustomer' table
    session.execute(insert_order_by_customer_query, (cust_name, placed_at, order_uuid))


async def _get_next_component(store_id):
    comp_list = workflows[store_id]["component-list"].copy()
    comp_list.remove("cass")
    next_comp_index = comp_list.index("delivery-assigner") + 1
    if next_comp_index >= len(comp_list):
        return None
    return comp_list[next_comp_index]


async def _get_component_url(component, store_id):
    comp_name = component +\
        (str(workflows[store_id]["workflow-offset"]) if workflows[store_id]["method"] == "edge" else "")
    url = "http://" + comp_name + ":"
    if component == "order-verifier":
        url += "1000/order"
    elif component == "stock-analyzer":
        url += "4000/order"
    elif component == "restocker":
        url += "5000/order"
    elif component == "order-processor":
        url += "6000/order"
    return url


async def _send_order_to_next_component(url, order):
    cust_name = order["pizza-order"]["custName"]
    entity = order["assignment"]["deliveredBy"]
    eta = order["assignment"]["estimatedTime"]
    def request_post():
        return requests.post(url, json=json.dumps(order))
    
    response = await run_sync(request_post)()
    
    if response.status_code == 200:
        logging.info("{} assigned to order from {} with time of delivery {} seconds.\
            Order sent to next component.".format(entity, cust_name, time))
    else:
        logging.info("{} assigned to order from {} with time of delivery {} seconds.\
            Issue sending order to next component:".format(entity, cust_name, time))
        logging.info(response.text)
    return Response(status=response.status_code, response=response.text)


async def assign_entity(store_id, order):
    '''Assigns the best delivery entity to and order and updates orderTable in the DB.
        
           Parameters:
               store_id(string): Store ID of workflow.
               order(dict): Order dictionary.
           Returns:
               Response (object): Response object for POST Request.
    '''
      
    try:
        store_info = await _get_store_info(store_id)
    except:
        return (Response(
            status=409,
            response="Store ID not found in Database!\n" +
                     "Please request with valid store ID."   
        ),)
    try:	
        entities = await _get_entities(store_id)    
        if len(entities) == 0:
            return (Response(
                status=204,
                response="No Avaiblabe delivery entities for storeID::" + 
                         str(storeID) + "\n" +
                         "Please update delivery entities or " + 
                         "wait for entities to finish active deliveries!"            
            ),)
    except:
        return (Response(
            status=502,
            response="Entities table in database corrupted!\n" +
                     "Please recreate delivery entities table."
        ),)
    
    customer_info = (order['pizza-order']['custLocation']['lat'], order['pizza-order']['custLocation']['lon'])
   
    try:
        time, entity = await _get_delivery_time(entities, customer_info, store_info)
    except:
    
        return (Response(
            status=502,
            response="Error in Google API!\n" +
                     "Please contact admin."
            ),)
    
    order['assignment'] = {}
    order['assignment']['deliveredBy'] = entity
    order['assignment']['estimatedTime'] = time
        
    return Response(
        status=200,        
        json=json.dumps(order)
    )


@app.route('/workflow-requests/<storeId>', methods=['PUT'])
async def register_workflow(storeId):
    '''REST API for registering workflow to delivery assigner service'''
    
    data = await request.get_json()
    data = json.loads(data)

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
async def teardown_workflow(storeId):
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
async def retrieve_workflow(storeId):
    '''REST API for requesting details of registered store'''

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
async def retrieve_workflows():
    logger.info('Received request for workflows\n')
    return Response(
        status=200,
        response='worflows::' + json.dumps(workflows) + '\n'
    )


@app.route('/order', methods=['POST'])
async def assign():
    '''REST API for assigning best delivery entity.'''
 
    order = await request.get_json()
    order = json.loads(order)

    storeId = order['pizza-order']['storeId']
    storeID = uuid.UUID(storeId)

    logger.info("Request for assignment of delivery entity to order by {} for".format(
        order['pizza-order']['custName']))

    if storeId not in workflows:
        logger.info("StoreId not in workflows of delivery assigner.")
        return Response(
            status=404,
            response="Workflow ID does not seem to exist for delivery assigner!\n" +
                     "Please add delivery assigner to the Workflow or " + 
                     "create the workflow if it doesnt exist."
	)


    if 'orderId' not in order:
       order['pizza-order']['orderId'] = str(uuid.uuid4())
       await _create_order(order)
    else:
       order['pizza-order']['orderId'] = uuid.UUID(order['pizza-order']['orderId'])

        
    res = await assign_entity(storeID, order)            
   
    if res.status_code == 200: 
        try:
            await _update_order(order['pizza-order']['orderId'], order['assignment']['deliveredBy'], 
                order['assignment']['estimatedTime'])
        except:    
            logging.info("order does not exist in the database, unable to update database order")

        order['pizza-order']['orderId'] = str(order['pizza-order']['orderId'])
        component = await _get_next_component(storeId)
        if component is not None:
            url = await _get_component_url(component, storeId)
            return await _send_order_to_next_component(url, order)            
    
    return res


@app.route("/workflow-update/<storeId>", methods=['PUT'])
async def update_workflow(storeId):
    '''REST API for updating registered workflow'''

    logging.info('Update request for workflow {} to delivery assigner\n'.format(storeId))

    data = await request.get_json()
    data =  json.loads(data)

    if not ("cass" in data["component-list"]):
        logging.info("Workflow-request rejected, cass is a required workflow component\n")
        return Response(status=422, response="workflow-request rejected, cass is a required workflow component\n")

    workflows[storeId] = data

    logging.info("Workflow updated for {}\n".format(storeId))

    return Response(status=200, response="Delivery Assigner updated for {}\n".format(storeId))


@app.route('/health', methods=['GET'])
async def health_check():
    '''REST API for checking health of task.'''
    logger.info("Checking health of delivery assigner.\n")
    return Response(status=200,response="Delivery Assigner is healthy!!\n")
 
