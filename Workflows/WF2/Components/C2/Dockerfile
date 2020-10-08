# https://stackoverflow.com/questions/32254497/create-keyspace-automatically-inside-docker-container-with-cassandra
# Code for File and entry-wrap inspired by two of the answers in this stack overflow
FROM cassandra:latest

COPY ./src/schema.cql /opt/data/schema.cql

COPY ./src/entry-wrap.sh /entry-wrap.sh
RUN chmod a+x /entry-wrap.sh
ENTRYPOINT ["/entry-wrap.sh"]

HEALTHCHECK --interval=5s --timeout=5s --start-period=10s --retries=3 \
    CMD cqlsh 127.0.0.1 || exit 1

CMD [ "cassandra", "-f"]