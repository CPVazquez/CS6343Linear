#/bin/bash

docker service create --name wkf-manager --publish 8080:8080 --mount 'type=bind,src=/var/run/docker.sock,dst=/var/run/docker.sock' --constraint=node.hostname==cluster1-1.utdallas.edu trishaire/wkf-manager 

