"""Camera_Calibrationクラスのテストコードを記述するモジュール.

@author: kawanoichi
"""

import unittest
from unittest import mock

from camera_system.camera_calibrator import CameraCalibrator


class TestCameraCalibrator(unittest.TestCase):
    @mock.patch('camera_interface.CameraInterface.capture_frame')
    def test_constructor(self, capture_frame_mock):
        cc = CameraCalibrator(0)
