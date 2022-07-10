"""
color_changer.py
カメラから取得した画像を6色画像に変換する
@author kodama0720
"""

import cv2 as cv
import numpy as np


class ColorChanger:
    """画像の色変換クラス"""

    __BLACK = [0, 0, 0]
    # RGB値（赤、黄色、緑、青、白）
    __BGR_COLOR = np.array([[0, 0, 255], [0, 255, 255], [0, 255, 0],
                           [255, 0, 0], [255, 255, 255]])
    # HSVの閾値（赤1、赤2、黄色、緑、青、白）
    __LOWER = np.array([[0, 90, 0], [151, 90, 0], [16, 130, 0],
                        [41, 70, 0], [104, 100, 0], [0, 0, 128]])
    __UPPER = np.array([[15, 255, 255], [179, 255, 255], [40, 255, 255],
                        [103, 255, 255], [150, 255, 255], [179, 70, 255]])

    def change_color(self, path="course.png"):
        """画像を6色画像に変換する関数"""

        frame_mask = []
        # 画像データの読み込み
        img = cv.imread(path)
        # BGR色空間からHSV色空間への変換
        hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
        # 元画像と同じサイズの黒色画像を作成
        result = np.zeros(
            (img.shape[0], img.shape[1], img.shape[2]), np.uint8)

        # 赤抽出
        mask1 = cv.inRange(hsv, self.__LOWER[0], self.__UPPER[0])
        mask2 = cv.inRange(hsv, self.__LOWER[1], self.__UPPER[1])
        frame_mask.append(mask1 + mask2)

        # 黄色、緑、青、白抽出
        for i in range(2, 6):
            frame_mask.append(cv.inRange(
                hsv, self.__LOWER[i], self.__UPPER[i]))

        for i in range(5):
            # 論理演算で色検出（検出しなかった部分は黒）
            frame_mask[i] = cv.bitwise_and(img, img, mask=frame_mask[i])
            # 色の置換
            result[np.where((frame_mask[i] != self.__BLACK).all(
                axis=2))] = self.__BGR_COLOR[i]

        # 6色画像を保存する
        cv.imwrite("sixColor.png", result)
