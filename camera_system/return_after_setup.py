"""設置後復帰のゲーム動作モジュール.

設置後復帰のゲーム動作のコマンド生成やコスト計算をする
パラメータは https://github.com/KatLab-MiyazakiUniv/etrobocon2022/pull/89 を参照
@author mutotaka0426
"""

from game_motion import GameMotion


class ReturnAfterSetup(GameMotion):
    """設置後復帰のゲーム動作クラス."""

    def __init__(self, angle: int, target_node: str, target_color: str = "NONE") -> None:
        """ReturnAfterSetupのコンストラクタ.

        Args:
            angle: 方向転換の角度
            target_node: 目標とするノード ("block" or "intersection" or middle")
            target_color: 目標となる交点の色（target_node=="intersection"の場合のみ使用）

        """
        self.__angle = angle
        self.__target_node = target_node
        self.__target_color = target_color

        expected_node = ["block", "intersection", "middle"]
        # 交点と中点とブロック置き場以外を指定された場合エラーを出す
        if self.__target_node not in expected_node:
            raise ValueError('"%s" is an Unexpected Node' % self.__target_node)

        if self.__target_node == "intersection":  # 交点が指定された場合
            expected_color = ["BLUE", "GREEN", "YELLOW", "RED"]
            # 交点の色以外を指定された場合エラーを出す
            if self.__target_color not in expected_color:
                raise ValueError('"%s" is an Unexpected Color' % self.__target_color)

    def generate_command(self) -> str:
        """設置後復帰のゲーム動作に必要なコマンドを生成するメソッド.

        Returns:
            str: コマンド
        """
        command_list = ""  # コマンドのリストを格納する文字列

        if self.__angle != 0:  # 回頭角度が0の場合はコマンドは生成しない
            # 回頭角度が正の数の場合時計回り，負の数の場合反時計回りで回頭をセットする
            clockwise = "clockwise" if self.__angle > 0 else "anticlockwise"
            command_list += "RT,%d,%d,%s\n" % (abs(self.__angle),
                                               GameMotion.ROTATION_PWM, clockwise)

        if self.__target_node == "block":
            # ToDo: ブロック置き場まで戻る場合のパラメータは未調整
            command_list += "DS,90,-70\n"  # ToDo: 仮のパラメータ
            self.current_edge = "none"  # 計算上のエッジをnoneにする
        elif self.__target_node == "intersection":
            # 回頭後にエッジが切り替わる場合，エッジ切り替えをセットする
            if (next_edge := self.get_next_edge(self.__angle)) != self.current_edge:
                command_list += "EC,%s\n" % next_edge
                self.current_edge = next_edge  # 現在のエッジを更新する

            command_list += "DS,70,-40\n"  # 黒を認識するための後退
            command_list += "CL,%s,0,-40,0.1,0.08,0.08\n" % self.__target_color  # 交点までライントレース
            command_list += "DS,15,60\n"  # 走行体が交差点に乗るように調整
        else:
            # ToDo: 中点まで戻る場合のパラメータは未調整
            # 回頭後にエッジが切り替わる場合，エッジ切り替えをセットする
            if (next_edge := self.get_next_edge(self.__angle)) != self.current_edge:
                command_list += "EC,%s\n" % next_edge
                self.current_edge = next_edge  # 現在のエッジを更新する
            command_list += "DL,80,0,-60,0.1,0.08,0.08\n"  # ToDo: 仮のパラメータ

        return command_list.replace("\n", ",設置後復帰\n", 1)  # 最初の行の末尾に",設置後復帰"を追加する

    def get_cost(self) -> float:
        """設置後復帰のゲーム動作のコストを計算するメソッド.

        Returns:
            float: コスト
        """
        return GameMotion.ROTATION_TIME[abs(self.__angle) // 45]  # 設置後復帰は回頭時間だけコストとする
