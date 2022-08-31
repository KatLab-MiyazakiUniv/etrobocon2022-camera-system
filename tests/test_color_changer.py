"""ColorChangerクラスのテストコードを記述するモジュール.

@author: kawanoichi
"""

import unittest
import cv2
import os
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent.parent))
sys.path.append(str(Path(__file__).parent.parent / "camera_system"))
from camera_system.color_changer import ColorChanger  # noqa


class TestColorChanger(unittest.TestCase):
    def test_color_changer(self):
        cc = ColorChanger()
        read_path = os.path.dirname(os.path.realpath(__file__)) + "/test_image.png"
        save_path = os.path.dirname(os.path.realpath(__file__)) + "/result_test_image.png"
        if os.path.exists(save_path):
            os.remove(save_path)
        img = cv2.imread(read_path)
        # 6色変換のテスト
        cc.change_color(img, save_path)
        actual_exist = os.path.exists(save_path)
        self.assertEqual(True, actual_exist)

        # 最頻値を求める関数のテスト
        mode01 = cc.mode_color(132, 150, 5, 5)  # ブロック置き場1
        mode02 = cc.mode_color(212, 122, 5, 5)  # ブロック置き場2
        mode03 = cc.mode_color(273,  92, 5, 5)  # ブロック置き場3
        mode04 = cc.mode_color(232, 178, 5, 5)  # ブロック置き場4
        mode05 = cc.mode_color(361, 113, 5, 5)  # ブロック置き場5
        mode06 = cc.mode_color(349, 210, 5, 5)  # ブロック置き場6
        mode07 = cc.mode_color(412, 163, 5, 5)  # ブロック置き場7
        mode08 = cc.mode_color(458, 133, 5, 5)  # ブロック置き場8
        mode09 = cc.mode_color(413,  87, 5, 5)  # ベースサークル1
        mode10 = cc.mode_color(561, 196, 5, 5)  # ベースサークル2
        mode11 = cc.mode_color(114, 232, 5, 5)  # ベースサークル3
        mode12 = cc.mode_color(121,  96, 5, 5)  # ベースサークル4
        mode13 = cc.mode_color(214, 420, 5, 5)  # 端点サークル

        expected = [4, 2, 3, 3, 4, 2, 1, 1, 3, 1, 4, 2, 3]
        self.assertEqual(expected[0], mode01)
        self.assertEqual(expected[1], mode02)
        self.assertEqual(expected[2], mode03)
        self.assertEqual(expected[3], mode04)
        self.assertEqual(expected[4], mode05)
        self.assertEqual(expected[5], mode06)
        self.assertEqual(expected[6], mode07)
        self.assertEqual(expected[7], mode08)
        self.assertEqual(expected[8], mode09)
        self.assertEqual(expected[9], mode10)
        self.assertEqual(expected[10], mode11)
        self.assertEqual(expected[11], mode12)
        self.assertEqual(expected[12], mode13)
