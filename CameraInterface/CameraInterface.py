##
# @file CameraInterface.py
# @brief カメラから画像を取得、保存を行う
# @author kawano
# 実行コマンド PowerShell.exe -ExecutionPolicy RemoteSigned -File captureCameraInterface.ps1 カメラ番号
import os
# cv2.VideoCaptureの処理時間短縮(import cv2の前に書く必要あり)
# @see https://qiita.com/youichi_io/items/b894b85d790720ea2346
os.environ["OPENCV_VIDEOIO_MSMF_ENABLE_HW_TRANSFORMS"] = "0"
import cv2
import sys

# カメラ仲介クラス
class CameraInterface:
    ##
    # @brief コンストラクタ
    # @param cameraId カメラ番号
    def __init__(self, cameraId):
        # 画像取得するカメラを選択する（引数はカメラ番号）
        self.camera = cv2.VideoCapture(cameraId)

    ##
    # @brief カメラから画像を取得、保存を行う
    def getFrame(self):
        # successed   : 画像が取得が成功したか(True or False)
        # frame : 画像
        successed, frame = self.camera.read()
        if successed:
            # 画像の保存
            cv2.imwrite("course.png", frame)
            print("画像を保存しました")
        else:
            print("画像を取得できませんでした")

    ##
    # @brief カメラが接続されているかどうかを一覧表示
    @staticmethod
    def checkCameraConnection():
        print('接続されているカメラの番号を調べています...')
        trueCameras = []  # 空の配列を用意

        # カメラ番号を0～9まで変えて、COM_PORTに認識されているカメラを探す
        for cameraNumber in range(0, 10):
            try:
                camera = cv2.VideoCapture(cameraNumber)
                successed, frame = camera.read()
            except:
                successed = False
            if successed:
                trueCameras.append(cameraNumber)
                print("カメラ番号->", cameraNumber, "接続済")
            else:
                print("カメラ番号->", cameraNumber, "未接続")
        print("接続されているカメラは", len(trueCameras), "台です。")
        print("カメラのインデックスは", trueCameras, "です。")
        print("カメラ番号を調べ終わりました。")

if __name__ == "__main__":
    args = sys.argv
    if len(args) == 2:
        cameraInterface = CameraInterface(int(args[1]))
        cameraInterface.getFrame()
    else:
        print("Warning:コマンドライン引数にカメラIDを入力してください")
