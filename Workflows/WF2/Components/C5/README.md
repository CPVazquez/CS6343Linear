# Restocker

## Description

This component recieves restocking orders sent to the workflow manager. The restock orders follow the format of the restock-order.shema.json file in the shema folder. The component also scans the database every 5 minutes to check for items that might need to be restocked.

To run localy make sure you have environment variable `CASS_DB=0.0.0.0`

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
docker service create --name restocker --network myNet --publish port:port --env CASS_DB=VIP_of_Cass_Service trishaire/restocker
```
where the port is 8000 and VIP_of_Cass_Service is retrieved from the docker info command.