#!/usr/bin/env python
"""A file that tests whether or not the cassandra container is ready for connections
"""
import logging
import json
from time import sleep

import docker

__author__ = "Carla Vazquez"
__version__ = "1.0.0"
__maintainer__ = "Carla Vazquez"
__email__ = "cpv150030@utdallas.edu"
__status__ = "Development"

# establish logging
logging.basicConfig(level=logging.DEBUG, 
    format='%(asctime)s - %(levelname)s - %(message)s')

# set default state of healthy to false
healthy = False

# get docker client
client = docker.from_env()
# get docker AIP client
APIclient = docker.APIClient(base_url='unix://var/run/docker.sock')

while not healthy : 
    # retrieve the tasks of the cass servcie
    tasks = client.services.get("cass").tasks()

    # see if at least one of the tasks is healthy
    for task in tasks:
        tID = task['ID']
        result = APIclient.inspect_task(tID)['Status']['Message']
        if result == 'started':
            healthy = True    
    
    # if none of the tasks are healthy, wait a bit before
    # trying again
    if not healthy:
        logging.debug("Cass failed health check")
        sleep(5)

logging.debug('Cass is healthy!')
