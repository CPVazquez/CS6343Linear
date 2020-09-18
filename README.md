# CS6343
Repository for our Cloud Computing Project


## Swarm initialization
To initialize the Docker Swarm, first connect to the server that you want the Manager node to exist on. In our case, this is done with `ssh cluster1-1` (if you are connected somewhere with the same username and hostname as an account on the server, such as `pubssh.utdallas.edu` to dodge the VPN requirement, those parts can be omitted from `ssh`. Additionally, setting up the `.ssh/authorized_keys` files will prevent you needing to log in with password). Then, initialize the swarm with `docker swarm init`.\

This command will specify a command to run on the other node to have a Docker worker ndoe join. This can also be generated with `docker swarm join-token worker`.\

Additionally, the firewall may need to be opened with `firewall-cmd --add-port=2377/tcp --permanent`, followed by `firewall-cmd --reload`. \

After this is complete, connect to the server you want the worker nodes to exist on. In our case, this is `ssh cluster1-2` or `ssh cluster1-3`. On that server, run the join command that was generated in the previous step. This should join your node to the swarm.\

This can be verified by returning to the server with the Manager node and running `docker node ls` and verifying the worker and manager nodes are in the list.


