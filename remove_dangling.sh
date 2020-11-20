#!/bin/bash

function remove() {
	Workers=$(docker node ls  -f "role=worker" --format '{{.Hostname}}')
	
	for worker in $Workers
	do
		set -xe
		ssh $worker docker rmi -f $(docker images -f "dangling=true" -q) || true
		set +xe
	done
	set -xe
	docker rmi -f $(docker images -f "dangling=true" -q) || true
	set +xe

}
	
function main() {
	remove
}


main "$@"
