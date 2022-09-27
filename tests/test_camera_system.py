"""CameraSystemクラスのテストコードを記述するモジュール.

@author: Takahiro55555 miyashita64 kawanoichi
"""
import unittest
from unittest import mock
import os
from contextlib import redirect_stdout

from camera_system.camera_system import CameraSystem
from game_area_info import GameAreaInfo
from node import Node
from robot import Robot, Direction
from coordinate import Coordinate
from color_changer import Color


class TestCameraSystem(unittest.TestCase):
    @mock.patch('camera_calibrator.CameraCalibrator.start_camera_calibration')
    @mock.patch('camera_calibrator.CameraCalibrator.make_game_area_info')
    @mock.patch('camera_interface.CameraInterface.capture_frame')
    @mock.patch('client.Client.wait_for_start_signal')
    def test_start(self, capture_frame_mock, make_game_area_info_mock,
                   start_camera_calibration_mock, client_func_mock):
        cs = CameraSystem(True, "127.0.0.1")
        # ゲームエリア情報の初期化
        robot = Robot(Coordinate(4, 4), Direction.E, "left")
        GameAreaInfo.node_list = [
            Node(-1, Coordinate(0, 0)), Node(-1, Coordinate(1, 0)),
            Node(-1, Coordinate(2, 0)), Node(-1, Coordinate(3, 0)),
            Node(-1, Coordinate(4, 0)), Node(-1, Coordinate(5, 0)),
            Node(-1, Coordinate(6, 0)),
            Node(-1, Coordinate(0, 1)), Node(0, Coordinate(1, 1)),
            Node(-1, Coordinate(2, 1)), Node(1, Coordinate(3, 1)),
            Node(-1, Coordinate(4, 1)), Node(2, Coordinate(5, 1)),
            Node(-1, Coordinate(6, 1)),
            Node(-1, Coordinate(0, 2)), Node(-1, Coordinate(1, 2)),
            Node(-1, Coordinate(2, 2)), Node(-1, Coordinate(3, 2)),
            Node(-1, Coordinate(4, 2)), Node(-1, Coordinate(5, 2)),
            Node(-1, Coordinate(6, 2)),
            Node(-1, Coordinate(0, 3)), Node(3, Coordinate(1, 3)),
            Node(-1, Coordinate(2, 3)), Node(-1, Coordinate(3, 3)),
            Node(-1, Coordinate(4, 3)), Node(4, Coordinate(5, 3)),
            Node(-1, Coordinate(6, 3)),
            Node(-1, Coordinate(0, 4)), Node(-1, Coordinate(1, 4)),
            Node(-1, Coordinate(2, 4)), Node(-1, Coordinate(3, 4)),
            Node(-1, Coordinate(4, 4)), Node(-1, Coordinate(5, 4)),
            Node(-1, Coordinate(6, 4)),
            Node(-1, Coordinate(0, 5)), Node(5, Coordinate(1, 5)),
            Node(-1, Coordinate(2, 5)), Node(6, Coordinate(3, 5)),
            Node(-1, Coordinate(4, 5)), Node(7, Coordinate(5, 5)),
            Node(-1, Coordinate(6, 5)),
            Node(-1, Coordinate(0, 6)), Node(-1, Coordinate(1, 6)),
            Node(-1, Coordinate(2, 6)), Node(-1, Coordinate(3, 6)),
            Node(-1, Coordinate(4, 6)), Node(-1, Coordinate(5, 6)),
            Node(-1, Coordinate(6, 6)),
        ]
        GameAreaInfo.block_color_list = [
            Color.RED, Color.RED, Color.YELLOW,
            Color.YELLOW, Color.GREEN,
            Color.GREEN, Color.BLUE, Color.BLUE
        ]
        GameAreaInfo.base_color_list = [
            Color.RED, Color.YELLOW,
            Color.GREEN, Color.BLUE
        ]
        GameAreaInfo.bonus_color = Color.RED
        GameAreaInfo.intersection_list = [Color.RED, Color.BLUE, Color.YELLOW, Color.GREEN]

        # 探索失敗のメッセージを無視するため標準出力を非表示にする
        with redirect_stdout(open(os.devnull, 'w')) as redirect:
            cs.start(camera_id=0)
            redirect.close()

    def test_is_left_course_default_value(self):
        cs = CameraSystem(True, "127.0.0.1")
        expected = True
        actual = cs.is_left_course
        self.assertEqual(expected, actual)

    def test_is_left_course_constructor(self):
        expected = False
        cs = CameraSystem(is_left_course=expected, robot_ip="127.0.0.1")
        actual = cs.is_left_course
        self.assertEqual(expected, actual)

    def test_is_left_course_setter_and_getter(self):
        cs = CameraSystem(True, "127.0.0.1")
        expected = False
        cs.is_left_course = expected
        actual = cs.is_left_course
        self.assertEqual(expected, actual)

        expected = True
        cs.is_left_course = expected
        actual = cs.is_left_course
        self.assertEqual(expected, actual)

        with self.assertRaises(TypeError):
            cs.is_left_course = 'hogehoge'
