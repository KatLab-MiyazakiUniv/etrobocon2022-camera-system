"""座標取得GUIツール.

画像を表示し、クリックした座標を保持する
@author miyashita64 mutotaka0426
@note 参考: https://techacademy.jp/magazine/51035
"""

import cv2
from typing import List


class CoordinateGetter:
    """画像から座標を取得するクラス.

    Attributes:
        __block_point: ブロック置き場の座標リスト
        __base_circle: ベースサークルの座標リスト
    """

    def __init__(self, file_name: str) -> None:
        """カメラシステムのコンストラクタ.

        Args:
            file_name (str, optional): 入力画像ファイルのパス.
        """
        # メンバを初期化する.
        self.__block_point = []
        self.__base_circle = []

        # GUIツールを設定する
        self.__img = cv2.imread(file_name)
        self.__window_name = "Coordinate Getter"
        # 画像を表示する.
        self.__showImage()

    def __showImage(self) -> None:
        """画像を表示する関数."""
        cv2.imshow(self.__window_name, self.__img)
        cv2.setMouseCallback(self.__window_name, self.__setCoordinate)
        cv2.waitKey(0)

    def __setCoordinate(self, event, x, y, flags, params) -> None:
        """マウス操作で取得した座標を各座標リストにセットするコールバック関数.

        Args:
            event (str, optional): イベントを示す変数.
            x, y (int, optional): イベント発生時のマウスポインタの座標.
            NOTE: OpenCVのコースバック関数については https://qr.paps.jp/opDWK を参照
        """
        # 最初の8クリックはブロック置き場の座標を取得する
        if len(self.__block_point) < 8:
            if event == cv2.EVENT_LBUTTONDOWN:
                print('ブロック置き場{}：{} {}'.format(len(self.__block_point)+1, x, y))
                self.__block_point.append([x, y])
        # 次の4クリックはベースサークルの座標を取得する
        elif len(self.__base_circle) < 4:
            if event == cv2.EVENT_LBUTTONDOWN:
                print('ベースサークル{}：{} {}'.format(len(self.__base_circle)+1, x, y))
                self.__base_circle.append([x, y])
        # ブロック置き場とベースサークルの座標を取得したら終了する
        else:
            # ウィンドウを閉じる.
            cv2.destroyWindow(self.__window_name)

    @property
    def block_point(self) -> List[int]:
        """Getter.

        Returns:
            List[int]: ブロック置き場の座標リスト ([x座標, y座標]の形で格納)
        """
        return self.__block_point

    @property
    def base_circle(self) -> List[int]:
        """Getter.

        Returns:
            List[int]: ベースサークルの座標リスト ([x座標, y座標]の形で格納)
        """
        return self.__base_circle
