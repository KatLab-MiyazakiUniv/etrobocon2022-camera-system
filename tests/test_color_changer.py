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
        save_path = os.path.dirname(os.path.realpath(__file__)) + "/test_color_image.png"
        if os.path.exists(save_path):
            os.remove(save_path)
        img = cv2.imread(read_path)
        # 6色変換のテスト
        cc.change_color(img, save_path)
        actual_exist = os.path.exists(save_path)
        self.assertEqual(True, actual_exist)

        # 最頻値を求める関数のテスト
        actual = []
        actual.append(cc.calculate_mode_color(132, 150, 5, 5))  # ブロック置き場1
        actual.append(cc.calculate_mode_color(212, 122, 5, 5))  # ブロック置き場2
        actual.append(cc.calculate_mode_color(273,  92, 5, 5))  # ブロック置き場3
        actual.append(cc.calculate_mode_color(232, 178, 5, 5))  # ブロック置き場4
        actual.append(cc.calculate_mode_color(361, 113, 5, 5))  # ブロック置き場5
        actual.append(cc.calculate_mode_color(349, 210, 5, 5))  # ブロック置き場6
        actual.append(cc.calculate_mode_color(412, 163, 5, 5))  # ブロック置き場7
        actual.append(cc.calculate_mode_color(458, 133, 5, 5))  # ブロック置き場8
        actual.append(cc.calculate_mode_color(413,  87, 5, 5))  # ベースサークル1
        actual.append(cc.calculate_mode_color(561, 196, 5, 5))  # ベースサークル2
        actual.append(cc.calculate_mode_color(114, 232, 5, 5))  # ベースサークル3
        actual.append(cc.calculate_mode_color(121,  96, 5, 5))  # ベースサークル4
        actual.append(cc.calculate_mode_color(214, 420, 5, 5))  # 端点サークル

        expected = [4, 2, 3, 3, 4, 2, 1, 1, 3, 1, 4, 2, 3]
        for i in range(13):
            self.assertEqual(expected[i], actual[i])
