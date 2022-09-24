#!/bin/bash

# 引数チェック
if [ $# -ne 2 ]; then
  echo "Please input 'left' or 'right' and robot ip address."
  exit 1
fi

COURSE=$1
ROBOT_IP=$2

if [ $COURSE == "left" ]; then
    make run-L ROBOT_IP=$ROBOT_IP
    bash ./submit.sh $ROBOT_IP
elif [ $COURSE == "right" ]; then
    make run-R ROBOT_IP=$ROBOT_IP
    bash ./submit.sh $ROBOT_IP
fi