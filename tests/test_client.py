"""Clientクラスのテストコードを記述するモジュール.
@author: miyashita64
"""

import unittest
from unittest import mock
from camera_system.client import Client


class TestClient(unittest.TestCase):
    def test_constructor(self):
        client = Client("127.0.0.1", 8080)

    @mock.patch('socket.socket.connect', return_value=1)
    @mock.patch('socket.socket.recv', return_value="Start".encode())
    def test_wait_for_start_signal(self, connect_mock, recv_mock):
        client = Client("127.0.0.1", 8080)
        client.wait_for_start_signal()
