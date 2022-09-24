# 引数チェック
if ($args.length -eq 0) {
    Write-Host "Please input robot ip address."
    exit 1
}

cd camera_system

# データ送信先機体を設定
$ssh_target = "katlab@${Args[0]}"

# 送信データディレクトリ
$data_directory = "datafiles/"

if (Test-Path $data_directory) {
    # 送信データディレクトリを機体に送信
    scp -r ${data_directory} ${ssh_target}:~/work/RasPike/sdk/workspace/etrobocon2022/
    Write-Host "Completed ${data_directory} submission."
} else {
    Write-Host "'${data_directory}' does not exist."
}

cd ../