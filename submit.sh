#!/bin/bash

# 引数チェック
if [ $# -ne 1 ]; then
  echo "Please input robot ip address."
  exit 1
fi

cd camera_system

# データ送信先機体を設定
SSH_TARGET="katlab@"$1

# 送信データディレクトリ
DATA_DIRECTORY="datafiles"

if [ -d ${DATA_DIRECTORY} ]; then
    # 送信データディレクトリを機体に送信後，機体のデータディレクトリに権限を付与する
    scp -r ${DATA_DIRECTORY} ${SSH_TARGET}:~/work/RasPike/sdk/workspace/etrobocon2022/
    ssh ${SSH_TARGET} "chmod 777 ~/work/RasPike/sdk/workspace/etrobocon2022/${DATA_DIRECTORY}/*"
    echo "Completed ${DATA_DIRECTORY} submission."
else
    echo "\"${DATA_DIRECTORY}\" does not exist."
fi
