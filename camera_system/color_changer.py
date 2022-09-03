"""画像変換モジュール.

カメラから取得した画像を6色画像に変換する。
@author kodama0720 kawanoichi
"""
import cv2
import numpy as np
from enum import Enum


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

    def calculate_mode_color(self, coord_x: int, coord_y: int,
                             mode_area_xsize: int, mode_area_ysize: int) -> int:
        """ブロック周辺の色の最頻値を求める.

        Args:
            coord_x (int): ブロックのx座標
            coord_y (int): ブロックのy座標
            mode_area_xsize (int): 最頻値を求める範囲のxサイズ
            mode_area_ysize (int): 最頻値を求める範囲のyサイズ
        """
        # 座標周辺を取り出す
        mode_area = self.color_id_img[coord_y-(mode_area_ysize//2):coord_y+(mode_area_ysize//2)+1,
                                      coord_x-(mode_area_xsize//2):coord_x+(mode_area_xsize//2)+1]
        # 配列から黒と白を除去
        mode_area = mode_area = mode_area[
            np.where((mode_area != Color.BLACK.value) & (mode_area != Color.WHITE.value))]

        # もし選択した座標周辺に白と黒しかなかった場合は赤を返す
        if not mode_area.shape[0]:
            return Color.RED.value

        # 配列に存在するIDの種類と頻度を求める
        uniqs, counts = np.unique(mode_area, return_counts=True)
        # 最頻値が複数の場合小さいほうを返す
        return int(min(uniqs[counts == np.amax(counts)]))


if __name__ == "__main__":
    read_path = "test_image.png"
    save_path = "color_" + read_path
    game_area_img = cv2.imread(read_path)
    # インスタンス化
    color_changer = ColorChanger()
    # 6色変換
    color_changer.change_color(game_area_img, save_path)
    # 最頻値取得　ボーナスブロック(211,432)
    # mode = color_changer.calculate_mode_color(211, 432, 5, 5)
    mode = color_changer.calculate_mode_color(0, 0, 5, 5)
    print("mode", mode)
    print("color_changer 終了")
