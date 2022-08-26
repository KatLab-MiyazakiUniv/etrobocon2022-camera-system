"""カメラキャリブレーションモジュール.
@author
"""
import cv2

import color_changer
import camera_coordinate_calibrator

import global_value as g #グローバル変数用ファイル

class CameraCalibration:
    """
    1. GUIから座標取得
    2. 6色変換
    3. 座標のところからカラーIDを取得
    """
    def __init__(self, read_path):
        # global変数を宣言
        g.save_path = "result_" + read_path
        g.img = cv2.imread(read_path)

        # 他のファイルクラスのインスタンス化
        self.coord = camera_coordinate_calibrator.CameraCoordinateCalibrator()
        self.color_changer = color_changer.ColorChanger()
        
        # テンプレートサイズ
        self.temp_xsize = 5
        self.temp_ysize = 5

        self.color_id_dic = {"0":"赤", "1":"黄", "2":"緑", "3":"青", "4":"白"}

    def camera_calibration_start(self):
        # GUIから座標取得
        __block_point, __base_circle, __end_point= self.coord.show_window()
        # 6色変換
        self.color_changer.change_color()
        # 座標からカラーIDを取得
        for i in range(len(__block_point)):
            color_id = self.color_changer.mode_color(__block_point[i][0], __block_point[i][1], self.temp_xsize, self.temp_ysize)
            print("ブロック置き場%d:%s" % (i,self.color_id_dic[str(color_id)]))

if __name__ == "__main__":
    read_path = "course.png"
    camera_calibration = CameraCalibration(read_path)
    camera_calibration.camera_calibration_start()
    print("CameraCalibration 終了")