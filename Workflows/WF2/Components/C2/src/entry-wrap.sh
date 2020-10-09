#!/bin/bash

# author = "Carla Vazquez"
# version = "1.0.0"
# maintainer = "Carla Vazquez"
# email = "cpv150030@utdallas.edu"
# status = "Development"

if [ ! -d "$CASSANDRA_HOME/data/data/pizza_grocery" ] || [ -z "$(ls $CASSANDRA_HOME/data/data/pizza_grocery)" ]; then
    echo "$0: running /opt/data/pizza.cql" && until cqlsh -f opt/data/pizza.cql; do >&2 echo "Cassandra is unavailable - sleeping"; sleep 2; done &
fi

exec /docker-entrypoint.sh "$@"