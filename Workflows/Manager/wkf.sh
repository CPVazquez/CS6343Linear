#/bin/bash

docker run -d --name wkf-manager --env TIMEOUT='1000' --publish 8080:8080 --mount 'type=bind,src=/var/run/docker.sock,dst=/var/run/docker.sock' --mount 'type=bind,src=/var/run/docker.sock,dst=/var/run/docker.sock' --network myNet  trishaire/wkf-manager:async
