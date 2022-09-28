"""カメラインターフェースモジュール.

カメラから画像を取得、保存を行う
@author kawanoichi
実行コマンド
    接続されているカメラIDを表示する
    $ python camera_interface.py
    カメラから画像を取得し、保存する
    $ python camera_interface.py -id <カメラID>
"""
import argparse
import os

# NOTE: cv2.VideoCaptureの処理時間短縮(import cv2の前に書く必要あり)
# 参考資料: https://qiita.com/youichi_io/items/b894b85d790720ea2346
os.environ["OPENCV_VIDEOIO_MSMF_ENABLE_HW_TRANSFORMS"] = "0"
import cv2  # noqa


class CameraInterface:
    """カメラ仲介クラス."""

    def __init__(self, camera_id=1) -> None:
        """CameraInterfaceのコンストラクタ.

        Args:
            camera_id (int): カメラ番号
        """
        # 画像取得するカメラを選択する（引数はカメラ番号）
        self.camera = cv2.VideoCapture(camera_id)

    def capture_frame(self, save_path: str) -> cv2.Mat:
        """カメラから画像を取得、保存.

        Args:
            save_path (str): 画像保存のパス

        Returns:
            cv2.Mat: 画像データ
        """
        # successed: 画像が取得が成功したか(True or False)
        # frame: 画像
        successed, frame = self.camera.read()
        if successed:
            # 画像の保存
            cv2.imwrite(save_path, frame)
            print("画像を保存しました")
        else:
            print("画像を取得できませんでした")

        return cv2.imread(save_path)

    @staticmethod
    def check_camera_connection() -> None:
        """カメラが接続されているかどうかを一覧表示."""
        print('接続されているカメラの番号を調べています...\n')
        true_cameras = []

        # カメラ番号を0～9まで変えて、COM_PORTに認識されているカメラを探す
        for camera_number in range(0, 10):
            try:
                camera = cv2.VideoCapture(camera_number)
                successed, _ = camera.read()
            except cv2.error:
                successed = False
            if successed:
                true_cameras.append(camera_number)
                print("カメラ番号->", camera_number, "接続済")

        print("\n接続されているカメラは", len(true_cameras), "台です。")
        print("カメラ番号を調べ終わりました。")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="使用例\n"
                                                 " 接続されているカメラIDを表示する\n"
                                                 " $ python camera_interface.py\n"
                                                 " カメラから画像を取得し、保存する\n"
                                                 " $ python camera_interface.py -id 0 (0はカメラID)",
                                     formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument("-id", "--camera-id", type=int, help="カメラから画像を取得し、保存する")
    args = parser.parse_args()

    # カメラIDがない時、接続されているカメラを取得し、表示する
    if args.camera_id is None:
        CameraInterface.check_camera_connection()
        exit(0)

    # カメラから画像を取得し、保存する
    save_path = "course.png"
    camera_interface = CameraInterface(args.camera_id)
    camera_interface.capture_frame(save_path)
