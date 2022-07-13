"""画像変換モジュール.

カメラから取得した画像を6色画像に変換する。
@author kodama0720

"""

import cv2 as cv
import numpy as np


class ColorChanger:
    """画像の色変換クラス.

    Attributes:
        __BLACK(ndarray): RGB値(黒)
        __BGR_COLOR(ndarray): RGB値(赤、黄、緑、青、白)
        __LOWER(ndarray): HSV閾値下限(赤1、赤2、黄、緑、青、白)
        __UPPER(ndarray): HSV閾値上限(赤1、赤2、黄、緑、青、白)

    """

    __BLACK = np.array([0, 0, 0])
    __BGR_COLOR = np.array([[0, 0, 255], [0, 255, 255], [0, 255, 0],
                           [255, 0, 0], [255, 255, 255]])
    __LOWER = np.array([[0, 90, 0], [151, 90, 0], [16, 130, 0],
                        [41, 70, 0], [104, 100, 0], [0, 0, 128]])
    __UPPER = np.array([[15, 255, 255], [179, 255, 255], [40, 255, 255],
                        [103, 255, 255], [150, 255, 255], [179, 70, 255]])

    def change_color(self, path: str = "course.png") -> None:
        """画像を6色画像に変換する関数.

        Args:
            path (str, optional): 入力画像ファイルのパス. Defaults to "course.png".

        """
        frame_mask = []
        # 画像データの読み込み
        img = cv.imread(path)
        # BGR色空間からHSV色空間への変換
        hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
        # 元画像と同じサイズの黒色画像を作成
        result = np.zeros(img.shape, np.uint8)

        # 赤抽出
        mask1 = cv.inRange(hsv, ColorChanger.__LOWER[0], ColorChanger.__UPPER[0])
        mask2 = cv.inRange(hsv, ColorChanger.__LOWER[1], ColorChanger.__UPPER[1])
        frame_mask.append(mask1 + mask2)

        # 黄、緑、青、白抽出
        for i in range(2, 6):
            frame_mask.append(cv.inRange(hsv, ColorChanger.__LOWER[i], ColorChanger.__UPPER[i]))

        for i in range(len(frame_mask)):
            # 論理演算で色検出（検出しなかった部分は黒）
            frame_mask[i] = cv.bitwise_and(img, img, mask=frame_mask[i])
            # 色の置換
            result[np.where((frame_mask[i] != ColorChanger.__BLACK).all(axis=2))
                   ] = ColorChanger.__BGR_COLOR[i]

        # 6色画像を保存
        cv.imwrite("sixColor.png", result)
