# CS6343
Repository for our Cloud Computing Project

## Swarm initialization
To initialize the Docker Swarm, first connect to the server that you want the Manager node to exist on. In our case, this is done with `ssh cluster1-1` (if you are connected somewhere with the same username and hostname as an account on the server, such as `pubssh.utdallas.edu` to dodge the VPN requirement, those parts can be omitted from `ssh`. Additionally, setting up the `.ssh/authorized_keys` files will prevent you needing to log in with password). Then, initialize the swarm with `docker swarm init`.  

This command will specify a command to run on the other node to have a Docker worker ndoe join. This can also be generated with `docker swarm join-token worker`.  

Additionally, the firewall may need to be opened with `firewall-cmd --add-port=2377/tcp --permanent`, followed by `firewall-cmd --reload`.  

After this is complete, connect to the server you want the worker nodes to exist on. In our case, this is `ssh cluster1-2` or `ssh cluster1-3`. On that server, run the join command that was generated in the previous step. This should join your node to the swarm.  

This can be verified by returning to the server with the Manager node and running `docker node ls` and verifying the worker and manager nodes are in the list.  

## Dockerhub as a Registry
To make sure that all nodes are using the correct image, and have access to said image, when creating a service, we are using Dockerhub as a registry for our repository<sup>[1](#repositoryFootnote)</sup>. Currently we are using Carla's account on dockerhub, trishaire, to host the repositories. Carla's credentials are on the `cluster1-1` machine. 

To login simply type in `sudo docker login` and you will connect to the account trishaire. If you are going to be creating a new repository or pushing an updated image to the repository you need to be logged in or you will get an error. Pulling should be able to be performed without authentication.

### To create a new repository on Dockerhub :

```
docker tag local-image:tagname new-repo:tagname
```

where new-repo must contain the prefix `trishaire/` for example:

```
docker tag restocker:latest trishaire/restocker:latest
```
### To push an image to the repository
```
docker push new-repo:tagname
```
for example:
```
docker push trishaire/restocker:1.0
```

<sub><a name="repositoryFootnote">1</a> an image is a single image, and a repository is a collection of images. On Dockerhub we can use a repository to hold multiple images with different tags as long as they have the same name.</sub>
