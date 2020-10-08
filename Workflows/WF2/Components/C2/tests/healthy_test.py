import docker

import logging
import json
from time import sleep

healthy = False
APIclient = docker.APIClient(base_url='unix://var/run/docker.sock')
logging.basicConfig(level=logging.DEBUG, 
    format='%(asctime)s - %(levelname)s - %(message)s')
client = docker.from_env()
while not healthy : 
    tasks = client.services.get("cass").tasks()
    #logging.debug(json.dumps(tasks,sort_keys=True, indent=4))
    
    for task in tasks:
        tID = task['ID']
        result = APIclient.inspect_task(tID)['Status']['Message']
        if result == 'started':
            healthy = True    
    

    if not healthy:
        logging.debug("Cass failed health check")
        sleep(5)

logging.debug('Cass is healthy!')

#docker inspect --format='{{json .State.Health}}' cass 
