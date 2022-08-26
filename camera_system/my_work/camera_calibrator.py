import cv2

import camera_coordinate_calibrator
import color_changer

class CameraCalibration:
    def __init__(self, img):
        self.img = img

    def camera_calibration_start(self):
        coord = camera_coordinate_calibrator()
        coord.show_window()
        print("ブロック置き場: %s" % coord.block_point)
        print("ベースサークル: %s" % coord.base_circle)
        print("端点サークル: %s" % coord.end_point)

if __name__ == "__main__":
    img = cv2.imread("course.png")
    camera_calibration = CameraCalibration()
    print("終了")