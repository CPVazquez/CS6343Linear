# Item Auto Stocker
  Workflow 2, Component 4

## Written By
Randeep Ahlawat

## Description
  The component forecasts the demand for a particular item in a store using Facebook Prophet. It receives a store ID and an item name and predicts its sale in the upcoming days using previous sale data which acts as a history. The workflow manager can choose how long back the sale data needs to be looked at for training and for how many days the predictions need to be made. The predictions are then used to automatically restock the item. The component allows the workflow manager to use a flexible automatic restock strategy whether it be daily or weekly restock. Facebook Prophet provides accurate predictions and can even discern seasonality and yearly, weekly and daily trends.

## Setup
Machine requirements:
* Python 3.8
* Docker

Packages  
* build-essential
* python-dev
* python3-dev

Packages installed using pip:
* flask
* gunicorn
* Facebook Prophet
* Pystan
* cassandra-driver

## Commands
  * To build the docker image, use the following command in the folder containing the Dockerfile:
    ```
    docker build --rm -t trishaire/auto-restocker path_to_c1_dockerfile
    ```
  * To update Dockerhub repository:
  
    ```
    sudo docker login
    docker push trishaire/auto-restocker:tag
    ```

  * To create the image as a service run the following command:

    ```
    docker service create --name auto-restocker --network myNet --publish port:port trishaire/auto-restocker
    ```

    * Where `port` is `4000` for auto-restocker.
  
[Main README](https://github.com/CPVazquez/CS6343)
