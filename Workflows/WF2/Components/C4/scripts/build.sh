#!/bin/bash
docker build --rm -t trishaire/auto-restocker:latest .
sudo docker login
sudo docker push trishaire/auto-restocker:latest
