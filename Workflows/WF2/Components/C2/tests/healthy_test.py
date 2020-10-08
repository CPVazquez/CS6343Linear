import docker

import logging
import json
from time import sleep

logging.basicConfig(level=logging.DEBUG, 
    format='%(asctime)s - %(levelname)s - %(message)s')

healthy = False

client = docker.from_env()
APIclient = docker.APIClient(base_url='unix://var/run/docker.sock')

while not healthy : 
    tasks = client.services.get("cass").tasks()

    for task in tasks:
        tID = task['ID']
        result = APIclient.inspect_task(tID)['Status']['Message']
        if result == 'started':
            healthy = True    
    
    if not healthy:
        logging.debug("Cass failed health check")
        sleep(5)

logging.debug('Cass is healthy!')
