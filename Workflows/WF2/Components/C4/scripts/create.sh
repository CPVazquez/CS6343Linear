#!/bin/bash
docker service create --name stock-analyzer --publish 4000:4000 \
	--network myNet --env CASS_DB=cass trishaire/stock-analyzer:linear
