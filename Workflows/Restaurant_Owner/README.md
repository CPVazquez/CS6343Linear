# Restaurant Owner (Client)

## Written By
Carla Vazquez

## Description
This program serves as the client for the workflow manager. It creates a workflow request and receives results from the workflow. 

Upon start up it will assign itself a randomly generated UUID to act as the store's ID. 

Then it will present a menu of options. 

0. Exit

    this option sends a workflow teardown request to the workflow manager and exits the program

1. Send workflow request

    this option will prompt the user for workflow deployment method and a list of components, then it sends this specification to the workflow manager

2. Update existing workflow

    this option prompts the user for the new list of components and sends an update request to the wkf-manager

3. Teardown workflow

    this option sends a workflow teardown request to the workflow manager

4. Get workflow

    this option retrieves the workflow specification from the workflow manager

5. Get all workflows

    this option retireves all active workflow specifications form the workflow manager

6. Get prediction

    this option attempts to make a prediction request from the predictor component

## Setup
Machine requirements:
* Python 3

Package requirements:
* pipenv

Packages installed on pipenv virtual environment:
* flask
* requests

## Commands

```
python3 generate_workflow_request.py
```

## Endpoints

### `POST /results`

An endpoint for the client to receive workflow results.

#### Body

| field | type | required | description |
|-------|------|----|---|
| message| string | true | the result that the client is receiving|

#### Responses
| status code | status | meaning|
|---|---|---|
|200| OK | message received|

### `GET /health`

#### Responses
| status code | status | meaning|
|---|---|---|
|200| OK | the server is up and running|

returns string `healthy` if the service is healthy

[Main README](https://github.com/CPVazquez/CS6343Linear)