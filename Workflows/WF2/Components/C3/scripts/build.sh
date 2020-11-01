#!/bin/bash
docker build --rm -t trishaire/delivery-assigner:latest .
sudo docker login
sudo docker push trishaire/delivery-assigner:latest
