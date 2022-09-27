"""画像変換モジュール.

カメラから取得した画像を6色画像に変換する。
@author kodama0720 kawanoichi
"""
import cv2
import numpy as np
from enum import Enum
from typing import Tuple


class Color(Enum):
    """色クラス."""

    BLACK = 0
    RED = 1
    YELLOW = 2
    GREEN = 3
    BLUE = 4
    WHITE = 5


class ColorChanger:
    """画像の色変換クラス.

    Attributes:
        __BGR_COLOR(ndarray): RGB値(黒、赤、黄、緑、青、白)
        __LOWER(ndarray): HSV閾値下限(赤1、赤2、黄、緑、青、白)
        __UPPER(ndarray): HSV閾値上限(赤1、赤2、黄、緑、青、白)
    """

    __BGR_COLOR = np.array([[0, 0, 0], [0, 0, 255], [0, 255, 255],
                            [0, 255, 0], [255, 0, 0], [255, 255, 255]])
    __LOWER = np.array([[0, 90, 0], [151, 90, 0], [16, 130, 0],
                        [41, 70, 0], [104, 100, 0], [0, 0, 128]])
    __UPPER = np.array([[15, 255, 255], [180, 255, 255], [40, 255, 255],
                        [103, 255, 255], [150, 255, 255], [180, 70, 255]])

    def __init__(self) -> None:
        """ColorChangerのコンストラクタ."""
        self.color_id_img = []  # カラーIDを格納する配列を宣言

    def change_color(self, game_area_img: cv2.Mat, save_path: str) -> None:
        """画像を6色画像に変換する関数.

        Args:
            game_area_img (cv2.Mat): ゲームエリア画像
            save_path (str): 出力画像ファイルの保存パス
        """
        y_size = game_area_img.shape[0]  # 入力画像の縦サイズ
        x_size = game_area_img.shape[1]  # 入力画像の横サイズ
        color_size = game_area_img.shape[2]  # RGBの3次元
        # BGR色空間からHSV色空間への変換
        hsv = cv2.cvtColor(game_area_img, cv2.COLOR_BGR2HSV)
        # 処理結果を保持する配列を宣言(色を黒で初期化)
        self.result = np.zeros((x_size*y_size, color_size), np.uint8)
        self.color_id_img = np.zeros(x_size*y_size)

        # 色ID(赤1、赤2、黄、緑、青、白)
        color_ids = [Color.RED.value, Color.RED.value, Color.YELLOW.value,
                     Color.GREEN.value, Color.BLUE.value, Color.WHITE.value]

        # 元画像を一次元の配列に変形
        hsv = hsv.reshape(self.result.shape)

        for i in range(len(color_ids)):
            # 条件を満たすindexを取得
            index = np.where(np.all(ColorChanger.__LOWER[i] <= hsv, axis=1)
                             & np.all(hsv <= ColorChanger.__UPPER[i], axis=1))
            # カラーIDの配列に変換
            self.color_id_img[index] = color_ids[i]
            # 6色画像(BGR)に変換
            self.result[index] = ColorChanger.__BGR_COLOR[color_ids[i]]

        # 元の形状に変形
        self.result = self.result.reshape(game_area_img.shape)
        self.color_id_img = self.color_id_img.reshape(y_size, x_size)

        # 6色画像を保存
        cv2.imwrite(save_path, self.result)

    def search_color(self, coord_x: int, coord_y: int,
                     search_area_xsize: int, search_area_ysize: int) -> Tuple[int, int]:
        """指定領域内の色IDと各色のピクセル数を取得する.

        Args:
            coord_x (int): 指定領域の中心のx座標
            coord_y (int): 指定領域の中心のy座標
            search_area_xsize (int): 指定領域のxサイズ
            search_area_ysize (int): 指定領域のyサイズ

        Returns:
            color_uniqs: 指定領域内に存在する色IDの種類
            color_pixel_sum: 指定領域内の各色のピクセル数
        """
        # 指定領域を配列として宣言
        search_area = self.color_id_img[
            coord_y-(search_area_ysize//2):coord_y+(search_area_ysize//2)+1,
            coord_x-(search_area_xsize//2):coord_x+(search_area_xsize//2)+1]
        # 配列から黒と白を除去
        search_area = search_area = search_area[
            np.where((search_area != Color.BLACK.value) & (search_area != Color.WHITE.value))]

        # もし選択した領域内に白と黒しかなかった場合は、領域内に各色(白黒以外)が同じピクセル数だけ存在することとする
        if not search_area.shape[0]:
            color_uniqs = np.array([1, 2, 3, 4])
            color_pixel_sum = np.full(4, search_area_xsize*search_area_ysize//4)
            return color_uniqs.astype(np.int64), color_pixel_sum.astype(np.int64)

        # 配列に存在する色IDの種類とピクセル数を求める
        color_uniqs, color_pixel_sum = np.unique(search_area, return_counts=True)

        # int型配列に直して返す
        return color_uniqs.astype(np.int64), color_pixel_sum.astype(np.int64)


if __name__ == "__main__":
    read_path = "test_image.png"
    save_path = "color_" + read_path
    game_area_img = cv2.imread(read_path)

    # インスタンス化
    color_changer = ColorChanger()

    # 6色変換
    color_changer.change_color(game_area_img, save_path)

    # 指定領域内の色IDと各色のピクセル数を取得
    color_uniqs, color_pixel_sum = color_changer.search_color(520, 145, 21, 21)  # base南(520, 145)
    print("color_uniqs", color_uniqs)
    print("color_pixel_sum", color_pixel_sum)
    color_uniqs, color_pixel_sum = color_changer.search_color(0, 0, 5, 5)  # 白黒のみ検知してしまう場合
    print("color_uniqs", color_uniqs)
    print("color_pixel_sum", color_pixel_sum)

    print("color_changer 終了")
