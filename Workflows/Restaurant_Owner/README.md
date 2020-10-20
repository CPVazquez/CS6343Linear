# Restaurant Owner (Client)

## Written By
Carla Vazquez

## Description
This program serves as the client for the workflow manager. It creates a workflow request and receives results from the workflow. 

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

[Main README](https://github.com/CPVazquez/CS6343)