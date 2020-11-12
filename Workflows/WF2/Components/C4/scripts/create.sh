#!/bin/bash
docker service create --name stock-analyzer --publish 4000:4000 \
	--network myNet --env CASS_DB=cass1 trishaire/stock-analyzer:linear
