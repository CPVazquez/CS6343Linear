#!/bin/bash
docker build --rm -t trishaire/delivery-assigner:async .
sudo docker login
sudo docker push trishaire/delivery-assigner:async
