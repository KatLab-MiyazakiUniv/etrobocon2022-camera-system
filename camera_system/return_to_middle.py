"""設置後復帰(→中点)のゲーム動作モジュール.

設置後復帰(→中点)のゲーム動作のコマンド生成やコスト計算をする
パラメータは https://github.com/KatLab-MiyazakiUniv/etrobocon2022/pull/89 を参照
@author mutotaka0426
"""

from game_motion import GameMotion


class ReturnToMiddle(GameMotion):
    """設置後復帰(→中点)のゲーム動作クラス."""

    def __init__(self, angle: int) -> None:
        """ReturnToMiddleのコンストラクタ.

        Args:
            angle: 方向転換の角度

        """
        self.__angle = angle

    def generate_command(self) -> str:
        """設置後復帰(→中点)のゲーム動作に必要なコマンドを生成するメソッド.

        Returns:
            str: コマンド
        """
        command_list = ""  # コマンドのリストを格納する文字列

        if self.__angle != 0:  # 回頭角度が0の場合はコマンドは生成しない
            # 回頭角度が正の数の場合時計回り，負の数の場合反時計回りで回頭をセットする
            clockwise = "clockwise" if self.__angle > 0 else "anticlockwise"
            command_list += "RT,%d,%d,%s\n" % (abs(self.__angle),
                                               GameMotion.ROTATION_PWM, clockwise)

        # 回頭後にエッジが切り替わる場合，エッジ切り替えをセットする
        if (next_edge := self.get_next_edge(self.__angle)) != self.current_edge:
            command_list += "EC,%s\n" % next_edge
            self.current_edge = next_edge  # 現在のエッジを更新する
        command_list += "DS,50,-40\n"  # 黒を認識するための後退
        command_list += "DL,50,0,-40,0.1,0.08,0.08\n"  # 中点までライントレース

        # 最初の行の末尾に",設置後復帰(→中点)"を追加する
        return command_list.replace("\n", ",設置後復帰(→中点)\n", 1)

    def get_cost(self) -> float:
        """設置後復帰(→中点)のゲーム動作のコストを計算するメソッド.

        Returns:
            float: コスト
        """
        return GameMotion.ROTATION_TIME[abs(self.__angle) // 45]  # 設置後復帰(→中点)は回頭時間だけコストとする
