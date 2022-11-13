"""開始合図要求モジュール.

走行システムに開始合図を要求する.
@author miyashita64
@note 参考 https://itsakura.com/python-socket
"""

import socket
import time


class Client:
    """走行体から開始合図を受け取るまで要求を続けるクラス."""

    def __init__(self, ip: str, port: int) -> None:
        """Clientのコンストラクタ.

        Args:
            ip (string): サーバのIPアドレス
            port (int): サーバのポート番号
        """
        self.server_ip = ip         # サーバのIPアドレス
        self.server_port = port     # サーバのポート番号

    def wait_for_start_signal(self) -> None:
        """Start合図を受け取るまで要求を続ける."""
        while True:
            # ソケットを作成する
            sock = socket.socket(socket.AF_INET)

            try:
                # サーバに接続する
                sock.connect((self.server_ip, self.server_port))
                # レスポンスを受け取る
                response = sock.recv(256).decode()
                if response:
                    print("Received '%s' Signal." % (response))
                if response == "Start":
                    break
            except ConnectionRefusedError as e:
                # 接続できなかった場合
                print(e)

            # ソケットを削除する
            sock.close()

            # 1秒待機する
            time.sleep(1)
