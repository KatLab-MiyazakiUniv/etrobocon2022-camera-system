"""CameraCoordinateCalibratorクラスのテストコードを記述するモジュール.

@author: mutotaka0426
"""

import unittest
import cv2
import os
from camera_system.camera_coordinate_calibrator import CameraCoordinateCalibrator


class TestCameraCoordinateCalibrator(unittest.TestCase):
    def test_constructor(self):
        read_path = os.path.dirname(os.path.realpath(__file__)) + "/test_image.png"
        img = cv2.imread(read_path)
        ccc = CameraCoordinateCalibrator(img)
        expected = []
        actual_block_point = ccc.block_point
        actual_base_circle = ccc.base_circle
        actual_end_point = ccc.end_point

        self.assertEqual(expected, actual_block_point)
        self.assertEqual(expected, actual_base_circle)
        self.assertEqual(expected, actual_end_point)
