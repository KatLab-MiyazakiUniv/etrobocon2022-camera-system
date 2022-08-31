"""Camera_Calibrationクラスのテストコードを記述するモジュール.

@author: kawanoichi
"""

import unittest
import cv2
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent.parent))
sys.path.append(str(Path(__file__).parent.parent / "camera_system"))
from camera_system.camera_calibrator import CameraCalibration  # noqa


class TestCameraCalibrator(unittest.TestCase):
    def test_constructor(self):
        read_path = "test_image.png"
        cc = CameraCalibration(read_path)
        img = cv2.imread(read_path)
        save_path = "result_" + read_path
        actual_img = cc.img
        actual_save_path = cc.save_path

        self.assertEqual(img, actual_img)
        self.assertEqual(save_path, actual_save_path)
