"""ゲーム動作モジュール.

ゲーム動作のコマンド生成やコスト計算をする
@author mutotaka0426
"""

from abc import ABCMeta, abstractmethod


class Edge:
    """エッジを疑似的なstatic変数として保持するためのクラス.

    __current_edge: 現在のエッジ("left" or "right" or "none")
    """

    __current_edge = "left"

    @staticmethod
    def get_current_edge() -> str:
        """Getter.

        Returns:
            str: 現在のエッジ
        """
        return Edge.__current_edge

    @staticmethod
    def set_current_edge(next_edge: str) -> None:
        """Setter.

        Args:
            next_edge: "left" or "right" or "none"
        """
        Edge.__current_edge = next_edge


class GameMotion(metaclass=ABCMeta):
    """ゲーム動作の親クラス.

    ttributes:
        MAX_TIME: 最大計測時間
        ROTATION_PWM: 回頭のPWM値
        ROTATION_TIME: 回頭の動作時間(45度単位で0~360度)
        VERTICAL_TIME: 縦調整の動作時間
        DIAGONAL_TIME: 斜め調整の動作時間
    """

    MAX_TIME = 120
    ROTATION_PWM = 100
    ROTATION_TIME = [0, 45, 90, 135, 180, 225, 270, 315]  # TODO: 回頭の動作時間を測る
    VERTICAL_TIME = 0.2558
    DIAGONAL_TIME = 0.2620

    @abstractmethod
    def generate_command(self) -> str:
        """ゲーム動作に必要なコマンドを生成する抽象メソッド.

        Returns:
            str: コマンド
        """
        pass

    @abstractmethod
    def get_cost(self) -> float:
        """ゲーム動作のコストを計算する抽象メソッド.

        Returns:
            float: コスト
        """
        pass

    def get_next_edge(self, angle: int) -> str:
        """現在のエッジと回頭角度から次のエッジを求める.

        Args:
            angle: 方向転換の角度

        Returns:
            str: 次のエッジ("left" or "right" or "none")
        """
        angle = angle % 360  # 時計回りの場合の角度に直す（0~360）
        current_edge = self.current_edge
        if current_edge == "left":
            if angle >= 90 and angle <= 225:  # 後方に回頭する場合エッジを反転する
                return "right"
            else:
                return current_edge
        elif current_edge == "right":
            if angle >= 135 and angle <= 270:  # 後方に回頭する場合エッジを反転する
                return "left"
            else:
                return current_edge
        else:  # current_edge == "none"
            if angle >= 45 and angle <= 135:  # 右側に回頭する場合エッジを右にする
                return "right"
            elif angle >= 225 and angle <= 315:
                return "left"  # 左側に回頭する場合エッジを左にする
            else:
                return current_edge

    @property
    def current_edge(self) -> str:
        """Getter.

        Returns:
            str: "left" or "right" or "none"
        """
        return Edge.get_current_edge()

    @current_edge.setter
    def current_edge(self, next_edge: str) -> None:
        """Setter.

        Args:
            next_edge: "left" or "right" or "none"
        """
        Edge.set_current_edge(next_edge)
