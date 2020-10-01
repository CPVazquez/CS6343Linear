# Restocker

## Description

This component recieves restocking orders sent to the workflow manager. The restock orders follow the format of the restock-order.shema.json file in the shema folder. The component also scans the database every 5 minutes to check for items that might need to be restocked.

To run localy make sure you have environment variables `CASS_DB=0.0.0.0` and `FLASK_ENV=development` set

## Docker Commands

To build the image:

```
docker build --rm -t trishare/restocker:tag path_to_c5_dockerfile
```
To update the repository:
```
sudo docker login
docker push trishaire/restocker:tag
```
To create the service type the following command:
```
docker service create --name restocker --network myNet --publish 8000:8000 --env CASS_DB=VIP_of_Cass_Service trishaire/restocker:tag
```
where VIP_of_Cass_Service is retrieved from the `docker inspect cass` command.

To run the container:
```
docker run -dp 8000:8000 --env CASS_DB=IP_of_Cass_Container trishaire/restocker 
```
where IP_of_Cass_Container is retrieved from the `docker inspect cass_contianer_name`

## Testing

This component uses pytest to run unit test. you must be connected to a cassandra instance to run the tests correctly. I'm still trying to figure out how to mock cassandra. 

use the following command to run tests:
```
pytest --cov=src tests
```
