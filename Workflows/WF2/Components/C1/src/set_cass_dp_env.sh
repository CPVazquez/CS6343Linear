#!/bin/bash
export CASS_DB=$(nrOfTasks=`getent hosts tasks.cass | wc -l` ; many=`getent hosts tasks.cass | awk '{print $1}' | sed "/$(hostname --ip-address)/d" | paste -d, -s -` ; printf '%s' $( [ ${nrOfTasks} -gt 1 ] && echo ${many} || echo "$(hostname --ip-address)" ))
cd ~
source .bash_profile
