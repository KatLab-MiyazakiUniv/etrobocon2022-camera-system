"""CameraSystemクラスのテストコードを記述するモジュール.

@author: Takahiro55555
"""
import unittest
from unittest import mock
import cv2
import os

from camera_system.camera_system import CameraSystem


class TestCameraSystem(unittest.TestCase):
    @mock.patch('camera_calibrator.CameraCalibrator.start_camera_calibration')
    @mock.patch('camera_calibrator.CameraCalibrator.make_game_area_info')
    @mock.patch('camera_interface.CameraInterface.capture_frame')
    def test_start(self, capture_frame_mock, make_game_area_info_mock,
                   start_camera_calibration_mock):
        cs = CameraSystem()
        cs.start(camera_id=0)

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
