#!/bin/bash
docker service create --name delivery-assigner --publish 3000:3000 \
	--network myNet --env CASS_DB=cass trishaire/delivery-assigner:linear

