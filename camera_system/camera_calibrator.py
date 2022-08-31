"""カメラキャリブレーションモジュール.

カメラキャリブレーションを行う
@author kawanoichi
"""
import cv2
from typing import List
from color_changer import ColorChanger
from color_changer import Color
from camera_coordinate_calibrator import CameraCoordinateCalibrator
from game_info import GameInfo


class CameraCalibration:
    """ゲームエリア認識クラス.

    Attributes:
        TEMP_XSIZE: 最頻値を求める範囲のxサイズ(奇数)
        TEMP_YSIZE: 最頻値を求める範囲のyサイズ(奇数)
    """

    # テンプレートサイズ(奇数)
    TEMP_XSIZE = 5
    TEMP_YSIZE = 5

    def __init__(self, read_path):
        """CameraCalibrationのコンストラクタ.

        Args:
            read_path: コース画像パス
        """
        self.__img = cv2.imread(read_path)
        self.__save_path = "result_" + read_path
        self.__color_changer = ColorChanger()
        self.__coord = CameraCoordinateCalibrator()

    def camera_calibration_start(self):
        """カメラキャリブレーションを行う関数."""
        # GUIから座標取得
        self.__coord.show_window(self.__img)

    def make_game_info(self):
        """コース情報作成を行う関数."""
        # 6色変換
        self.__color_changer.change_color(self.__img, self.__save_path)

        # 座標からカラーIDを取得
        block_id_list = []
        base_id_list = []
        end_id = []

        # ブロック置き場
        for i, point in enumerate(self.__coord.block_point):
            color_id = self.__color_changer.mode_color(
                point[0], point[1], CameraCalibration.TEMP_XSIZE, CameraCalibration.TEMP_YSIZE)
            block_id_list.append(color_id)
            print("ブロック置き場%d:%s" % (i, Color(color_id).name))
        # ベースサークル置き場
        for i, base in enumerate(self.__coord.base_circle):
            color_id = self.__color_changer.mode_color(
                base[0], base[1], CameraCalibration.TEMP_XSIZE, CameraCalibration.TEMP_YSIZE)
            base_id_list.append(color_id)
            print("ベースサークル置き場%d:%s" % (i, Color(color_id).name))
        # 端点サークル置き場
        color_id = self.__color_changer.mode_color(
            self.__coord.end_point[0][0], self.__coord.end_point[0][1],
            CameraCalibration.TEMP_XSIZE, CameraCalibration.TEMP_YSIZE)
        end_id.append(color_id)
        print("ボーナスブロック置き場%d:%s" % (i, Color(color_id).name))

        # コース情報を作成
        GameInfo.block_id_list = block_id_list
        GameInfo.base_id_list = base_id_list
        GameInfo.end_id = end_id

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
    read_path = "course.png"
    save_path = "result_" + read_path
    camera_calibration = CameraCalibration(read_path)
    camera_calibration.camera_calibration_start()
    camera_calibration.make_game_info()
    print("CameraCalibration 終了")
