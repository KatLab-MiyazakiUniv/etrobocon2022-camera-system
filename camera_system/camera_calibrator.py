"""カメラキャリブレーションモジュール.

カメラキャリブレーションを行う
@author kawanoichi
"""
from typing import List
import argparse
from color_changer import Color, ColorChanger
from camera_coordinate_calibrator import CameraCoordinateCalibrator
from camera_interface import CameraInterface
from game_area_info import GameAreaInfo


class CameraCalibrator:
    """ゲームエリア認識クラス.

    Attributes:
        MODE_AREA_XSIZE: 最頻値を求める範囲のxサイズ(奇数)
        MODE_AREA_YSIZE: 最頻値を求める範囲のyサイズ(奇数)
    """

    # テンプレートサイズ(奇数)
    MODE_AREA_XSIZE = 5
    MODE_AREA_YSIZE = 5

    def __init__(self, camera_id: int, cali_img_save_path="cali_course.png") -> None:
        """CameraCalibrationのコンストラクタ.

        Args:
            camera_id: 撮影カメラID
            cali_img_save_path: キャリブレーション用画像保存パス
        """
        # キャリブレーション用画像の取得
        self.__camera_interface = CameraInterface(camera_id)
        self.__calibration_img = self.__camera_interface.capture_frame(cali_img_save_path)

        self.__color_changer = ColorChanger()
        self.__coord = CameraCoordinateCalibrator(self.__calibration_img)

    def start_camera_calibration(self) -> None:
        """カメラキャリブレーションを行う関数."""
        # GUIから座標取得
        self.__coord.show_window()

    def make_game_area_info(self, game_save_path="game_course.png") -> None:
        """ゲームエリア情報作成を行う関数."""
        # ゲームエリア画像を取得
        game_area_img = self.__camera_interface.capture_frame(game_save_path)
        # 6色変換
        color_save_path = "color_" + game_save_path
        self.__color_changer.change_color(game_area_img, color_save_path)

        # カラーIDを格納する配列を宣言
        block_id_list = []
        base_id_list = []
        end_id = []

        # ブロック置き場
        for i, point in enumerate(self.__coord.block_point):
            # 最頻値を求めてブロックの色を判定
            color_id = self.__color_changer.calculate_mode_color(point[0],
                                                                 point[1],
                                                                 CameraCalibrator.MODE_AREA_XSIZE,
                                                                 CameraCalibrator.MODE_AREA_YSIZE)
            block_id_list.append(color_id)
            print("ブロック置き場%d:%s" % (i, Color(color_id).name))
        # ベースサークル置き場
        for i, base in enumerate(self.__coord.base_circle):
            # 最頻値を求めてブロックの色を判定
            color_id = self.__color_changer.calculate_mode_color(base[0],
                                                                 base[1],
                                                                 CameraCalibrator.MODE_AREA_XSIZE,
                                                                 CameraCalibrator.MODE_AREA_YSIZE)
            base_id_list.append(color_id)
            print("ベースサークル置き場%d:%s" % (i, Color(color_id).name))
        # 端点サークル置き場
        # 最頻値を求めてブロックの色を判定
        color_id = self.__color_changer.calculate_mode_color(
            self.__coord.end_point[0][0], self.__coord.end_point[0][1],
            CameraCalibrator.MODE_AREA_XSIZE, CameraCalibrator.MODE_AREA_YSIZE)
        end_id.append(color_id)
        print("ボーナスブロック置き場%d:%s" % (i, Color(color_id).name))

        # ゲームエリア情報を作成
        GameAreaInfo.block_id_list = block_id_list
        GameAreaInfo.base_id_list = base_id_list
        GameAreaInfo.end_id = end_id


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
    camera_calibration.make_game_area_info()
    print("CameraCalibrator 終了")
