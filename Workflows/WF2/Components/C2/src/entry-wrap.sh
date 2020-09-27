#!/bin/bash


if [ ! -d "$CASSANDRA_HOME/data/data/pizza_grocery" ] || [ -z "$(ls $CASSANDRA_HOME/data/data/pizza_grocery)" ]; then
    echo "$0: running /opt/data/schema.cql" && until cqlsh -f opt/data/schema.cql; do >&2 echo "Cassandra is unavailable - sleeping"; sleep 2; done &
fi

exec /docker-entrypoint.sh "$@"