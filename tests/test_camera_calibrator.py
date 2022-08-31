"""Camera_Calibrationクラスのテストコードを記述するモジュール.

@author: kawanoichi
"""

import unittest
import cv2
import os
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent.parent))
sys.path.append(str(Path(__file__).parent.parent / "camera_system"))
from camera_system.camera_calibrator import CameraCalibration  # noqa


class TestCameraCalibrator(unittest.TestCase):
    def test_constructor(self):
        read_path = os.path.dirname(os.path.realpath(__file__)) + "/test_image.png"
        save_path = "result_" + read_path
        cc = CameraCalibration(read_path)
        actual_save_path = cc.save_path

        self.assertEqual(save_path, actual_save_path)
