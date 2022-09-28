"""カメラ画像の座標取得するためのモジュール.

カメラ画像を表示し、クリックした座標を保持する
@author miyashita64 mutotaka0426 kawanoichi
@note 参考: https://techacademy.jp/magazine/51035
@note 参考:
    - [【Python】Tkinterによる画像表示をわかりやすく解説](https://onl.bz/5Bwmt1b)
    - [Tkinterで作成したウインドウにOpenCV-Pythonの画像を表示](https://onl.bz/sTkdsGb)
    - [Tkinter: イベントを検出する（クリック・キー入力・マウス移動）](https://onl.bz/7sMdTKw)
    - [Python Tkinter Canvasについて](https://onl.bz/mWGj8f9)
    - [【Python/tkinter】ウィジェットの配置(pack)](https://onl.bz/etTHi5T)
"""

import cv2
import tkinter as tk
from PIL import Image, ImageTk
from typing import List, Tuple


class CameraCoordinateCalibrator:
    """カメラ画像から座標を取得するクラス."""

    def __init__(self, img: cv2.Mat) -> None:
        """CameraCoordinateCalibratorのコンストラクタ.

        Args:
            img (cv2.Mat): 画像データ
        """
        # メンバを初期化する
        self.__block_point = []  # ブロック置き場の座標リスト
        self.__base_circle = []  # ベースサークルの座標リスト
        self.__end_point = []  # 端点サークルの座標リスト
        self.__calibration_img = img

    def show_window(self) -> None:
        """画像取得ツールを起動する関数."""
        # 画像情報を取得する
        img_height = self.__calibration_img.shape[0]  # 画像の高さ
        img_width = self.__calibration_img.shape[1]  # 画像の横幅

        # ウィンドウを定義する
        self.__window = tk.Tk()
        self.__window.title("Camera Coordinate Calibrator")
        # ウィンドウサイズ: (画像の横幅 + UIの横幅) x 画像の高さ
        self.__window.geometry("%dx%d" % (img_width+200, img_height))

        # 取得状況を表示するMessageを定義する
        self.__message = tk.Message(self.__window, text="", font=("", 10), bg="#ddd", aspect=500)
        # Messageを配置する
        self.__message.place(x=img_width+10, y=150, width=180)

        # OpenCVで取得した画像を変換する
        img_rgb = cv2.cvtColor(self.__calibration_img, cv2.COLOR_BGR2RGB)  # imreadはBGRなのでRGBに変換
        img_pil = Image.fromarray(img_rgb)    # RGBからPILフォーマットへ変換
        img_tk = ImageTk.PhotoImage(img_pil)  # ImageTkフォーマットへ変換

        # ウィジェットを定義する
        # 画像を表示するCanvasを定義する
        canvas = tk.Canvas(self.__window, width=img_width, height=img_height)
        # コールバック関数を指定する ("<Button-1>"は左クリックボタン)
        canvas.bind("<Button-1>", self.__set_coordinate)
        # Canvasを配置する
        canvas.pack(side=tk.LEFT)
        # Canvasに画像を設置する
        canvas.create_image(0, 0, image=img_tk, anchor=tk.NW)

        # 直前の操作を取り消すためのButtonを定義する
        reset_previous_operation = tk.Button(self.__window, text="Reset Prev")
        # コールバック関数を指定する ("<Button-1>"は左クリックボタン)
        reset_previous_operation.bind("<Button-1>", self.__reset_previous_coordinate)
        # 直前の操作を取り消すButtonを配置する
        reset_previous_operation.place(x=img_width+10, y=80, width=180, height=50)

        # OK用のButtonを定義する
        ok_button = tk.Button(self.__window, text="OK")
        # コールバック関数を指定する ("<Button-1>"は左クリックボタン)
        ok_button.bind("<Button-1>", self.__complete_input_coordinate)
        # OKボタンを配置する
        ok_button.place(x=img_width+10, y=20, width=180, height=50)

        # ウィンドウを表示する
        self.__window.mainloop()

    def __set_coordinate(self, event) -> None:
        """マウス操作で取得した座標を各座標リストにセットするコールバック関数.

        Args:
            event: マウスイベント
        """
        # 最初の8クリックはブロック置き場の座標を取得する
        if len(self.__block_point) < 8:
            # Messageを更新.
            self.__message["text"] += "ブロック置き場%d:(%d,%d)\n" % (
                len(self.__block_point)+1, event.x, event.y)
            self.__block_point.append((event.x, event.y))
        # 次の4クリックはベースサークルの座標を取得する
        elif len(self.__base_circle) < 4:
            # Messageを更新
            self.__message["text"] += "ベースサークル%d:(%d,%d)\n" % (
                len(self.__base_circle)+1, event.x, event.y)
            self.__base_circle.append((event.x, event.y))
        # 最後の1クリックは端点サークルの座標を取得する
        elif len(self.__end_point) < 1:
            # Messageを更新.
            self.__message["text"] += "端点サークル:(%d,%d)\n" % (
                event.x, event.y)
            self.__end_point.append((event.x, event.y))
        else:
            print('[Warning] 座標入力を完了しています')

    def __reset_previous_coordinate(self, event) -> None:
        """直前の操作を取り消すボタンで入力座標の削除とメッセージを削除するコールバック関数.

        Args:
            event: リセットボタンのクリックイベント
        """
        if len(self.__end_point) != 0:
            self.__end_point.pop()
            self.__remove_tail_message_line()
        elif len(self.__base_circle) != 0:
            self.__base_circle.pop()
            self.__remove_tail_message_line()
        elif len(self.__block_point) != 0:
            self.__block_point.pop()
            self.__remove_tail_message_line()
        else:
            print("[Warning] 取り消すべき操作がありません")

    def __remove_tail_message_line(self) -> None:
        """最終行のメッセージを削除する関数."""
        # 末尾の改行文字を除いた改行文字の位置を末尾から検索する
        i = self.__message["text"][:-1].rfind('\n')
        # 最終行のメッセージを削除する
        self.__message["text"] = self.__message["text"][:i+1]

    def __complete_input_coordinate(self, event) -> None:
        """OKボタンで画面を閉じるためのコールバック関数.

        Args:
            event: リセットボタンのクリックイベント
        """
        if len(self.__block_point) > 8 and len(self.__base_circle) >= 4 and len(self.__end_point) >= 1:  # noqa
            # ウィンドウを閉じる
            self.__window.destroy()
        else:
            print("[Warning] 未入力の座標があります")

    @property
    def block_point(self) -> List[Tuple[int, int]]:
        """Getter.

        Returns:
            List[Tuple[int, int]]: ブロック置き場の座標リスト ([x座標, y座標]の形で格納)
        """
        return self.__block_point

    @property
    def base_circle(self) -> List[Tuple[int, int]]:
        """Getter.

        Returns:
            List[Tuple[int, int]]: ベースサークルの座標リスト ([x座標, y座標]の形で格納)
        """
        return self.__base_circle

    @property
    def end_point(self) -> List[Tuple[int, int]]:
        """Getter.

        Returns:
            List[Tuple[int, int]]: 端点サークルの座標リスト ([x座標, y座標]の形で格納)
        """
        return self.__end_point


if __name__ == "__main__":
    read_path = "test_image.png"
    img = cv2.imread(read_path)
    coord = CameraCoordinateCalibrator(img)
    coord.show_window()
    print("ブロック置き場: %s" % coord.block_point)
    print("ベースサークル: %s" % coord.base_circle)
    print("端点サークル: %s" % coord.end_point)
