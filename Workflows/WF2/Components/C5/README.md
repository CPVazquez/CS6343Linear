# Restocker

## Written By
Carla Patricia Vazquez, Christopher Michael Scott

## Description
This component recieves restocking orders sent to the workflow manager. The restock orders follow the format of the restock-order.shema.json file in the shema folder. The component also scans the database every 5 minutes to check for items that might need to be restocked.

## Setup
Machine requirements:
* Python 3.8
* Docker

Package requirements:
* pipenv

Packages installed on pipenv virtual environment:
* flask
* gunicorn
* jsonschema
* uuid
* cassandra-driver
* docker
* pytest
* mockito
* pytest-cov

## Commands
  * To build the image:
    ```
    docker build --rm -t trishare/restocker:tag path_to_c5_dockerfile
    ```
  * To update the repository:
    ```
    sudo docker login
    docker push trishaire/restocker:tag
    ```
  * To create the service type the following command:
    ```
    docker service create --name restocker --network myNet --publish 5000:5000 --env CASS_DB=VIP_of_Cass_Service trishaire/restocker:tag
    ```
    * Where `VIP_of_Cass_Service` is the VIP of `myNet` overlay network.

To run localy, ensure these environment variables `CASS_DB=0.0.0.0` and `FLASK_ENV=development` are set.

## Testing
This component uses pytest to run unit test. you must be connected to a cassandra instance to run the tests correctly. I'm still trying to figure out how to mock cassandra. 

Use the following command to run tests:
```
pytest --cov=src tests
```
[Main README](https://github.com/CPVazquez/CS6343)