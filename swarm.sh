#!/bin/bash

function create() {
	ManagerIP=$(hostname -i)	
	echo "Manager IP: ${ManagerIP}"
	set -xe
	docker swarm init --advertise-addr ${ManagerIP}
	set +xe
	echo "Swarm manager created"
	ManagerToken=`docker swarm join-token manager | grep token | awk '{ print $5 }'`
    	WorkerToken=`docker swarm join-token worker | grep token | awk '{ print $5 }'`
	echo "Manager Token: ${ManagerToken}"
    	echo "Workder Token: ${WorkerToken}"

	for node in "$@"
	do    				
		set -xe
        	ssh $node "docker swarm join --token ${WorkerToken} ${ManagerIP}:2377"
        	set +xe
		echo "$node joined as a worker"
	done
	set -xe
	docker network create --attachable --driver=overlay myNet
	set +xe
}

function destroy() {
	Workers=$(docker node ls  -f "role=worker" --format '{{.Hostname}}')
	
	Services=$(docker service ls --format '{{.Name}}')
	
	for service in $Services
	do
		set -xe
		docker service rm $service
		set +xe
	done

	for worker in $Workers
	do
		set -xe
		ssh $worker docker swarm leave
		set +xe
	done
	set -xe
	docker swarm leave --force
	set +xe

}
	
function main() {
    Command=$1
    shift
    case "${Command}" in
        create) create "$@" ;;
        destroy) destroy "$@" ;;
        *)      echo "Usage: $0 <create|destroy>" ;;
    esac
}

main "$@"
