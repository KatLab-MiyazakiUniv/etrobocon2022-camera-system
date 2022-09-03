"""Camera_Calibrationクラスのテストコードを記述するモジュール.

@author: kawanoichi
"""

import unittest
from unittest import mock
import os
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent.parent))
sys.path.append(str(Path(__file__).parent.parent / "camera_system"))

from camera_system.camera_calibrator import CameraCalibrator  # noqa


class TestCameraCalibrator(unittest.TestCase):
    @mock.patch('camera_interface.CameraInterface.capture_frame')
    def test_constructor(self, capture_frame_mock):
        cc = CameraCalibrator(0)
