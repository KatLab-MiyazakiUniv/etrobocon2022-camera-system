"""カメラキャリブレーションモジュール.

カメラキャリブレーションを行う
@author kawanoichi
"""
import numpy as np
import argparse
from color_changer import Color, ColorChanger
from camera_coordinate_calibrator import CameraCoordinateCalibrator
from camera_interface import CameraInterface
from game_area_info import GameAreaInfo

import cv2

class CameraCalibrator:
    """ゲームエリア認識クラス.

    Attributes:
        MODE_AREA_XSIZE (int): 最頻値を求める範囲のxサイズ(奇数)
        MODE_AREA_YSIZE (int): 最頻値を求める範囲のyサイズ(奇数)
    """

    # テンプレートサイズ(奇数)
    MODE_AREA_XSIZE = 5
    MODE_AREA_YSIZE = 5

    # 各ブロックの数
    COLOR_BLOCK_NUM = 8
    BASE_BLOCK_NUM = 4
    BONUS_BLOCK_NUM = 1

    # ブロックに使用されるカラー（赤、黄、緑、青の4種類）
    VALIDITY_COLOR_NUM = 4

    def __init__(self, camera_id: int, cali_img_save_path="cali_course.png") -> None:
        """CameraCalibrationのコンストラクタ.

        Args:
            camera_id (int): 撮影カメラ番号
            cali_img_save_path (str): キャリブレーション用画像保存パス
        """
        # キャリブレーション用画像の取得
        self.__camera_interface = CameraInterface(camera_id)
        # self.__calibration_img = self.__camera_interface.capture_frame(cali_img_save_path)
        self.__calibration_img = cv2.imread("test_image.png")

        self.__color_changer = ColorChanger()
        self.__coord = CameraCoordinateCalibrator(self.__calibration_img)

        # 色カウント
        self.count_point = np.zeros(CameraCalibrator.COLOR_BLOCK_NUM*CameraCalibrator.VALIDITY_COLOR_NUM
                                    ).reshape(CameraCalibrator.COLOR_BLOCK_NUM,CameraCalibrator.VALIDITY_COLOR_NUM)
        self.count_base = np.zeros(CameraCalibrator.BASE_BLOCK_NUM*CameraCalibrator.VALIDITY_COLOR_NUM
                                    ).reshape(CameraCalibrator.BASE_BLOCK_NUM,CameraCalibrator.VALIDITY_COLOR_NUM)

    def start_camera_calibration(self) -> None:
        """カメラキャリブレーションを行う関数."""
        # GUIから座標取得
        self.__coord.show_window()

    def make_game_area_info(self, is_left_course: bool, game_save_path="game_course.png") -> None:
        """ゲームエリア情報作成を行う関数.

        Args:
            is_left_course (bool): 左コースの場合 True. Defaults to True.
            game_save_path (str): ゲームエリア画像保存パス
        """
        # ゲームエリア画像を取得
        # game_area_img = self.__camera_interface.capture_frame(game_save_path)
        # 6色変換
        color_save_path = "color_" + game_save_path
        # self.__color_changer.change_color(game_area_img, color_save_path)
        self.__color_changer.change_color(self.__calibration_img, color_save_path)

        # カラーIDを格納する配列を宣言
        block_color_list = np.zeros(CameraCalibrator.COLOR_BLOCK_NUM)
        base_color_list = np.zeros(CameraCalibrator.BASE_BLOCK_NUM)
        bonus_color = np.zeros(CameraCalibrator.BONUS_BLOCK_NUM)
        print("bonus_color", bonus_color)
        print("bonus_color.shape", bonus_color.shape)

        # """

        # ブロック置き場
        print("ブロック置き場")
        for i, point in enumerate(self.__coord.block_point):
            # 最頻値を求めてブロックの色を判定
            uniqs, counts = self.__color_changer.calculate_mode_color(point[0],
                                                                      point[1],
                                                                      CameraCalibrator.MODE_AREA_XSIZE,
                                                                      CameraCalibrator.MODE_AREA_YSIZE)
            np.put(self.count_point[i], uniqs-1, 
                   counts/(CameraCalibrator.MODE_AREA_XSIZE*CameraCalibrator.MODE_AREA_XSIZE))
        
        color_count = np.zeros(CameraCalibrator.VALIDITY_COLOR_NUM) #(赤、黄、緑、青)
        for i in range(block_color_list.shape[0]):
            # print("i:", i)
            # print("self.count_point\n", self.count_point)
            max_index = np.unravel_index(np.argmax(self.count_point), self.count_point.shape)
            # print("2次元の最大値座標\n", max_index)
            block_color_list[max_index[0]] = max_index[1]+1 # indexとカラーIDを合わせるために+1
            color_count[max_index[1]] += 1
            if color_count[max_index[1]] == 2:
                self.count_point[:,max_index[1]] = -1
            self.count_point[max_index[0],:] = -1
        print("block_color_list", block_color_list)


        # ベースサークル置き場
        print("ベースサークル置き場")
        for i, base in enumerate(self.__coord.base_circle):
            # 最頻値を求めてブロックの色を判定
            uniqs, counts = self.__color_changer.calculate_mode_color(base[0],
                                                                      base[1],
                                                                      CameraCalibrator.MODE_AREA_XSIZE,
                                                                      CameraCalibrator.MODE_AREA_YSIZE)

            np.put(self.count_base[i], uniqs-1, 
                   counts/(CameraCalibrator.MODE_AREA_XSIZE*CameraCalibrator.MODE_AREA_XSIZE))
        
        for i in range(base_color_list.shape[0]):
            # print("i:", i)
            # print("self.count_base\n", self.count_base)
            max_index = np.unravel_index(np.argmax(self.count_base), self.count_base.shape)
            # print("2次元の最大値座標\n", max_index)
            base_color_list[max_index[0]] = max_index[1]+1 # indexとカラーIDを合わせるために+1
            self.count_base[max_index[0],:] = -1
            self.count_base[:,max_index[1]] = -1
        print("base_color_list", base_color_list)

        # """
        # 端点サークル置き場
        # 最頻値を求めてブロックの色を判定
        uniqs, counts = self.__color_changer.calculate_mode_color(self.__coord.end_point[0][0],
                                                                  self.__coord.end_point[0][1],
                                                                  CameraCalibrator.MODE_AREA_XSIZE,
                                                                  CameraCalibrator.MODE_AREA_YSIZE)
        bonus_color = uniqs[np.argmax(counts)]
        print("bonus_color", bonus_color)

        # aaa = [Color(block) for block in block_color_list]
        # print("aaa",aaa)


        # """
        # ゲームエリア情報を作成
        GameAreaInfo.block_color_list = [Color(block_color) for block_color in block_color_list]
        GameAreaInfo.base_color_list = [Color(base_color) for base_color in base_color_list]
        GameAreaInfo.bonus_color = Color(bonus_color)
        # コースに応じて交点の色をセットする
        if is_left_course:
            GameAreaInfo.intersection_list = [Color.RED, Color.BLUE, Color.YELLOW, Color.GREEN]
        else:
            GameAreaInfo.intersection_list = [Color.BLUE, Color.RED, Color.GREEN, Color.YELLOW]
        # """


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="使用例\n"
                                                 " 接続されているカメラIDを表示する\n"
                                                 " $ python camera_calibrator.py\n"
                                                 " カメラキャリブレーションを開始する\n"
                                                 " $ python camera_calibrator.py -id 0 (0はカメラID)",
                                     formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument("-id", "--camera-id", type=int, help="カメラキャリブレーションを開始する")
    args = parser.parse_args()

    # カメラIDがない時、接続されているカメラを取得し、表示する
    if args.camera_id is None:
        CameraInterface.check_camera_connection()
        exit(0)

    camera_calibration = CameraCalibrator(camera_id=args.camera_id)
    camera_calibration.start_camera_calibration()
    camera_calibration.make_game_area_info(False)

    # print(GameAreaInfo.block_color_list)
    # print(GameAreaInfo.base_color_list)
    # print(GameAreaInfo.bonus_color)

    print("CameraCalibrator 終了")
