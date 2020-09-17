#!/bin/bash
# https://stackoverflow.com/questions/34909702/how-to-create-a-dockerfile-for-cassandra-or-any-database-that-includes-a-schem

if [ ! -d "$CASSANDRA_HOME/data/data/pizza_grocery" ] || [ -z "$(ls $CASSANDRA_HOME/data/data/pizza_grocery)" ]; then
    (sleep 30 ;cqlsh -f /opt/data/schema.cql) &
fi

cassandra -fR