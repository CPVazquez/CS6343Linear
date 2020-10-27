import logging
import uuid
import json
from threading import Timer

from cassandra.query import dict_factory
from cassandra.policies import RoundRobinPolicy
from cassandra.cluster import Cluster
from flask import Flask, request, Response
import pandas as pd
from fbprophet import Prophet
from datetime import date

__author__ = "Randeep Ahlawat"
__version__ = "1.0.0"
__maintainer__ = "Randeep Ahlawat"
__email__ = "randeep.ahalwat@utdallas.edu"
__status__ = "Development"

'''Component for forecasting the demand of an item and automatically restocking'''

#Flask application initialzation
app = Flask(__name__)

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s')

logger = logging.getLogger(__name__)
logging.getLogger('docker').setLevel(logging.INFO)
logging.getLogger('requests').setLevel(logging.INFO)
logging.getLogger('cassandra.cluster').setLevel(logging.ERROR)

workflows = {}

history = {}

#Connecting to Cassandra Cluster    
cass_IP = os.environ["CASS_DB"]
cluster = Cluster([cass_IP], load_balancing_policy=RoundRobinPolicy())
session = cluster.connect('pizza_grocery')

#Prepared Queries
get_item_stock_query = session.prepare("Select * from stockTracker where storeID=? and itemName=? and dateSold<=?")
get_current_stock_query = session.prepare("Select quantity from stock where storeID=? and itemName=?")
update_tracker_query = session.prepare("Update stockTracker set quantitySold=? where storeID=? and itemName=? and dateSold=?")
insert_tracker_query = session.prepare('Insert into stockTracker (storeID, itemName, quantitySold, dateSold) +'
	'VALUES (?, ?, ?, ?)')
update_tracker_query = session.prepare('UPDATE stockTracker SET quantitySold=? WHERE storeID=? AND ' + 
	'itemName=? AND dateSold=?')

def pandas_factory(colnames, rows):
	return pd.DataFrame(rows, columns=colnames)


session.row_factory = pandas_factory


def _get_ingredients_dict():
	return {
		'Dough': 0,         'SpicySauce': 0,        'TraditionalSauce': 0,  'Cheese': 0,
		'Pepperoni': 0,     'Sausage': 0,           'Beef': 0,              'Onion': 0,
		'Chicken': 0,       'Peppers': 0,           'Olives': 0,            'Bacon': 0,
		'Pineapple': 0,     'Mushrooms': 0
	}

def _aggregate_ingredients(pizza_list, ingredients):
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


def _predict_item_stocks(storeId, item_name):
	
	values = [(key, value[item_name])for key, value in history[storeId].items()]
	df = pd.DataFrame(values, columns=['ds', 'y'])
	m = Prophet()
	m.fit(df)
	future = m.make_future_dataframe(periods=1, freq='d', include_history=False)
	date = future.iloc[0,0]
	forecast = m.predict(future)
	prediction = forecast['yhat'].tolist()
	return prediction, date

  
def _asdasd_stocks(store_id, item_name, history):
	logger.info("***predicting stocks*****")
	today = date.today()
	rows = session.execute(get_item_stock_query, (store_id, item_name, today))
	df = rows._current_rows
	df = df[['datesold','quantitysold']].sort_values(['datesold'], ascending=False)	
	df = df.iloc[:history, :]
	df = df.rename(columns={'datesold':'ds', 'quantitysold':'y'})	
	m = Prophet()
	m.fit(df)
	future = m.make_future_dataframe(periods=1, freq='d', include_history=False)
	forecast = m.predict(future)
	prediction = forecast['yhat'].tolist()	
	logger.info('Auto Restock - Precdiction:: Date: {}, Quantity: {}'.format(forecast['ds'],sum(prediction)))
	return prediction, today + datetime.timedelta(days=1)


def _update_stock_tracker(ingredients, storeId, date):

	ingredient_list = ['Dough', 'Traditional Sauce']

	for ingredient in ingredient_list:
		session.execute(update_tracker_query, ingredients[ingredient], 
			storeId, ingredient, date)


def _insert_stock_tracker(ingredients, storeId, date):
	
	ingredient_list = ['Dough', 'Traditional Sauce']
	
	for ingredient in ingredient_list:
		session.execute(insert_tracker_query, storeId, ingredient,
			ingredients[ingredient], date)


def periodic_auto_restock():
	Timer(420.0, periodic_auto_restocker).start()
	items = ['Dough', 'TraditionalSauce']
        for store_id in workflows:
		for item in items:
			prediction, date = auto_restock(store_id, item, 7)
                        requests.put('http://' + worflows[store_id]['origin'] +
				'/auto-restock', json=json.dumps({"item": item,
					"prediction" : prediction, 'date': date)
		history[store_id] = {}
			

t = Timer(420.0, periodic_auto_restocker)
t.start()


def auto_restock(store_id, item_name, days):
	'''Forecasts the demand for a item in a store using previous sale data and automatically restocks.

		Parameters:
			store_id (UUID): ID of the store
			item_name (string): Name of the item
			days (int): Number of days of sale data to be used 			
		Returns:
			Prediction, Date (tuple): Prediction and Date of prediction
	'''
	logger.info("Starting Auto-Restock Store:{}, Item:{}, History:{}, Days:{}\n".format(store_id, item_name, history, days))
	
	predictions, date = _predict_item_stocks(store_id, item_name, days)
		
	return predictions, date


@app.route('/order/<storeId>', methods=['POST'])
def get_order(storeId):
	'''REST API for storing order'''

	logger.info("Received order for aggregation by Auto-Restocker\n")

	order = request.get_json()
	pizza_list = order['pizzaList']
	order_date = order['orderDate']

	new_date = False

	if order_date not in history[storeId]:
		history[storeId][order_date] = _get_ingredients_dict()
		new_date = True

	history[storeId][order_date] = _aggregate_ingredients(pizza_list, history[storeId][order_date])

	if new_date:
		_insert_stock_tracker(history[storeId][order_date], storeId, order_date)
	else:
		_update_stock_tracker(history[storeId][order_date], storeId, order_date)

	return Response(
		status=200,
		response="Order accepted and aggregated\n"
	)


@app.route('/workflow-requests/<storeId>', methods=['PUT'])
def register_workflow(storeId):
	'''REST API for registering workflow to auto-restocker service'''
    
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
	history[storeId] = {}

	logger.info("Workflow request for store::{} accepted\n".format(storeId))
	return Response(
		status=201,
		response='Valid Workflow registered to auto-restocker component\n')

    
@app.route('/workflow-requests/<storeId>', methods=['DELETE'])
def teardown_workflow(storeId):
	'''REST API for tearing down workflow for auto-restocker service'''

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
		response="Workflow removed from auto-restocker!\n"
	)

    
@app.route("/workflow-requests/<storeId>", methods=["GET"])
def retrieve_workflow(storeId):
	if not (storeId in workflows):
		logger.info('Workflow not registered to auto-restocker\n')
		return Response(
			status=404,
			response="Workflow doesn't exist. Nothing to retrieve\n"
		)
	else:
		logger.info('{} Workflow found on auto-restocker\n'.format(storeId))
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


@app.route('/health', methods=['GET'])
def health_check():
	'''REST API for checking health of task.'''

	logger.info("Checking health of auto-restocker.\n")
	return Response(status=200,response="Auto-Restocker is healthy!!\n")
 
