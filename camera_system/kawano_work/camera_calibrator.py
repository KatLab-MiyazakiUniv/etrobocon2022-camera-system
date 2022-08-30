"""カメラキャリブレーションモジュール.
@author
"""
import cv2
import color_changer
import camera_coordinate_calibrator
import game_info


class CameraCalibration:
    """
    1. GUIから座標取得
    2. 6色変換
    3. 座標のところからカラーIDを取得
    """
    # テンプレートサイズ
    TEMP_XSIZE = 5
    TEMP_YSIZE = 5

    def __init__(self, read_path):
        # global変数を宣言
        self.__img = cv2.imread(read_path)
        self.__save_path = "result_" + read_path

        # 他のファイルクラスのインスタンス化
        self.coord = camera_coordinate_calibrator.CameraCoordinateCalibrator()
        self.color_changer = color_changer.ColorChanger()

        # カラーid
        self.color_id_dic = {"0": "赤", "1": "黄", "2": "緑", "3": "青", "4": "白"}

        # 座標
        self.__block_point = []
        self.__base_circle = []
        self.__end_point = []

    def camera_calibration_start(self):
        """ カメラキャリブレーションを行う関数 """
        # GUIから座標取得
        print("\n座標取得")
        self.__block_point, self.__base_circle, self.__end_point = self.coord.show_window(
            self.__img)

    def make_game_info(self):
        # 6色変換
        self.color_changer.change_color(self.__img, self.__save_path)
        # 座標からカラーIDを取得
        block_id_list = []
        base_id_list = []
        end_id_list = []

        # ブロック置き場
        for i in range(len(self.__block_point)):
            color_id = self.color_changer.mode_color(
                self.__block_point[i][0], self.__block_point[i][1], CameraCalibration.TEMP_XSIZE, CameraCalibration.TEMP_YSIZE)
            block_id_list.append(color_id)
            print("ブロック置き場%d:%s" % (i, self.color_id_dic[str(color_id)]))
        # ベースサークル置き場
        for i in range(len(self.__base_circle)):
            color_id = self.color_changer.mode_color(
                self.__base_circle[i][0], self.__base_circle[i][1], CameraCalibration.TEMP_XSIZE, CameraCalibration.TEMP_YSIZE)
            base_id_list.append(color_id)
            print("ベースサークル置き場%d:%s" % (i, self.color_id_dic[str(color_id)]))
        # 端点サークル置き場
        color_id = self.color_changer.mode_color(
            self.__end_point[0][0], self.__end_point[0][1], CameraCalibration.TEMP_XSIZE, CameraCalibration.TEMP_YSIZE)
        end_id_list.append(color_id)
        print("ボーナスブロック置き場%d:%s" % (i, self.color_id_dic[str(color_id)]))

        # コース情報を作成
        game_info.GameInfo.color_block_setter(block_id_list)
        game_info.GameInfo.base_color_block_setter(base_id_list)
        game_info.GameInfo.bonus_block_setter(end_id_list)


if __name__ == "__main__":
    read_path = "course.png"
    save_path = "result_" + read_path
    camera_calibration = CameraCalibration(read_path)
    camera_calibration.camera_calibration_start()
    print("CameraCalibration 終了")
