import logging
import uuid
import json
from threading import Timer

from cassandra.query import dict_factory
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

workflows = {}

#Connecting to Cassandra Cluster    
cluster = Cluster(['cass'])
session = cluster.connect('pizza_grocery')

#Prepared Queries
get_item_stock_query = session.prepare("Select * from stockTracker where storeID=? and itemName=? and dateSold<=?")
get_current_stock_query = session.prepare("Select quantity from stock where storeID=? and itemName=?")
update_stock_query = session.prepare("Update stock set quantity=? where storeID=? and itemName=?")


def pandas_factory(colnames, rows):
	return pd.DataFrame(rows, columns=colnames)


session.row_factory = pandas_factory


def _get_current_stock(store_id, item_name):
	session.row_factory = dict_factory
	row = session.execute(get_current_stock_query, (store_id, item_name)).one()
	session.row_factory = pandas_factory
	logger.info('Auto Restock - Currect Stock:::{}'.format(row['quantity']))
	return row['quantity']
	

def _update_stock(store_id, item_name, quantity):
	session.execute(update_stock_query, (quantity, store_id, item_name))


def _predict_item_stocks(store_id, item_name, history, days):
	logger.info("***predicting stocks*****")
	today = date.today()
	rows = session.execute(get_item_stock_query, (store_id, item_name, today))
	df = rows._current_rows
	df = df[['datesold','quantitysold']].sort_values(['datesold'], ascending=False)	
	df = df.iloc[:history, :]
	df = df.rename(columns={'datesold':'ds', 'quantitysold':'y'})	
	m = Prophet()
	m.fit(df)
	future = m.make_future_dataframe(periods=days, freq='d', include_history=False)
	forecast = m.predict(future)
	prediction = forecast['yhat'].tolist()	
	logger.info('Auto Restock - Precdiction:: Date: {}, Quantity: {}'.format(forecast['ds'],sum(prediction)))
	return prediction

def periodic_auto_restock():
	Timer(420.0, periodic_auto_restocker).start()
	items = ['Dough', 'Cheese']
        for item in items:
		for store_id in workflows:
			prediction, date = auto_restock(store_id, item, 7, 1)
                        requests.put('http://' + worflows[store_id]['origin'] +
				'/auto-restock', json=json.dumps({"item": item,
					"prediction" : prediction, 'date': date)


def auto_restock(store_id, item_name, history):
	'''Forecasts the demand for a item in a store using previous sale data and automatically restocks.

		Parameters:
			store_id (UUID): ID of the store
			item_name (string): Name of the item
			history (int): Number of days of sale data to be used 
			days (int): Number of forecasted days
		Returns:
			Response (object): Response object for POST request
	'''
	logger.info("Starting Auto-Restock Store:{}, Item:{}, History:{}, Days:{}\n".format(store_id, item_name, history, days))
	
	predictions, date = _predict_item_stocks(store_id, item_name, history)
		
	return predictions, date


@app.route('/workflow-request/<storeId>', methods=['PUT'])
def register_workflow(storeId):
	'''REST API for registering workflow to auto restocker service'''
    
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
		response='Valid Workflow registered to auto-restocker component')

    
@app.route('/workflow-request/<storeId>', methods=['DELETE'])
def teardown_workflow(storeId);
	'''REST API for tearing down workflow for auto-restocker service'''

	if storeId not in workflows:
		return Response(
			status=404, 
			response="Workflow does not exist for auto-restocker!\n" +
				"Nothing to tear down."
		)
	del workflows[storeId]
    
	return Response(
		status=204,
		response="Workflow removed from auto-restocker!"
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


@app.route('/auto-restock', methods=['POST'])
def restock():'''REST API for auto-restocking an item in a store.'''
	'''REST API for auto-restocking an item in a store.'''

	data = request.get_json()
	store_id = uuid.UUID(data['store_id'])
	item_name = data['item_name']
	history = data['history']
	days = data['days']
	return auto_restock(store_id, item_name, history, days)	

	
@app.route('/health', methods=['GET'])
def health_check():
	'''REST API for checking health of task.'''

	return Response(status=200,response="healthy")

		
