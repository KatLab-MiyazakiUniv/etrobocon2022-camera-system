"""画像変換モジュール.

カメラから取得した画像を6色画像に変換する。
@author kodama0720 kawanoichi

"""

import cv2
import numpy as np


class ColorChanger:
    """画像の色変換クラス.

    Attributes:
        __BGR_COLOR(ndarray): RGB値(赤、黄、緑、青、白)
        __LOWER(ndarray): HSV閾値下限(赤1、赤2、黄、緑、青、白)
        __UPPER(ndarray): HSV閾値上限(赤1、赤2、黄、緑、青、白)
    """

    __BGR_COLOR = np.array([[0, 0, 255], [0, 255, 255], [0, 255, 0],
                           [255, 0, 0], [255, 255, 255]])
    __LOWER = np.array([[0, 90, 0], [151, 90, 0], [16, 130, 0],
                        [41, 70, 0], [104, 100, 0], [0, 0, 128]])
    __UPPER = np.array([[15, 255, 255], [180, 255, 255], [40, 255, 255],
                        [103, 255, 255], [150, 255, 255], [180, 70, 255]])

    def change_color(self, read_path: str, save_path: str) -> None:
        """画像を6色画像に変換する関数.

        Args:
            read_path : 入力画像ファイルのパス
            save_path : 出力画像ファイルの保存パス
        """
        # 入力画像データの読み込み
        img = cv2.imread(read_path)
        y_size = img.shape[0]     # 入力画像の縦サイズ
        x_size = img.shape[1]     # 入力画像の横サイズ
        color_size = img.shape[2]  # RGBの3次元
        # BGR色空間からHSV色空間への変換
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        # 処理結果を保持する配列を宣言(色を黒で初期化)
        result = np.zeros((x_size*y_size, color_size), np.uint8)

        # 色ID(赤1、赤2、黄、緑、青、白)
        color_ids = [0, 0, 1, 2, 3, 4]

        # 元画像を一次元の配列に変形
        hsv = hsv.reshape(result.shape)

        for i in range(len(color_ids)):
            # 条件を満たすindexを取得
            index = np.where(np.all(ColorChanger.__LOWER[i] <= hsv, axis=1)
                             & np.all(hsv <= ColorChanger.__UPPER[i], axis=1))
            # 6色画像(BGR)に変換
            result[index] = ColorChanger.__BGR_COLOR[color_ids[i]]

        # 元の形状に変形
        result = result.reshape(img.shape)

        # 6色画像を保存
        cv2.imwrite(save_path, result)
