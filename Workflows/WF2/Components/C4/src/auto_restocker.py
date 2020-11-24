import logging
import uuid
import json
from threading import Timer
import os
import time
from datetime import datetime, date, timedelta

from cassandra.query import dict_factory
from cassandra.policies import RoundRobinPolicy
from cassandra.cluster import Cluster
from quart import Quart, Response, request
from quart.utils import run_sync
import pandas as pd
from fbprophet import Prophet
import requests


__author__ = "Randeep Ahlawat"
__version__ = "1.0.0"
__maintainer__ = "Randeep Ahlawat"
__email__ = "randeep.ahalwat@utdallas.edu"
__status__ = "Development"

'''Component for forecasting the demand of an item and automatically restocking'''

today = date.today() 
#Quart application initialzation
app = Quart(__name__)

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s')

logger = logging.getLogger(__name__)
logging.getLogger('docker').setLevel(logging.INFO)
logging.getLogger('requests').setLevel(logging.INFO)
logging.getLogger('cassandra.cluster').setLevel(logging.ERROR)
logging.getLogger('quart.app').setLevel(logging.WARNING)
logging.getLogger('quart.serving').setLevel(logging.WARNING)


workflows = {}

history = {}

#Connecting to Cassandra Cluster    
cass_IP = os.environ["CASS_DB"]
cluster = Cluster([cass_IP], load_balancing_policy=RoundRobinPolicy())
session = cluster.connect('pizza_grocery')

#Prepared Queries
count = 0
while True:
	try:
		get_item_stock_query = session.prepare("Select * from stockTracker \
			where storeID=? and itemName=? and dateSold<=?")
		get_current_stock_query = session.prepare("Select quantity from stock \
			where storeID=? and itemName=?")
		update_tracker_query = session.prepare("Update stockTracker \
			set quantitySold=? where storeID=? and itemName=? and dateSold=?")
		insert_tracker_query = session.prepare('Insert into stockTracker \
			(storeID, itemName, quantitySold, dateSold) values (?, ?, ?, ?)')
		
	except:
		count += 1
		if count <= 5:
			time.sleep(15)
		else:
			exit()
	else:
		break




def pandas_factory(colnames, rows):
	return pd.DataFrame(rows, columns=colnames)


session.row_factory = pandas_factory



async def _get_ingredients_dict():
	return {
		'Dough': 0,         'SpicySauce': 0,        'TraditionalSauce': 0,  'Cheese': 0,
		'Pepperoni': 0,     'Sausage': 0,           'Beef': 0,              'Onion': 0,
		'Chicken': 0,       'Peppers': 0,           'Olives': 0,            'Bacon': 0,
		'Pineapple': 0,     'Mushrooms': 0
	}

async def _aggregate_ingredients(pizza_list, ingredients):
	for pizza in pizza_list:
		if pizza['crustType'] == 'Thin':
			ingredients['Dough'] += 1
		elif pizza['crustType'] == 'Traditional':
            		ingredients['Dough'] += 2

		if pizza['sauceType'] == 'Spicy':
            		ingredients['SpicySauce'] += 1
		elif pizza['sauceType'] == 'Traditional':
			ingredients['TraditionalSauce'] += 1

		if pizza['cheeseAmt'] == 'Light':
			ingredients['Cheese'] += 1
		elif pizza['cheeseAmt'] == 'Normal':
			ingredients['Cheese'] += 2
		elif pizza['cheeseAmt'] == 'Extra':
			ingredients['Cheese'] += 3

		for topping in pizza["toppingList"]:
			ingredients[topping] += 1
	return ingredients


def _predict_item_stocks(storeId, item_name):
	
	values = [(key, value[item_name]) for key, value in history[storeId].items()]
	df = pd.DataFrame(values, columns=['ds', 'y'])
	m = Prophet()
	m.fit(df)
	future = m.make_future_dataframe(periods=1, freq='d', include_history=False)
	date = future.iloc[0,0]
	forecast = m.predict(future)
	prediction = forecast['yhat'].tolist()
	logger.info("FORECAST::\n\t{}".format(forecast.to_string().replace('\n', '\n\t')))
	return prediction, date

  
async def _predict_stocks(store_id, item_name, history, days):	
	
	rows = session.execute(get_item_stock_query, (store_id, item_name, today))
	df = rows._current_rows
	df = df[['datesold','quantitysold']].sort_values(['datesold'], ascending=False)	
	df = df.iloc[:history, :]
	df = df.rename(columns={'datesold':'ds', 'quantitysold':'y'})	
	m = Prophet()
	m.fit(df)
	future = m.make_future_dataframe(periods=days, freq='d', include_history=False)
	forecast = m.predict(future)
	predictions = forecast['yhat'].tolist()	
	dates = forecast['ds'].tolist()
	result = {date.strftime("%m/%d/%Y"): prediction for date, prediction in zip(dates, predictions)}
	
	return result


async def _update_stock_tracker(ingredients, storeId, date):

	ingredient_list = ['Dough', 'TraditionalSauce']
	
	for ingredient in ingredient_list:
		session.execute(update_tracker_query, (ingredients[ingredient], 
			storeId, ingredient, date))


async def _insert_stock_tracker(ingredients, storeId, date):
	
	ingredient_list = ['Dough', 'TraditionalSauce']
	
	for ingredient in ingredient_list:
		session.execute(insert_tracker_query, (storeId, ingredient,
			ingredients[ingredient], date))

async def _get_next_component(store_id):
	comp_list = workflows[store_id]["component-list"].copy()
	comp_list.remove("cass")
	next_comp_index = comp_list.index("stock-analyzer") + 1
	if next_comp_index >= len(comp_list):
		return None
	return comp_list[next_comp_index]


async def _get_component_url(component, store_id):
	comp_name = component +\
		(str(workflows[store_id]["workflow-offset"]) if workflows[store_id]["method"] == "edge" else "")
	url = "http://" + comp_name + ":"
	if component == "order-verifier":
		url += "1000/order"
	elif component == "delivery-assigner":
		url += "3000/order"
	elif component == "restocker":
		url += "5000/order"
	elif component == "order-processor":
		url += "6000/order"
	return url


async def _send_order_to_next_component(url, order):

	cust_name = order["pizza-order"]["custName"]
	def request_post():
		return requests.post(url, json=json.dumps(order))
	response = await run_sync(request_post)()
	    
	if response.status_code == 200:
		logging.info("Order from {} aggregated.\
			Order sent to next component.".format(cust_name))		
	else:
		logging.info("Order from {} aggregated.\
			Issue sending order to next component:".format(cust_name))
		logging.info(response.text)

	return Response(status=response.status_code, response=response.text)


def periodic_auto_restock():
	'''Function to periodically predict weekly sales for items'''
	
	logger.info("Weekly analysis of items initiating\n")
	global today	
	Timer(420.0, periodic_auto_restock).start()
	items = ['Dough', 'TraditionalSauce']
	for store_id in workflows:
		for item in items:
			prediction, date = _predict_item_stocks(store_id, item)
			logger.info("Prediction for item::{}, for date::{} for store::{} ::".format(
				item, date, store_id, prediction))
			requests.post('http://' + workflows[store_id]['origin'] + ':8080/results',
				json=json.dumps({"message": {"item": item, "prediction": prediction,
				'date': date.strftime("%m/%d/%Y")}}))
		history[store_id] = {}
	today = today + timedelta(days=7)
			
t = Timer(420.0, periodic_auto_restock)
t.start()


@app.route('/predict-stocks/<storeId>', methods=['GET'])
async def predict_stocks(storeId):
	'''REST API for requesting future sales of an item'''

	data = request.get_json()
	data = json.loads(data)

	logger.info("Received request by {} for predicting sales for" +
		"{} using {} days for the next {} days\n".format(
			storeId, data['itemName'], data['history'], data['days']
	))

	storeID = uuid.UUID(storeId)
	
	result = await _predict_stocks(storeID, data['itemName'], data['history'], data['days'])
	logger.info("Predictions for item {}, for storeId {}::{}".format(
		data['itemName'], storeId, result))

	return Response(
		status=200,
		response=json.dumps(result)
	)


@app.route('/order', methods=['POST'])
async def get_order():
	'''REST API for storing order'''
	
	start = time.time()	
	order = await request.get_json()
	order = json.loads(order)
	storeId = order['pizza-order']['storeId']
	storeID = uuid.UUID(storeId)
	pizza_list = order['pizza-order']['pizzaList']
	order_date = datetime.strptime(order['pizza-order']["orderDate"], '%Y-%m-%dT%H:%M:%S').date()

	logger.info("Received order from {} for aggregation by stock-analyzer\n".format(order['pizza-order']['custName']))

	new_date = False
		
	if order_date not in history[storeId]:
		history[storeId][order_date] = await _get_ingredients_dict()		
		new_date = True
			
	history[storeId][order_date] = await _aggregate_ingredients(pizza_list, history[storeId][order_date])
	
	
	if new_date:		
		await _insert_stock_tracker(history[storeId][order_date], storeID, order_date)
	else:
		await _update_stock_tracker(history[storeId][order_date], storeID, order_date)
	
	component = await _get_next_component(storeId)
	end = time.time() - start
	order['stock-analyzer_execution_time'] = end
	if component is not None:
		url = await _get_component_url(component, storeId)
		res =  await _send_order_to_next_component(url, order)
		if res.status_code == 200 or res.status_code == 208:			
			return res 
		
		else:
			order.update({"error": {"status-code": res.status_code, "text": res.text}})
			return Response(
				status=208,
				response=json.dumps(order))
	return Response(
		status=200,
		response=json.dumps(order)
	)


@app.route('/workflow-requests/<storeId>', methods=['PUT'])
async def register_workflow(storeId):
	'''REST API for registering workflow to stock-analyzer service'''
    
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

	if not ("cass" in data["component-list"]):
		logging.info("Workflow-request rejected, cass is a required workflow component\n")
		return Response(status=422, response="workflow-request rejected, cass is a required workflow component\n")

	workflows[storeId] = data
	history[storeId] = {}

	logger.info("Workflow request for store::{} accepted\n".format(storeId))
	return Response(
		status=201,
		response='Valid Workflow registered to stock-analyzer component\n')

    
@app.route('/workflow-requests/<storeId>', methods=['DELETE'])
async def teardown_workflow(storeId):
	'''REST API for tearing down workflow for stock-analyzer service'''
	
	logger.info('Received teardown request for store::{}\n'.format(storeId))

	if storeId not in workflows:
		logger.info('Nothing to tear down, store::{} does not exist\n'.format(storeId))
		return Response(
			status=404, 
			response="Workflow does not exist for delivery assigner!\n" +
			"Nothing to tear down.\n"
		)
	
	del workflows[storeId]
	del history[storeId]    

	logger.info('Store::{} deleted!!\n'.format(storeId))
	return Response(
		status=204,
		response="Workflow removed from stock-analyzer!\n"
	)

    
@app.route("/workflow-requests/<storeId>", methods=["GET"])
async def retrieve_workflow(storeId):
	
	if not (storeId in workflows):
		logger.info('Workflow not registered to stock-analyzer\n')
		return Response(
			status=404,
			response="Workflow doesn't exist. Nothing to retrieve\n"
		)
	else:
		logger.info('{} Workflow found on stock-analyzer\n'.format(storeId))
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


@app.route("/workflow-update/<storeId>", methods=['PUT'])
async def update_workflow(storeId):
    '''REST API for updating registered workflow'''

    logging.info('Update request for workflow {} to stock analyzer\n'.format(storeId))

    data = await request.get_json()
    data = json.loads(data)

    if not ("cass" in data["component-list"]):
        logging.info("Workflow-request rejected, cass is a required workflow component\n")
        return Response(status=422, response="workflow-request rejected, cass is a required workflow component\n")

    workflows[storeId] = data

    logging.info("Workflow updated for {}\n".format(storeId))

    return Response(status=200, response="Stock-Analyzer updated for {}\n".format(storeId))


@app.route('/health', methods=['GET'])
async def health_check():
	'''REST API for checking health of task.'''

	logger.info("Checking health of stock-analyzer.\n")
	return Response(status=200,response="stock-analyzer is healthy!!\n")
 
