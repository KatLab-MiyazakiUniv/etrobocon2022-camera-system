"""画像変換モジュール.

カメラから取得した画像を6色画像に変換する。
@author kodama0720 kawanoichi

"""

import cv2
import numpy as np
import statistics
import global_value as g


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
    def __init__(self):
        # カラーIDを格納する配列を宣言
        self.color_id_img = []

    def change_color(self) -> None:
        """画像を6色画像に変換する関数.

        Args:
            read_path : 入力画像ファイルのパス
            save_path : 出力画像ファイルの保存パス
        """
        # 入力画像データの読み込み
        # g.img = cv2.imread(ColorChanger.READ_PATH)
        print("入力サイズ", g.img.shape)
        y_size = g.img.shape[0]     # 入力画像の縦サイズ
        x_size = g.img.shape[1]     # 入力画像の横サイズ
        color_size = g.img.shape[2]  # RGBの3次元
        # BGR色空間からHSV色空間への変換
        hsv = cv2.cvtColor(g.img, cv2.COLOR_BGR2HSV)
        # 処理結果を保持する配列を宣言(色を黒で初期化)
        self.result = np.zeros((x_size*y_size, color_size), np.uint8)
        self.color_id_img = np.zeros(x_size*y_size)

        # 色ID(赤1、赤2、黄、緑、青、白)
        color_ids = [0, 0, 1, 2, 3, 4]

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
        self.result = self.result.reshape(g.img.shape)
        self.color_id_img = self.color_id_img.reshape(y_size, x_size)

        # 6色画像を保存
        cv2.imwrite(g.save_path, self.result)

    def mode_color(self, coord_x:int, coord_y:int, temp_xsize:int, temp_ysize:int)->int:
        """ ブロック周辺の色の最頻値を求める """
        # 座標周辺を取り出す
        temp = self.color_id_img[coord_y-(temp_ysize//2):coord_y+(temp_ysize//2)+1,
                                 coord_x-(temp_xsize//2):coord_x+(temp_xsize//2)+1]
        # 画像周辺の最頻値を求める(カラーID)
        return int(statistics.mode(temp.reshape(temp_ysize*temp_xsize)))

if __name__ == "__main__":
    read_path = "course.png"
    g.save_path = "result_" + read_path
    g.img = cv2.imread(read_path)

    color_changer = ColorChanger()
    color_changer.change_color()
    color_changer.mode_color()
    print("color_changer 終了")
