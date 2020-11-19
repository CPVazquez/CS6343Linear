#!/bin/bash
docker build --rm -t trishaire/stock-analyzer:async .
sudo docker login
sudo docker push trishaire/stock-analyzer:async
