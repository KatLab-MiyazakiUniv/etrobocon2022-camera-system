"""CameraCoordinateCalibratorクラスのテストコードを記述するモジュール.

@author: mutotaka0426
"""

import unittest
import cv2

from camera_system.camera_coordinate_calibrator import CameraCoordinateCalibrator


class TestCameraCoordinateCalibrator(unittest.TestCase):
    def test_constructor(self):
        ccc = CameraCoordinateCalibrator()
        expected = []
        actual_block_point = ccc.block_point
        actual_base_circle = ccc.base_circle
        actual_end_point = ccc.end_point

        self.assertEqual(expected, actual_block_point)
        self.assertEqual(expected, actual_base_circle)
        self.assertEqual(expected, actual_end_point)
