"""座標取得GUIツール

画像を表示し、クリックした座標を保持する
@author miyashita64
@note 参考:https://techacademy.jp/magazine/51035
"""

import cv2

class CoordinateGetter:
    def __init__(self, img):
        # メンバを初期化する.
        self.img = img
        self.window_name = "course"
        # 画像を表示する.
        self.showImage()

    def showImage(self):
        cv2.imshow(self.window_name, self.img)
        cv2.setMouseCallback(self.window_name, self.onMouse)
        cv2.waitKey(0)

    def onMouse(self, event, x, y, flags, params):
        if event == cv2.EVENT_LBUTTONDOWN:
            print(x, y)
            # ウィンドウを閉じる.
            cv2.destroyWindow(self.window_name)

def main():
    # 画像を取得する.
    img = cv2.imread('course.png')
    CoordinateGetter(img)

if __name__ == "__main__":
    main()