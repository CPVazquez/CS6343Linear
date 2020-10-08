import docker

import logging
from time import sleep

healthy = False
client = docker.APIClient(base_url='unix://var/run/docker.sock')
logging.basicConfig(level=logging.DEBUG, 
    format='%(asctime)s - %(levelname)s - %(message)s')

while not healthy : 
    result = client.inspect_container("cass")['State']['Health']['Status']
    if result == 'healthy':
        healthy = True
    else:
        logging.debug("Cass failed health check")
        sleep(5)

logging.debug('Cass is healthy!')

#docker inspect --format='{{json .State.Health}}' cass 