to build the image:

```
docker build --rm -t trishare/restocker:tag path_to_c5_dockerfile
```
update the repository:
```
sudo docker login
docker push trishaire/restocker:tag
```
to create the serve type the following command:
```
docker service create --name restocker --network myNet --publish 8000:8000 --env CASS_DB=$CASS_DB trishaire/restocker
docker service create --name restocker --network myNet --mount type=bind,src=/var/run/docker.sock,dst=/var/run/docker.sock --publish 8000:8000 trishaire/restocker
```

Idea copy config file onto cluster1-2 and cluster1-3