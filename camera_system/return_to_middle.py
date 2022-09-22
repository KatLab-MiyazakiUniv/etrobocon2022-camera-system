"""設置後復帰(→中点)のゲーム動作モジュール.

設置後復帰(→中点)のゲーム動作のコマンド生成やコスト計算をする
パラメータは https://github.com/KatLab-MiyazakiUniv/etrobocon2022/pull/89 を参照
@author mutotaka0426
"""

from game_motion import GameMotion


class ReturnToMiddle(GameMotion):
    """設置後復帰(→中点)のゲーム動作クラス."""

    def __init__(self, angle: int, have_block: bool) -> None:
        """ReturnToMiddleのコンストラクタ.

        Args:
            angle: 方向転換の角度
            have_block: ブロックを保持している場合True

        """
        self.__angle = angle
        # rotation_angleは指定角度に対して実際に回頭する角度
        if have_block:  # ブロックを保持している場合
            self.__rotation_angle = GameMotion.ROTATION_BLOCK_TABLE[abs(angle)]["angle"]
            self.__rotation_pwm = GameMotion.ROTATION_BLOCK_PWM
            self.__rotation_time = GameMotion.ROTATION_BLOCK_TABLE[abs(angle)]["time"]
        else:  # ブロックを保持していない場合
            self.__rotation_angle = GameMotion.ROTATION_NO_BLOCK_TABLE[abs(angle)]["angle"]
            self.__rotation_pwm = GameMotion.ROTATION_NO_BLOCK_PWM
            self.__rotation_time = GameMotion.ROTATION_NO_BLOCK_TABLE[abs(angle)]["time"]
        self.__direct_rotation = "clockwise" if angle > 0 else "anticlockwise"

    def generate_command(self) -> str:
        """設置後復帰(→中点)のゲーム動作に必要なコマンドを生成するメソッド.

        Returns:
            str: コマンド
        """
        command_list = ""  # コマンドのリストを格納する文字列

        if self.__angle != 0:  # 回頭角度が0の場合は回頭のコマンドを生成しない
            # 回頭角度が正の数の場合時計回り，負の数の場合反時計回りで回頭をセットする
            command_list += "RT,%d,%d,%s\n" % (self.__rotation_angle,
                                               self.__rotation_pwm, self.__direct_rotation)

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
        return self.__rotation_time
