# Cass

## Written By
Carla Patricia Vazquez

## Description
This is the database component for both workflow mangers. It gets cql requests from several other components. It uses the official docker image for Cassandra as a base and loads our keyspace (database) on to it.

## Setup
Machine requirements:
* Python 3.8
* Docker

Package requirements:
* pipenv

Packages installed on pipenv virtual environment:
* cassandra-driver

## Commands

To build the image:

```
docker build --rm -t trishaire/cass:tag path_to_c2_dockerfile
```
To update the repository:
```
sudo docker login
docker push trishaire/cass:tag
```
To create cassandra service:
```
docker service create --name cass --network myNet --publish 9042:9042 trishaire/cass
```

## Connecting to Cass from a python component

For connecting to cassandra:
```
docker service inspect cass
Copy the virtual ip of the cassandra service
```

pip3 install `cassandra-driver` or make a Dockerfile with this package
python code to connect -

```
from cassandra.cluster import Cluster

cluster = Cluster(['vip of cassandra'])
session = cluster.connect()
session.execute(query)
```

[Main README](https://github.com/CPVazquez/CS6343)
