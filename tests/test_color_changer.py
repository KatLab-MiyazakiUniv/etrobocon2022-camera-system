"""ColorChangerクラスのテストコードを記述するモジュール.

@author: kawanoichi
"""

import unittest
import numpy as np
import cv2
import os
from camera_system.color_changer import ColorChanger


class TestColorChanger(unittest.TestCase):
    def test_color_changer(self):
        cc = ColorChanger()
        read_path = os.path.dirname(os.path.realpath(__file__)) + "/test_image.png"
        save_path = os.path.dirname(os.path.realpath(__file__)) + "/test_color_image.png"
        img = cv2.imread(read_path)

        # change_color関数のテスト(画像が生成されているか)
        if os.path.exists(save_path):  # テスト前に画像があったら消去
            os.remove(save_path)
        cc.change_color(img, save_path)
        expected_exist = True
        actual_exist = os.path.exists(save_path)  # 画像が生成されているか確認(bool)
        self.assertEqual(expected_exist, actual_exist)

        # search_color関数のテスト
        actual = []
        search_area_size = 21
        actual.append(cc.search_color(422, 387, search_area_size, search_area_size))  # 領域が白のみ

        expected_color_uniqs = np.array([1, 2, 3, 4])  # 正解のカラーID
        expected_pixel_sum = search_area_size ** 2 // 2  # 正解のカラーID

        self.assertEqual(expected_color_uniqs, actual[0])
        self.assertEqual(expected_pixel_sum, actual[1])
