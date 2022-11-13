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

    attributes:
        MAX_TIME: 最大計測時間
        ROTATION_BLOCK_PWM: ブロックを保持した時の回頭のPWM値
        ROTATION_NO_BLOCK_PWM: ブロックを保持していない時の回頭のPWM値
        ROTATION_BLOCK_TABLE: ブロックを保持した時の回頭のパラメータ(45度単位で0~360度)
        ROTATION_NO_BLOCK_TABLE: ブロックを保持していない時の回頭のパラメータ(45度単位で0~360度)
        VERTICAL_TIME: 縦調整の動作時間
        DIAGONAL_TIME: 斜め調整の動作時間
        SLEEP_TIME: 回頭前後のスリープ時間
    """

    MAX_TIME = 120
    ROTATION_BLOCK_PWM = 70
    ROTATION_NO_BLOCK_PWM = 70
    ROTATION_BLOCK_TABLE = {0: {"angle": 0, "time": 0},
                            45: {"angle": 35, "time": 0.405},
                            90: {"angle": 85, "time": 0.661},
                            135: {"angle": 132, "time": 0.920},
                            180: {"angle": 177, "time": 1.165},
                            225: {"angle": 225, "time": 120},  # 失敗率の高い角度
                            270: {"angle": 270, "time": 120},  # 想定しない角度
                            315: {"angle": 315, "time": 120}}  # 想定しない角度
    ROTATION_NO_BLOCK_TABLE = {0: {"angle": 0, "time": 0},
                               45: {"angle": 30, "time": 0.342},
                               90: {"angle": 78, "time": 0.575},
                               135: {"angle": 124, "time": 0.778},
                               180: {"angle": 170, "time": 1.049},
                               225: {"angle": 216, "time": 1.281},
                               270: {"angle": 270, "time": 120},  # 想定しない角度
                               315: {"angle": 315, "time": 120}}  # 想定しない角度
    VERTICAL_TIME = 0.2558
    DIAGONAL_TIME = 0.2620
    SLEEP_TIME = 0.1
    CORRECTION_BLOCK_PWM = 73       # ブロック保持時の回頭補正に用いるPWM値
    CORRECTION_NO_BLOCK_PWM = 62    # ブロック未保持時の回頭補正に用いるPWM値

    def __eq__(self, other) -> bool:
        """オブジェクトの等価比較をする.

        Returns:
            bool: 等価比較の結果
        """
        return self.__dict__ == other.__dict__  # 全てのインスタンス変数を比較

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
        conv_angle = angle % 360  # 時計回りの場合の角度に直す（0~360）
        current_edge = self.current_edge
        if current_edge == "left":
            if conv_angle >= 90 and conv_angle <= 225:  # 後方に回頭する場合エッジを反転する
                return "right"
            else:
                return current_edge
        elif current_edge == "right":
            if conv_angle >= 135 and conv_angle <= 270:  # 後方に回頭する場合エッジを反転する
                return "left"
            else:
                return current_edge
        else:  # current_edge == "none"
            if conv_angle >= 45 and conv_angle <= 135:  # 右側に回頭する場合エッジを右にする
                return "right"
            elif conv_angle >= 225 and conv_angle <= 315:
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
