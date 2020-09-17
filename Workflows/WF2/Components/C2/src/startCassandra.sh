#!/bin/bash

if [ ! -d "$CASSANDRA_HOME/data/data/pizza_grocery" ] || [ -z "$(ls $CASSANDRA_HOME/data/data/pizza_grocery)" ]; then
    (sleep 30 ;cqlsh -f /opt/data/schema.cql) &
fi

cassandra -fR