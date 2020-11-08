#!/bin/bash
docker build --rm -t trishaire/auto-restocker:linear .
sudo docker login
sudo docker push trishaire/auto-restocker:linear
