"""CameraCoordinateCalibratorクラスのテストコードを記述するモジュール.

@author: mutotaka0426
"""

import unittest
import cv2

from camera_system.camera_calibrator import CameraCalibration


class TestCameraCalibrator(unittest.TestCase):
    def test_constructor(self):
        read_path = "course.png"
        cc = CameraCalibration(read_path)
        img = cv2.imread(read_path)
        save_path = "result_" + read_path
        actual_img = cc.img
        actual_save_path = cc.save_path

        self.assertEqual(img, actual_img)
        self.assertEqual(save_path, actual_save_path)
