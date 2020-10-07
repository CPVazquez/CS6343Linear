import os
import logging
import uuid

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

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s')

logger = logging.getLogger(__name__)

#Connecting to Cassandra Cluster
    
cluster = Cluster(['cass'])
session = cluster.connect('pizza_grocery')

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
	logger.info('Currect Stock:::{}'.format(row['quantity']))
	return row['quantity']
	


def _update_stock(store_id, item_name, quantity):
	session.execute(update_stock_query, (quantity, store_id, item_name))


def _predict_item_stocks(store_id, item_name, history, days):
	today = date.today()
	rows = session.execute(get_item_stock_query, (store_id, item_name, today))
	df = rows._current_rows
	df = df[['datesold','quantitysold']].sort_values(['datesold'], ascending=False)	
	df = df.iloc[:history, :]
	df = df.rename(columns={'datesold':'ds', 'quantitysold':'y'})
	logger.info('Training Data: {}'.format(df))
	m = Prophet()
	m.fit(df)
	future = m.make_future_dataframe(periods=days, freq='d', include_history=False)
	forecast = m.predict(future)
	prediction = forecast['yhat'].tolist()
	
	logger.info('Precdiction:: Date: {}, Quantity: {}'.format(forecast['ds'],sum(prediction)))
	return prediction


def auto_restock(store_id, item_id, history, days):
	stock = _get_current_stock(store_id, item_id)
	predictions = _predict_item_stocks(store_id, item_name, history, days)
	total_stock = sum(predictions)
	if stock < total_stock:
		_update_stock(store_id, item_name, total_stock)
		logger.info('Updated stock of Item: {} in Store: {} to {}'.format(item_name, store_id, total_stock))
	else:
		logger.info('Stock Surplus of {} available for Item: {} in Store: {}'.format(stock, item_name, store_id))
	
	

if __name__ == '__main__':
	store_id = uuid.UUID('7098813e-4624-462a-81a1-7e0e4e67631d')
	item_name = "Dough"
	auto_restock(store_id, item_name, 5, 1)
		
