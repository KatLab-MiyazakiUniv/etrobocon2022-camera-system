"""カメラキャリブレーションモジュール.

カメラキャリブレーションを行う
@author kawanoichi
"""
import cv2
from typing import List
from color_changer import Color, ColorChanger
from camera_coordinate_calibrator import CameraCoordinateCalibrator
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

    def __init__(self, read_path: str):
        """CameraCalibrationのコンストラクタ.

        Args:
            read_path: コース画像パス
        """
        self.__img = cv2.imread(read_path)
        self.__save_path = "color_" + read_path  # 6色変換後の画像の保存パス
        self.__color_changer = ColorChanger()
        self.__coord = CameraCoordinateCalibrator(self.__img)

    def start_camera_calibration(self) -> None:
        """カメラキャリブレーションを行う関数."""
        # GUIから座標取得
        self.__coord.show_window()

    def make_game_area_info(self, actual_course_img: cv2.Mat) -> None:
        """コース情報作成を行う関数."""
        # 6色変換
        self.__color_changer.change_color(actual_course_img, self.__save_path)

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

        # コース情報を作成
        GameAreaInfo.block_id_list = block_id_list
        GameAreaInfo.base_id_list = base_id_list
        GameAreaInfo.end_id = end_id

    @property
    def img(self) -> List[int]:
        """Getter.

        Returns:
            List[Tuple[int, int]]: コース画像
        """
        return self.__img

    @property
    def save_path(self) -> str:
        """Getter.

        Returns:
            str: 6色変換後の保存パス
        """
        return self.__save_path


if __name__ == "__main__":
    read_path = "test_image.png"
    actual_course_img = cv2.imread(read_path)
    camera_calibration = CameraCalibrator(read_path)
    camera_calibration.start_camera_calibration()
    camera_calibration.make_game_area_info(actual_course_img)
    print("CameraCalibrator 終了")
