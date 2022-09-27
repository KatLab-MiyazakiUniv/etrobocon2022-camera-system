"""カメラキャリブレーションモジュール.

カメラキャリブレーションを行う
@author kawanoichi
実行コマンド
    接続されているカメラIDを表示する
    $ python camera_calibrator.py
    カメラから画像を取得し、保存する
    $ python camera_calibrator.py -id <カメラID>
"""
import numpy as np
import argparse
from color_changer import Color, ColorChanger
from camera_coordinate_calibrator import CameraCoordinateCalibrator
from camera_interface import CameraInterface
from game_area_info import GameAreaInfo


class CameraCalibrator:
    """ゲームエリア認識クラス.

    Attributes:
        SEARCH_AREA_XSIZE (int): ブロックの色を求めるための領域xサイズ(奇数)
        SEARCH_AREA_YSIZE (int): ブロックの色を求めるための領域xサイズ(奇数)
        COLOR_BLOCK_NUM (int): カラーブロックの個数(8個)
        BASE_BLOCK_NUM (int): ベースエリアブロックの個数(4個)
        BONUS_BLOCK_NUM (int): ボーナスブロックの個数(1個)
        VALIDITY_COLOR_NUM (int): カラーブロックに使用されている色の種類の数(赤、黄、緑、青の4種類)
    """

    SEARCH_AREA_XSIZE = 5
    SEARCH_AREA_YSIZE = 5

    COLOR_BLOCK_NUM = 8
    BASE_BLOCK_NUM = 4
    BONUS_BLOCK_NUM = 1

    VALIDITY_COLOR_NUM = 4

    def __init__(self, camera_id: int, cali_img_save_path="cali_course.png") -> None:
        """CameraCalibrationのコンストラクタ.

        Args:
            camera_id (int): 撮影カメラ番号
            cali_img_save_path (str): キャリブレーション用画像保存パス
        """
        # キャリブレーション用画像の取得
        self.__camera_interface = CameraInterface(camera_id)
        self.__calibration_img = self.__camera_interface.capture_frame(cali_img_save_path)

        self.__color_changer = ColorChanger()
        self.__coord = CameraCoordinateCalibrator(self.__calibration_img)

        # ブロックの色を判定するための配列を宣言(行:各ブロック, 行：各色)
        self.count_point = np.zeros(
            CameraCalibrator.COLOR_BLOCK_NUM*CameraCalibrator.VALIDITY_COLOR_NUM
        ).reshape(CameraCalibrator.COLOR_BLOCK_NUM, CameraCalibrator.VALIDITY_COLOR_NUM)
        self.count_base = np.zeros(
            CameraCalibrator.BASE_BLOCK_NUM*CameraCalibrator.VALIDITY_COLOR_NUM
        ).reshape(CameraCalibrator.BASE_BLOCK_NUM, CameraCalibrator.VALIDITY_COLOR_NUM)

    def start_camera_calibration(self) -> None:
        """カメラキャリブレーションを行う関数."""
        # GUIから座標取得
        self.__coord.show_window()

    def make_game_area_info(self, is_left_course=True, game_save_path="game_course.png") -> None:
        """ゲームエリア情報作成を行う関数.

        Args:
            is_left_course (bool): 左コースの場合 True. Defaults to True.
            game_save_path (str): ゲームエリア画像保存パス
        """
        # ゲームエリア画像を取得
        game_area_img = self.__camera_interface.capture_frame(game_save_path)

        # 6色変換
        color_save_path = "color_" + game_save_path
        self.__color_changer.change_color(game_area_img, color_save_path)

        # 色IDを格納する配列を宣言
        block_color_list = np.zeros(CameraCalibrator.COLOR_BLOCK_NUM)
        base_color_list = np.zeros(CameraCalibrator.BASE_BLOCK_NUM)
        bonus_color = np.zeros(CameraCalibrator.BONUS_BLOCK_NUM)

        # ブロックの色を調べる領域のピクセル数を求める
        area_pixel_sum = CameraCalibrator.SEARCH_AREA_XSIZE*CameraCalibrator.SEARCH_AREA_XSIZE

        # カラーブロックの色IDを求める
        for i, point in enumerate(self.__coord.block_point):
            # ブロック上の領域に存在する色の種類とピクセル数を取得
            color_uniqs, color_pixel_sum = self.__color_changer.search_color(
                point[0],
                point[1],
                CameraCalibrator.SEARCH_AREA_XSIZE,
                CameraCalibrator.SEARCH_AREA_YSIZE)
            # 色の種類とピクセル数を配列に格納
            # 第2引数はindexと色IDを合わせるために-1
            # 第3引数は色を求める際に領域に対する割合で比較できるように各色のピクセル数÷全体のピクセル数
            np.put(self.count_point[i], color_uniqs-1,
                   color_pixel_sum/area_pixel_sum)
        # 認識したブロックの数を把握するための配列
        color_count = np.zeros(CameraCalibrator.VALIDITY_COLOR_NUM)  # (赤、黄、緑、青)
        # 各ブロックの領域に対する色の割合が高い順に色IDを割り振る
        for i in range(block_color_list.shape[0]):
            # 配列の最大値のインデックスを取得
            max_index = np.unravel_index(np.argmax(self.count_point), self.count_point.shape)
            # ブロックに対する色IDを格納する
            block_color_list[max_index[0]] = max_index[1]+1  # indexと色IDを合わせるために+1
            # 認識した色をカウント
            color_count[max_index[1]] += 1
            # 2回認識した色を候補から外す
            if color_count[max_index[1]] == 2:
                # -1を代入して優先順位を小さくする
                self.count_point[:, max_index[1]] = -1
            # 色の判別が終わったブロックを候補から外す
            self.count_point[max_index[0], :] = -1

        # ベースサークルの色IDを求める
        for i, base in enumerate(self.__coord.base_circle):
            # ブロック上の領域に存在する色の種類とピクセル数を取得
            color_uniqs, color_pixel_sum = self.__color_changer.search_color(
                base[0],
                base[1],
                CameraCalibrator.SEARCH_AREA_XSIZE,
                CameraCalibrator.SEARCH_AREA_YSIZE)
            # 色の種類とピクセル数を配列に格納
            np.put(self.count_base[i], color_uniqs-1,
                   color_pixel_sum/area_pixel_sum)
        # 各ブロックの領域に対する色の割合が高い順に色IDを割り振る
        for i in range(base_color_list.shape[0]):
            # 配列の最大値のインデックスを取得
            max_index = np.unravel_index(np.argmax(self.count_base), self.count_base.shape)
            # ブロックに対する色IDを格納する
            base_color_list[max_index[0]] = max_index[1]+1  # indexと色IDを合わせるために+1
            # 認識した色を候補から外す
            self.count_base[:, max_index[1]] = -1
            # 色の判別が終わったブロックを候補から外す
            self.count_base[max_index[0], :] = -1

        # ボーナスブロックの色IDを求める
        # ブロック上の領域に存在する色の種類とピクセル数を取得
        color_uniqs, color_pixel_sum = self.__color_changer.search_color(
            self.__coord.end_point[0][0],
            self.__coord.end_point[0][1],
            CameraCalibrator.SEARCH_AREA_XSIZE,
            CameraCalibrator.SEARCH_AREA_YSIZE)
        # ボーナスブロックはピクセル数の多い色にする(1個しかないから)
        bonus_color = color_uniqs[np.argmax(color_pixel_sum)]

        # ゲームエリア情報を作成
        GameAreaInfo.block_color_list = [Color(block_color) for block_color in block_color_list]
        GameAreaInfo.base_color_list = [Color(base_color) for base_color in base_color_list]
        GameAreaInfo.bonus_color = Color(bonus_color)

        # 確認のためにゲームエリア情報を出力
        print("Color Block\n", GameAreaInfo.block_color_list)
        print("Base Block\n", GameAreaInfo.base_color_list)
        print("Bonus Block\n", GameAreaInfo.bonus_color)

        # コースに応じて交点の色をセットする
        if is_left_course:
            GameAreaInfo.intersection_list = [Color.RED, Color.BLUE, Color.YELLOW, Color.GREEN]
        else:
            GameAreaInfo.intersection_list = [Color.BLUE, Color.RED, Color.GREEN, Color.YELLOW]


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
    # カメラキャリブレーションを行う
    camera_calibration.start_camera_calibration()
    # ゲームエリア情報作成を行う
    camera_calibration.make_game_area_info()

    print("CameraCalibrator 終了")
