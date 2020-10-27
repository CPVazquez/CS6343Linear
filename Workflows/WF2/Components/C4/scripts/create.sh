#!/bin/bash
docker service create --name auto-restocker --publish 4000:4000 \
	--network myNet --env CASS_DB=cass trishaire/auto-restocker:latest
