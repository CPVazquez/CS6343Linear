#!/bin/bash
docker build --rm -t trishaire/delivery-assigner:linear .
sudo docker login
sudo docker push trishaire/delivery-assigner:linear
