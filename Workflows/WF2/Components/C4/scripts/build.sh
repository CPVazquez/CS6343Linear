#!/bin/bash
docker build --rm -t trishaire/stock-analyzer:linear .
sudo docker login
sudo docker push trishaire/stock-analyzer:linear
