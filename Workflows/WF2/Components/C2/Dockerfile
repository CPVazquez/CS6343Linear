From cassandra:latest

COPY ./src/schema.cql /opt/data/schema.cql
COPY ./src/startCassandra.sh /app/startCassandra.sh
RUN chmod a+x /app/startCassandra.sh

CMD   /app/startCassandra.sh