#!/bin/bash

# 引数チェック
if [ $# -ne 1 ]; then
  echo "Please input 1 or 2 robot id."
  exit 1
fi

# データ送信先機体を設定
if [ $1 -eq 1 ]; then
    SSH_TARGET="katlab@192.168.11.16"
elif [ $1 -eq 2 ]; then
    SSH_TARGET="katlab@192.168.11.17"
else
    echo "Missing robot id."
    exit 1
fi

# 送信データディレクトリ
DATA_DIRECTORY="command_files"

if [ -d ${DATA_DIRECTORY} ]; then
    # 送信データディレクトリを機体に送信
    scp -r ${DATA_DIRECTORY} ${SSH_TARGET}:~/work/RasPike/sdk/workspace/etrobocon2022/
    echo "Completed ${DATA_DIRECTORY} submission."
else
    echo "\"${DATA_DIRECTORY}\" does not exist."
fi