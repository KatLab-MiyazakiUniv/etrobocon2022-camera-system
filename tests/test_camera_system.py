"""CameraSystemクラスのテストコードを記述するモジュール.

@author: Takahiro55555 miyashita64
"""

import unittest
from unittest import mock
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent.parent))
sys.path.append(str(Path(__file__).parent.parent / "camera_system"))
from camera_system.camera_system import CameraSystem    # noqa


class TestCameraSystem(unittest.TestCase):
    @mock.patch('client.Client.wait_for_start_signal')
    def test_start(self, client_func_mock):
        cs = CameraSystem()
        cs.start()

    def test_is_left_course_default_value(self):
        cs = CameraSystem()
        expected = True
        actual = cs.is_left_course
        self.assertEqual(expected, actual)

    def test_is_left_course_constructor(self):
        expected = False
        cs = CameraSystem(is_left_course=expected)
        actual = cs.is_left_course
        self.assertEqual(expected, actual)

    def test_is_left_course_setter_and_getter(self):
        cs = CameraSystem()
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
