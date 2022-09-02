"""Camera_Calibrationクラスのテストコードを記述するモジュール.

@author: kawanoichi
"""

import unittest
import os
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent.parent))
sys.path.append(str(Path(__file__).parent.parent / "camera_system"))
from camera_system.camera_calibrator import CameraCalibrator  # noqa


class TestCameraCalibrator(unittest.TestCase):
    def test_constructor(self):
        cali_img_save_path = os.path.dirname(os.path.realpath(__file__)) + "/cali_test_image.png"
        cc = CameraCalibrator(0, cali_img_save_path)
        self.assertTrue(os.path.exists(cali_img_save_path))
        os.remove(cali_img_save_path)
        print("カメラキャリブレーションテスト画像の削除")
