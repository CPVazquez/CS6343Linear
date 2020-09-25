To Create cassandra service:
  docker service create --name cassandra --network mynetwork --publish port:port image_name
  keep port as 9042 
  
For connecting to cassandra:
  docker service inspect cassandra
  Copy the virtual ip of the cassandra service
  
  pip3 install cassandra-drive or make a docker file with this package
  python code to connect -
    from cassandra.cluster import Cluster

    cluster = Cluster{['vip of cassandra'])
    session = cluster.connect()
    session.execute(query)
