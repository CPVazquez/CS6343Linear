#!/bin/bash

declare -a imageArray=("trishaire/order-verifier:async" "trishaire/order-processor:async" "trishaire/delivery-assigner:async" "trishaire/stock-analyzer:async" "trishaire/cass:async")

function pull() {
	Workers=$(docker node ls  -f "role=worker" --format '{{.Hostname}}')
	for val in ${imageArray[@]}; do
		for worker in $Workers
		do
			set -xe
			ssh $worker sudo docker pull $val
			set +xe
		done
		set -xe
		sudo docker pull $val
		set +xe
	done
}


function main() {
	pull
}


main "$@"
