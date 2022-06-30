##
# @file CheckConnectCamera.py
# @brief 接続されているカメラ番号の確認
# @author kawano

import cv2
import sys

##    
# @brief カメラが接続されているかどうかを一覧表示
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
    print("カメラのインデックスは", trueCameras,"です。")
    sys.exit("カメラ番号を調べ終わりました。")

if __name__ == "__main__":
    checkCameraConnection()