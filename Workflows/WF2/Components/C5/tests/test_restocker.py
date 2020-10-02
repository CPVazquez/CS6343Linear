#!/usr/bin/env python

"""The Test file for the Restocker Component for this Cloud Computing project.

This file does unit testing on the Restocker Component using Pytest and Mokito
"""
import os
import json

import flask
import pytest
import mockito
from cassandra.cluster import Cluster, Session

from src.restocker import app
import src.restocker as restocker

__author__ = "Carla Vazquez"
__version__ = "1.0.0"
__maintainer__ = "Carla Vazquez"
__email__ = "cpv150030@utdallas.edu"
__status__ = "Development"




@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_verify_restock_order():
    with open("tests/valid/valid.example.json", "r") as data:
        json_data = json.loads(data.read())
        valid, mess = restocker.verify_restock_order(json_data)
        assert valid == True
        assert mess is None

    with open("tests/invalid/invalid.array.json", "r") as data:
        json_data = json.loads(data.read())
        valid, mess = restocker.verify_restock_order(json_data)
        assert valid == False
        assert "is not of type 'array'" in mess

    with open("tests/invalid/invalid.missing_restock-list.json", "r") as data:
        json_data = json.loads(data.read())
        valid, mess = restocker.verify_restock_order(json_data)
        assert valid == False
        assert "'restock-list' is a required property" in mess
    
    with open("tests/invalid/invalid.missing_storeid.json", "r") as data:
        json_data = json.loads(data.read())
        valid, mess = restocker.verify_restock_order(json_data)
        assert valid == False
        assert "'storeID' is a required property" in mess

    with open("tests/invalid/invalid.missing_quantity.json", "r") as data:
        json_data = json.loads(data.read())
        valid, mess = restocker.verify_restock_order(json_data)
        assert valid == False
        assert "'quantity' is a required property" in mess

    with open("tests/invalid/invalid.missing_item-name.json", "r") as data:
        json_data = json.loads(data.read())
        valid, mess = restocker.verify_restock_order(json_data)
        assert valid == False
        assert "'item-name' is a required property" in mess
    
    with open("tests/invalid/invalid.additional.json", "r") as data:
        json_data = json.loads(data.read())
        valid, mess = restocker.verify_restock_order(json_data)
        assert valid == False
        assert "Additional properties are not allowed " in mess

def test_restocker_invalid(client):
    with open("tests/invalid/invalid.storeid.json", "r") as data:
        json_data = json.loads(data.read())
        resp = client.post("/restock", json=json_data)
        assert resp.status == '400 BAD REQUEST'
        assert resp.status_code == 400
        assert b"'storeID' is not in valid UUID format" in resp.data

    with open("tests/invalid/invalid.array.json", "r") as data:
        json_data = json.loads(data.read())
        resp = client.post("/restock", json=json_data)  
        assert resp.status == '400 BAD REQUEST'
        assert resp.status_code == 400
        assert b"is not of type 'array'" in resp.data
    
    with open("tests/invalid/invalid.missing_restock-list.json", "r") as data:
        json_data = json.loads(data.read())
        resp = client.post("/restock", json=json_data)  
        assert resp.status == '400 BAD REQUEST'
        assert resp.status_code == 400
        assert b"'restock-list' is a required property" in resp.data
    
    with open("tests/invalid/invalid.missing_storeid.json", "r") as data:
        json_data = json.loads(data.read())
        resp = client.post("/restock", json=json_data)  
        assert resp.status == '400 BAD REQUEST'
        assert resp.status_code == 400
        assert b"'storeID' is a required property" in resp.data

    with open("tests/invalid/invalid.missing_quantity.json", "r") as data:
        json_data = json.loads(data.read())
        resp = client.post("/restock", json=json_data)  
        assert resp.status == '400 BAD REQUEST'
        assert resp.status_code == 400
        assert b"'quantity' is a required property" in resp.data

    with open("tests/invalid/invalid.missing_item-name.json", "r") as data:
        json_data = json.loads(data.read())
        resp = client.post("/restock", json=json_data)  
        assert resp.status == '400 BAD REQUEST'
        assert resp.status_code == 400
        assert b"'item-name' is a required property" in resp.data
    
    with open("tests/invalid/invalid.additional.json", "r") as data:
        json_data = json.loads(data.read())
        resp = client.post("/restock", json=json_data)  
        assert resp.status == '400 BAD REQUEST'
        assert resp.status_code == 400
        assert b"Additional properties are not allowed " in resp.data
    

def test_health(client):
    resp = client.post("/health")
    assert resp.status_code == 200
    assert b"healthy" in resp.data
