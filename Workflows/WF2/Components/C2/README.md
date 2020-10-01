# Cass

## Description
This is the database component for both workflow mangers. It gets cql requests from several other components. It uses the offical docker image for Cassandra as a base and loads our keyspace (database) on to it.

## Docker Commands

To build the image:

```
docker build --rm -t trishare/cass:tag path_to_c2_dockerfile
```
To update the repository:
```
sudo docker login
docker push trishaire/cass:tag
```
To Create cassandra service:
```
docker service create --name cass --network myNet --publish port:port trishaire/cass:tag
```
where port is 9042

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

cluster = Cluster{['vip of cassandra'])
session = cluster.connect()
session.execute(query)
```